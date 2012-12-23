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

lStory_pagedown = {
    'extend': function(editor) {
        var refresh = function() {
            $(editors).each(function() { this.refreshPreview(); });
        };
        $('.wmd-button-row').each(function() {
                var button_row = this;
                if($(button_row).find('.wmd-imd-button').length>0) {
                    return;
                }
                var li = $(document.createElement('li'));
                li.attr('class', 'wmd-button wmd-imd-button');
                li.attr('id', 'wmd-imd-button');
                li.append('<img src="/static/img/admin/wmd-imd-button.png" />');
                li.attr('style', 'left: '+ $(button_row).children().length*25+'px');
                $(button_row).append(li);
                $(li).click(function() {
                    var elem = $(this);
                    var ta = elem.parents('.wmd-panel').find('textarea').first();
                    if(ta.getSelection()) {
                        ta.wrapSelection('[imd]','[/imd]');
                        setTimeout(refresh,10);
                    } else {
                        MessageBoxes.Prompt('Enter IMD text here',
                            "In more Detail",
                            [{label: 'text', type: 'textarea', name: 'text'}],
                            function(data) {
                                ta.replaceSelection('[imd]'+data.text+'[/imd]');
                                setTimeout(refresh,10);
                            });
                    }
                    });
                li = $(document.createElement('li'));
                li.attr('class', 'wmd-button wmd-imd-button');
                li.attr('id', 'wmd-imd-button');
                li.append('<img src="/static/img/admin/wmd-preview-button.png" />');
                li.attr('style', 'left: '+ $(button_row).children().length*25+'px');
                $(button_row).append(li);
                $(li).click(function() {
                    var elem = $(this);
                    var ta = elem.parents('.wmd-panel').find('textarea').first();
                    text = ta.val();
                    var div = document.createElement('div');
                    $(div).addClass('text');
                    $(document).append(div);
                    $(div).load('/api/preview/', {'text': text}, function() {initInMoreDetail();});
                    $(div).dialog({modal: true, width: 609, beforeClose: function() { $(div).remove();div=null; }});
                    $(div).attr('style', 'height: 400px; overflow: scroll; background-color: white;');
                });
            });
        return true;
    }
}
