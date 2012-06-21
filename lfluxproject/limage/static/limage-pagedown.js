lImage_pagedown = {
    'extend': function(imageurl, dialogdiv, editor) {
        editor.hooks['insertImageDialog'] = function(callback) {
            var buildForm = function(data, textStatus, jqXHR) {
                $('#'+dialogdiv).empty();
                var imagecontainer = document.createElement('div');
                for(var i=0;i<data['images'].length;i++) {
                    var x =data['images'][i];
                    var el = document.createElement('img');
                    $(el).attr('src', x['url']);
                    el.onclick = function() {
                        callback(x['url']);
                        $('#'+dialogdiv).dialog('close');
                    };
                    var cnt = document.createElement('div');
                    $(cnt).addClass('image');
                    $(cnt).append(el);
                    $(imagecontainer).append(cnt);
                }
                $('#'+dialogdiv).append(imagecontainer);
                $(imagecontainer).addClass('imagegrid');
                if(data['enable_upload']) {
                    var form = document.createElement('form');
                    $(form).append('<h3>Upload new picture:</h3>');
                    $(form).attr('action', imageurl);
                    $(form).attr('method', 'post');
                    $(form).addClass('imageuploadform');
                    $(form).ajaxForm();
                    $(form).append(data['form']);
                    $(form).append('<p><input type="submit" value="Upload" /></p>');
                    $('#'+dialogdiv).append('<hr />');
                    $('#'+dialogdiv).append(form);
                    $(form).ajaxForm({beforeSubmit: function() {$('#'+dialogdiv+' input[type=submit]').addClass('loading');}, success: buildForm});
                } else {
                    var form = document.createElement('form');
                    $(form).append(data['form']);
                    $('#'+dialogdiv).append(form);
                }
            };
            $.getJSON(imageurl, buildForm);
            $('#'+dialogdiv).dialog({close: function() { $('.wmd-prompt-background').hide(); }, width: '700px'});
            return true;
        };
    }
}
