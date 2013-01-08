(function($) { 
    $.fullTextArea_cache = {};
    $.fn.fullTextArea = function(options) {
        this.each(function() {
            var textarea = this;
            if($(this).data('fulltextarea-initialized')) {
                return;
            }
            $(this).data('fultextarea-initialized','true');
            var holder = document.createElement('div');
            $(holder).css('position', 'relative');
            $(this).after(holder);
            $(holder).append(this);
            var button = $('<button style="position: absolute; right: 10px; bottom: 10px; background: black; background: rgba(0,0,0,.8); color: white; color: rgba(255,255,255,.8); border: none; font-size: 3em; border-radius: 10px;">⎙</button>');
            $(holder).append(button)
            $(button).click(function() {
                var overlay = $('<div class="fullscreen-overlay" style="position: fixed; top: 0; left: 0; height: 100%; width: 100%; background-color: black;"><textarea style="width: 700px; position: absolute; left: 50%; margin-left: -350px; margin-top: 1em; height: 100%; font-size: 1.5em; background-color: black; color: rgb(200,200,200); border: none;"></textarea><button style="color: white; background-color: grey; border-radius: 10px; font-size: 2em; border: none; margin: 1em;">X</button></div>');
                var newta = $(overlay).find('textarea');
                $(newta).val($(textarea).val());
                $(newta).keypress(function() { $(textarea).val($(newta).val()); });
                $(overlay).find('button').click(function() {$(overlay).remove();});
                $(document.body).append(overlay);
                return false;
            });
        });
    };
})(jQuery);
