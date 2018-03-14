function get_image_asset(div_id, slug, size=null, crop=null, quality=null) {
    $.ajax({
        url: '/ajax/get_asset/',
        data: {
            'type': 'image',
            'slug': slug,
            'size': size,
            'crop': crop,
            'quality': quality
        },
        dataType: 'json',
        success: function(data) {
            $(div_id).href = data['url'];
        },
        error: function() {
            console.log("Error");
        }
    });
}

function get_file_asset(div_id, slug) {
    $.ajax({
        url: '/ajax/get_asset/',
        data: {
            'type': 'file',
            'slug': slug
        },
        dataType: 'json',
        success: function(data) {
            $(div_id).href = data['url'];
        },
        error: function() {
            console.log("Error");
        }
    });
}