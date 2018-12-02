function update_sort_tab(sort_tab) {
    $.post('/blog/update_sort_tab/'.concat(sort_tab));

    var currSelected = document.getElementById('blog-sort-'.concat(sort_tab));
    if (currSelected == null) { return; }
    if (currSelected.getAttribute('aria-selected') == "true") {
        if (sort_tab == "date") {
            window.location = "/blog/";
        }
        else {
            window.location = "/blog/".concat(sort_tab.concat('.html'));
        }
    }
}

function blog_search() {
    var search_text = document.getElementById('search-input').value;
    var clean_url = '/blog/search.html?q='.concat(encodeURI(search_text));
    document.getElementById('blog-search-submit').href=clean_url;
}

function blog_search_enter() {
    blog_search();
    document.getElementById('blog-search-submit').click();
}

document.getElementById("search-input")
    .addEventListener("keyup", function(event) {
	event.preventDefault();
	if(event.keyCode == 13) {
	    blog_search_enter();
	}
    });
