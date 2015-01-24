    $.contextMenu({
    selector: '.icon',
    callback: function(key, options) {
        console.log("Clicked: " + key)
    },
    items: {
        open: {
            name: "Open",
            callback: function(key, opts) {
                console.log($(this).text());
                }
        },
        separator: "-----------",
        rename: {
            name: "Rename",
            callback: function(key, opts) {
                var name = prompt("Input new name:");
                console.log("Renaming " + $(this).text() + " to " + name);
            }
        }
    }
});
$.contextMenu({
    selector: '#view',
    items: {
        'newdoc': {
            name: "New document",
            callback: function(key, opts) {
                var name = prompt("New document name:");
                console.log(name);
            }
        },
        'newfolder': {
            name: "New directory",
            callback: function(key, opts) {
                var name = prompt("New folder name:");
                if (!name)
                    return false;
                $.ajax(
                    "/__netfm_api/folder/",
                    {
                        type: "POST",
                        data: {
                            action: "new",
                            target: name
                        },
                        success: function(data) {
                            $("#dialog").text(data.message);
                            $("#dialog").dialog({
                                modal: true,
                                buttons: {
                                    Ok: function() { $(this).dialog("close"); }
                                }
                            });
                        },
                        error: function(xhr) {
                            $("#dialog").text(xhr.responseJSON.message);
                            $("#dialog").dialog({
                                modal: true,
                                buttons: {
                                    Ok: function() { $(this).dialog("close"); }
                                }
                            });
                        }
                    }
                );
            }
        }
    }
});