function scrollTimelineToAppropriateDate() {
    var highlight_el = $('.timeline.highlight a[data-date="'+$('#article').data('article-previous-date')+'"]');
    var version_el = $('.timeline.version a[data-date="'+$('#article').data('article-version-date')+'"]');
    if(version_el.length>0 && version_el.offset().left!=0) {
        $('.timeline.version').scrollTo(version_el);
    }
    if(highlight_el.length>0 && highlight_el.offset().left!=0) {
        $('.timeline.highlight').scrollTo(highlight_el);
    }
}


function initMarkAsRead() {

    var mark_as_read_if_needed = function() {
        $('#mark_as_read .tracking-status').each(function(){
            if($(this).data('track') == 'yes') {
                var element = $(this);
                var f = function() {
                    element.load($('#article').data('mark-as-read'), function() { });
                };
                setTimeout(f, 2500);
            }
        });
    };

    $('#end_of_article').waypoint(function() {
        if($('#article').data('article-current') == 'False' || $('#article').data('article-changed') == 'False')
            return;
        $('#mark_as_read').removeClass('hiding');
        mark_as_read_if_needed();
    }, {'offset': '100%'});
    var eh = function(event) {
        event.preventDefault();
        event.stopPropagation();
        var element = $(this).parent('.reload-here');
        $(this).parent('.reload-here').addClass('loading');
        $(this).parent('.reload-here').load($(this).attr('href'), function() { mark_as_read_if_needed(); element.removeClass('loading'); } );
    };
    $('#mark_as_read .tracking-status').on('click', 'a', eh);

    $('#mark_as_read').on('click', 'a', eh);
}

$(document).ready(initMarkAsRead);

initTimelines_done = false;
function initTimelines() {
    if(initTimelines_done) {
        scrollTimelineToAppropriateDate();
        return;
    }
    initTimelines_done = true;
    var width = $('.timeline li .month').parent().map(
            function() {
                return $(this).offset()['left']+$(this).outerWidth() - $(this).parents('.timeline').offset()['left'] + 1;
           }).toArray().reduce(function(x,y){return (x>y?x:y);});
    $('.timeline .months').attr('style', 'width: '+width+'px;');

    var highlight_scroll = $('#article').data('article-previous-date');
    var version_scroll = $('#article').data('article-version-date');

    if(highlight_scroll) {
        var highlight_el = $('.timeline.highlight a[data-date="'+highlight_scroll+'"]');
        highlight_el.addClass('mark');
    }
    if(version_scroll) {
        var version_el = $('.timeline.version a[data-date="'+version_scroll+'"]');
        version_el.addClass('mark');
    }
    scrollTimelineToAppropriateDate();
}

function initHistoryView() {
    $('.historyform a.switch').click(function() {
        var which = $(this).hasClass('version')?'version':'highlight';
        $(this).closest('.historyform').each(function(i,e){
            $(e).attr('class','historyform '+($(e).hasClass(which)?'':which));
        });
        setTimeout(initTimelines, 0);
    });
}

$(document).ready(initHistoryView);
