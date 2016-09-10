convertDataToDate = function(data) {
    for (var i=0; i<data.length; i++) {
        data[i][0] = Date.parse(data[i][0]);
    }
    return data;
};

posts_by_day = function(data) {
    $('#id_posts_by_day').highcharts({
        chart: {
            type: 'line',
            zoomType: 'x'
        },
        title: {
            text: 'Posts By Day'
        },
        xAxis: {
            type: 'datetime',
            range: 6 * 30 * 24 * 3600 * 1000
        },
        rangeSelector: {
            enabled: true
        },
        scrollbar: {
            enabled: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total Posts'
            }
        },
        series: [{
            name: 'Total Posts',
            data: convertDataToDate(data.data)
        }
        ]
    });
};

updateView = function() {
    $('.statistics').hide();
    var viewType = $('#id_select_statistics').val();
    $("#id_" + viewType).show();

    var viewFunction = window[viewType];
    if (typeof viewFunction === "function") {
        $.ajax({
            url: viewType,
            contentType: 'application/json',
            success: function (data, textStatus, jqXHR) {
                if ($.isEmptyObject(data)) {
                    $("." + viewType + "_error").show();
                } else {
                    viewFunction(data);
                }
            }
        });
    }
};

$(document).ready(function () {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    $('#id_select_statistics').on('change', updateView);
    updateView();
});
