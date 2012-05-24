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
