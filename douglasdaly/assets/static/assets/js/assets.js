function getImageAsset(img_id, slug, size=null, crop=null, quality=null) {
    $.ajax({
        url: '/' + assetBaseUrl + '/get_asset/',
        data: {
            'type': 'image',
            'slug': slug,
            'size': size,
            'crop': crop,
            'quality': quality
        },
        dataType: 'json',
        success: function(data) {
            var docElement = document.getElementById(img_id);
            if(docElement != null) {
                docElement.src = data['url'];
                return true;
            } else {
                console.log('Error: No element named: ' + img_id)
                return false;
            }
        },
        error: function() {
            console.log("AJAX Error");
        }
    });
}

function getFileAsset(div_id, slug) {
    if (assetBaseUrl == null) {
        console.log("Error: Base Asset app URL is not set");
        return false;
    }
    $.ajax({
        url: '/' + assetBaseUrl + '/get_asset/',
        data: {
            'type': 'file',
            'slug': slug
        },
        dataType: 'json',
        success: function(data) {
            var docElement = document.getElementById(div_id);
            if (docElement != null) {
                docElement.href = data['url'];
                return true;
            } else {
                console.log("Error: No element named: " + div_id)
                return false;
            }
        },
        error: function() {
            console.log("AJAX Error");
        }
    });
}
