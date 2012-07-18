/* from http://jsperf.com/jquery-scrollable */
(function($) {
   $.extend($.expr[":"], {
    scrollable: function(element) {
     var vertically_scrollable, horizontally_scrollable;
     if ($(element).css('overflow') == 'scroll' || $(element).css('overflowX') == 'scroll' || $(element).css('overflowY') == 'scroll') return true;
  
     vertically_scrollable = (element.clientHeight < element.scrollHeight) && (
     $.inArray($(element).css('overflowY'), ['scroll', 'auto']) != -1 || $.inArray($(element).css('overflow'), ['scroll', 'auto']) != -1);
  
     if (vertically_scrollable) return true;
  
     horizontally_scrollable = (element.clientWidth < element.scrollWidth) && (
     $.inArray($(element).css('overflowX'), ['scroll', 'auto']) != -1 || $.inArray($(element).css('overflow'), ['scroll', 'auto']) != -1);
     return horizontally_scrollable;
    }
   });
  })(jQuery)
