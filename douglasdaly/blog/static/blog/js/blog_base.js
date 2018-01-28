function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function update_sort_tab(sort_tab) {
    $.post('/blog/update_sort_tab/'.concat(sort_tab));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	    xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    }
});
