/*
 * Copyright (c) 2009 Benoit Chesneau <benoitc@e-engura.org> 
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.

 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 * Some code borrowed to livepipe :
 * Copyright 2008 PersonalGrid Corporation <http://personalgrid.com/>
 * License MIT
 * Url: http://livepipe.net/control/textarea
 *
 */
(function($) {
    $.fn.getSelection = function(){
      if(!!document.selection)
        return document.selection.createRange().text;
      else if(!!this.first()[0].setSelectionRange)
        return this.first()[0].value.substring(this.first()[0].selectionStart,this.first()[0].selectionEnd);
      else
      return false;
    };
    
    $.fn.replaceSelection = function(text){
      var scroll_top = this.first()[0].scrollTop;
      if(!!document.selection){
        this.first()[0].focus();
        var range = (this.range) ? this.range : document.selection.createRange();
        range.text = text;
        range.select();
      }else if(!!this.first()[0].setSelectionRange){
        var selection_start = this.first()[0].selectionStart;
        this.first()[0].value = this.first()[0].value.substring(0,selection_start) + text + this.first()[0].value.substring(this.first()[0].selectionEnd);
        this.first()[0].setSelectionRange(selection_start + text.length,selection_start + text.length);
      }
      this.first()[0].focus();
      this.first()[0].scrollTop = scroll_top;
    };

    $.fn.wrapSelection = function(before,after){
      this.replaceSelection(before + this.getSelection() + after);
    };
})(jQuery);



