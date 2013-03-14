function scrollTimelineToAppropriateDate() {
    var highlight_el = $('.timeline.highlight a[data-date="'+$('#article').data('article-previous-date')+'"]');
    var version_el = $('.timeline.version a[data-date="'+$('#article').data('article-current-date')+'"]');
    if(version_el.length>0 && version_el.offset().left!=0) {
        $('.timeline.version').scrollTo(version_el, {'over': -33});
    }
    if(highlight_el.length>0 && highlight_el.offset().left!=0) {
        $('.timeline.highlight').scrollTo(highlight_el, {'over': -33});
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
        if($('#article').data('allow-mark-as-read') != 'True')
            return;
        $('#mark_as_read').removeClass('hiding');
        mark_as_read_if_needed();
    }, {'offset': '100%'});

    var eh = function(event) {
        if($(this).hasClass('ignorereload'))
            return;
        event.preventDefault();
        event.stopPropagation();
        var element = $(this).parents('.reload-here');
        $(this).parents('.reload-here').addClass('loading');
        $(this).parents('.reload-here').load($(this).attr('href'), function() { mark_as_read_if_needed(); element.removeClass('loading'); } );
    };
    $('#mark_as_read .tracking-status').on('click', 'a', eh);
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
    var version_scroll = $('#article').data('article-current-date');

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
        var newclass = 'history'+which;

        $(document.body).each(function(i,e){
            var show = !$(this).hasClass(newclass);
            $(this).removeClass('historyhighlight');
            $(this).removeClass('historyversion');
            if(show) {
                $(this).addClass(newclass);
            }
        });
        setTimeout(initTimelines, 100);
    });
}

$(document).ready(initHistoryView);

function initForms() {
    var elems = $('form.replacecontent');
    $.each(elems, function() {
        var elem = $(this);
        opts = {'success': function(data, statusText, xhr, form) {
                var e = elem.find('.replace_here');
                if(!e) {
                    e = elem;
                }
                if(data['error']) {
                    e.html(data['error']);
                } else if(data['form']) {
                    e.html(data['form']);
                } else if(data['result']) {
                    elem.html(data['result']);
                }
            }
        };
        if($(elem).data('request-type')) {
            opts['target'] = elem;
        }
        console.log('ajaxforming');
        elem.ajaxForm(opts);
    });
}
$(document).ready(initForms);


function openLinksInNewWindow() {
    $("a[href^=http]").each(function(){
        if(this.href.indexOf(location.hostname) == -1) {
            $(this).attr({
                target: "_blank",
            });
        }
    });
}
$(document).ready(openLinksInNewWindow);

function initSidebarTabs() {
    $('#sidebar .tabs a').click(function() {
        var tab = $(this);
        tab.parents('.tabs li').siblings().removeClass('sel');
        tab.parents('.tabs li').addClass('sel');
        var content = $(tab.attr('href'));
        content.siblings().not('.share').hide();
        content.show();
        tab.parents('.tabs').show();
        return false;
    });
}
$(document).ready(initSidebarTabs);

function initFeaturetour() {
    $('#featuretourbtn').click(function(event) {
        event.preventDefault();
        event.stopPropagation();
        $('#featuretour').joyride({'tipLocation': 'top', 'tipContainer': document.body, 'nubPosition': 'bottom',});
    });
}
$(document).ready(initFeaturetour);
