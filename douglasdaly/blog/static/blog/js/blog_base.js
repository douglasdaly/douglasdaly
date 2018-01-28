function update_sort_tab(sort_tab) {
    $.post('/blog/update_sort_tab/'.concat(sort_tab));
}
