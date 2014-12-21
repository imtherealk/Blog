var toggle_comment_box = function(url, entry_id) {
    var elt = $('comment_box_'+entry_id);

    if ( elt.visible() == true ) {
        elt.hide();
    }
    else {
        var ajax = new Ajax.Updater(elt, url);
        elt.show();
    }
}
