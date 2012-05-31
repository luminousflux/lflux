lImage_pagedown = {
    'extend': function(imageurl, dialogdiv, editor) {
        editor.hooks['insertImageDialog'] = function(callback) {
            var buildForm = function(data, textStatus, jqXHR) {
                $('#'+dialogdiv).empty();
                $('#'+dialogdiv).append('<p>to upload images, go to the <a href="/admin/limage/image/">image admin</a> interface. we will fix this soon.</p>')
                for(var i=0;i<data['images'].length;i++) {
                    var x =data['images'][i];
                    var el = document.createElement('img');
                    $(el).attr('src', x['url']);
                    $(el).attr('style', 'max-width: 100px; max-height: 100px; cursor: pointer;');
                    el.onclick = function() {
                        callback(x['url']);
                        $('#'+dialogdiv).dialog('close');
                    };
                    $('#'+dialogdiv).append(el);
                }
                var form = document.createElement('form');
                $(form).attr('action', imageurl);
                $(form).attr('method', 'post');
                $(form).ajaxForm();
                $(form).append(data['form']);
                $('#'+dialogdiv).append(form);
                $(form).ajaxForm({success: buildForm});
            };
            $.getJSON(imageurl, buildForm);
            $('#'+dialogdiv).dialog({close: function() { $('.wmd-prompt-background').hide(); }});
            return true;
        };
    }
}
