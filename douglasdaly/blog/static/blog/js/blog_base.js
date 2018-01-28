function update_sort_tab(sort_tab) {
    $.post('/blog/update_sort_tab/'.concat(sort_tab));
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
