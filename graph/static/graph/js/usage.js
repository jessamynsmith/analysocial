$(function () {
    $('#id_usage').highcharts({
        title: {
            text: 'KeyWord Usage by Post',
            x: -20 //center
        },
        xAxis: {
            categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        },
        yAxis: {
            title: {
                text: 'Posts Containing Keyword'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Total Posts',
            data: [10, 3, 5, 6, 4, 7, 9]
        }, {
            name: 'Obama',
            data: [2, 0, 2, 1, 0, 0, 3]
        }, {
            name: 'Trump',
            data: [5, 2, 3, 2, 0, 4, 4]
        }, {
            name: 'Hillary',
            data: [2, 0, 1, 3, 4, 2, 3]
        }]
    });
});
