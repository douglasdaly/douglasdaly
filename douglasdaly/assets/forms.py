# -*- coding: utf-8 -*-
"""
Custom forms for the Asset application.

:author: Douglas Daly
:date: 2/18/2019
"""
#
#   Imports
#
import os
import pickle
import zipfile
import tempfile

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import ImageAsset, FileAsset, VideoAsset


#
#   Form classes
#

class BulkUploadForm(forms.Form):
    """
    Custom form for bulk asset uploads
    """
    bulk_file = forms.FileField(label="Bulk file for upload",
                                allow_empty_file=False)
    overwrite_existing = forms.BooleanField(label="Overwrite existing assets?",
                                            initial=False, required=False)

    class Meta:
        description = _(
            "File for bulk upload, it must be a zip archive with a "
            "special file called '__assets.pkl' containing a "
            "dictionary of file to Asset creation kwargs."
        )

    # - Action methods

    def process_bulk_file(self):
        """Processes the bulk_file given"""
        added_items = dict()
        replaced_items = dict()
        error_items = dict()
        with tempfile.TemporaryDirectory() as tmp_dir:
            # - Extract file data
            with tempfile.NamedTemporaryFile(dir=tmp_dir) as tmp:
                for chunk in self.cleaned_data['bulk_file'].chunks():
                    tmp.write(chunk)
                tmp.seek(0)

                zipfile.ZipFile(tmp).extractall(path=tmp_dir)

            # - Get listing object
            with open(os.path.join(tmp_dir, '__assets.pkl'), 'rb') as fin:
                asset_listing = pickle.load(fin)

            # - Iterate and create assets
            for filename, meta_data in asset_listing.items():
                a_type = meta_data.pop('type', None)
                if a_type == 'image':
                    asset_cls = ImageAsset
                elif a_type == 'video':
                    asset_cls = VideoAsset
                elif a_type == 'file':
                    asset_cls = FileAsset
                else:
                    error_items[filename] = meta_data
                    error_items[filename]['error'] = \
                        "Invalid asset type: %s" % a_type
                    continue

                # - Check exists
                curr_obj = asset_cls.objects.filter(slug=meta_data['slug'])\
                                    .first()
                if curr_obj:
                    if self.cleaned_data['overwrite_existing']:
                        curr_obj.delete()
                    else:
                        error_items[filename] = meta_data
                        error_items[filename]['error'] = "Asset already exists"
                        continue

                with open(os.path.join(tmp_dir, filename), 'rb') as fin:
                    t_asset_file = SimpleUploadedFile(filename, fin.read())

                try:
                    new_asset = asset_cls(**meta_data, asset=t_asset_file)
                    new_asset.save()
                except Exception as ex:
                    error_items[filename] = meta_data
                    error_items[filename]['error'] = ex
                    continue

                if not curr_obj:
                    added_items[filename] = meta_data
                else:
                    replaced_items[filename] = meta_data

        return added_items, replaced_items, error_items

    # - Utility methods

    def save(self):
        """Override save for form action"""
        try:
            add_items, replace_items, error_items = self.process_bulk_file()
        except Exception as ex:
            error_message = str(ex)
            self.add_error(None, error_message)
            raise

        return add_items, replace_items, error_items
