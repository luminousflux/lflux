function initHistoryView() {
    /* versions is an array of datetimes */

    var versions = [];
    $('.history a').each(function(i, e) {
        versions.push(new Date($(e).data('date')));
    });

    var since = $('input.since');
    var until = $('input.until');

    var highlightDates = function(date) {
        var result = null;
        $(versions).each(function(i,e) {
            if(e.toISOString().substring(0,10) == date.toISOString().substring(0,10))
                result = e;
        });
        if(result)
            return [true, 'selectable','asdf'];
        return [false, '', 'asdfghjkloe'];
    };

    options = {beforeShowDay: highlightDates, dateFormat: 'yy-mm-dd', minDate: versions[0], maxDate: versions[versions.length-1]};

    since.datepicker(options);
    until.datepicker(options);

    $('input.date').datepicker(options);

    $('.historyform a[rel=switch]').click(function() {
        $(this).closest('.historyform').each(function(i,e){ $(e).toggleClass('highlight'); $(e).toggleClass('version'); });
    });
}

$(document).ready(initHistoryView);

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
