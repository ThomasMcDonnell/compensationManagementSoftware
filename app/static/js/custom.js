
    var getData = $.get('/record/api')
    getData.done(function (results) {
        var data = {
            // A labels array that can contain any sort of values
            labels: results.date,
            // Our series array that contains series objects or in this case series data arrays
            series: [
                results.bonus
            ]
        }
        var options = {
            showArea: true
        }
        // Create a new line chart object where as first parameter we pass in a selector
        // that is resolving to our chart container element. The Second parameter
        // is the actual data object.
        var myChart = new Chartist.Line('.ct-chart-one', data, options);

        var data = {
            labels: results.date,
            series: [
                results.bonus
            ]
        };

        var options = {
            seriesBarDistance: 5
        };

        var responsiveOptions = [
            ['screen and (max-width: 640px)', {
                axisX: {
                    labelInterpolationFnc: function (value) {
                        return value[0];
                    }
                }
            }]
        ];

        var myBarChart = new Chartist.Bar('.ct-chart-two', data, options, responsiveOptions);

        var data = {
            labels: results.date,
            series: [results.msr]
        };

        var options = {
            seriesBarDistance: 5,
            reverseData: true,
            horizontalBars: true,
            axisY: {
                offset: 70
            }
        };

        var myMsrBarChart = new Chartist.Bar('.ct-chart-three', data, options)
    });
    var getData = $.get('/record/qtr/api')
    getData.done(function (results) {
        var data = {
            labels: ['QTR 1', 'QTR 2', 'QTR 3', 'QTR 4'],
            series: [results.qtr1, results.qtr2, results.qtr3, results.qtr4]
        };

        var options = {
            labelInterpolationFnc: function (value) {
                return value[0]
            }
        };

        var responsiveOptions = [
            ['screen and (min-width: 640px)', {
                chartPadding: 30,
                labelOffset: 100,
                labelDirection: 'explode',
                labelInterpolationFnc: function (value) {
                    return value;
                }
            }],
            ['screen and (min-width: 1024px)', {
                labelOffset: 80,
                chartPadding: 20
            }]
        ];

        new Chartist.Pie('.ct-chart-four', data, options, responsiveOptions);
    });