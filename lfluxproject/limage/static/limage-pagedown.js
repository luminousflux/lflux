lImage_pagedown = {
    'extend': function(imageurl, dialogdiv, editor) {
        editor.hooks['insertImageDialog'] = function(callback) {
            $.getJSON(imageurl, function(data, textStatus, jqXHR) {
                $('#'+dialogdiv).empty();
                for(var i=0;i<data.length;i++) {
                    var x =data[i];
                    console.log(x);
                    var el = document.createElement('img');
                    $(el).attr('src', x['url']);
                    $(el).attr('style', 'max-width: 100px; max-height: 100px; cursor: pointer;');
                    el.onclick = function() {
                        callback(x['url']);
                        $('#'+dialogdiv).dialog('close');
                    };
                    $('#'+dialogdiv).append(el);
                }
                $(dialogdiv).dialog
            });
            $('#'+dialogdiv).dialog();
            return true;
        };
    }
}
