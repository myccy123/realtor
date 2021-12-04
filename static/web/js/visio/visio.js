$(document).ready(function() {

    var boostMOD = document.createElement('script')
    boostMOD.setAttribute('src', 'http://www.janetech.cn:8080/static/bi/js/boost.js')
    document.body.appendChild(boostMOD)

    var moreMOD = document.createElement('script')
    moreMOD.setAttribute('src', 'http://www.janetech.cn:8080/static/bi/js/highcharts-more.js')
    document.body.appendChild(moreMOD)

})


function makeChart(id, chartid, filters) {

    $.ajax({
        type: 'POST',
        url: 'http://47.96.81.211:8080/bi/gen/chart/',
        data: { chartid: chartid, filters: JSON.stringify(filters) },
        dataType: 'JSON',
        success: function(resp) {
            if (resp.code == '0') {

                if (resp.charttype == 'table') {
                    $("#"+id).empty()
                    // $("#"+id).css('background','none')
                    $("#"+id).append('<iframe src="/table/'+chartid+'" width="100%" frameborder="0" height="100%"></iframe>')
                    return
                }


                if (resp.diy == '1') {
                    let code = resp.diycode.replace('targetDOM', id)
                    eval(code)
                } else if (resp.static == '1') {
                    let charttype = resp.charttype
                    $.ajax({
                        type: 'GET',
                        url: resp.data,
                        dataType: 'JSON',
                        success: function(jsn) {

                            let data = jsn.data
                            if (data.type == 'line' || data.type == 'label_line' || data.type == 'reverse_line' || data.type == 'bigdata_line') {
                                return make_line(id, data)
                            }
                            if (data.type == 'column' || data.type == 'label_column' || data.type == 'stack_column' || data.type == 'percent_column' || data.type == 'nesting_column') {
                                return make_column(id, data)
                            }
                            if (data.type == 'bar' || data.type == 'stack_bar' || data.type == 'range_bar') {
                                return make_bar(id, data)
                            }
                            if (data.type == 'pie' || data.type == 'legend_pie' || data.type == 'double_pie' || data.type == 'sector_pie' || data.type == 'blank_pie') {
                                return make_pie(id, data)
                            }
                            if (data.type == 'area' || data.type == 'stack_area' || data.type == 'break_area' || data.type == 'curve_area' || data.type == 'range_area' || data.type == 'average_area') {
                                return make_area(id, data)
                            }
                            if (data.type == 'scatter' || data.type == 'subline_scatter' || data.type == '3d_scatter' || data.type == 'bigdata_scatter') {
                                return make_scatter(id, data)
                            }
                        }
                    })
                } else {
                    let data = resp.data
                    if (data.type == 'line' || data.type == 'label_line' || data.type == 'reverse_line' || data.type == 'bigdata_line') {
                        return make_line(id, data)
                    }
                    if (data.type == 'column' || data.type == 'label_column' || data.type == 'stack_column' || data.type == 'percent_column' || data.type == 'nesting_column') {
                        return make_column(id, data)
                    }
                    if (data.type == 'bar' || data.type == 'stack_bar' || data.type == 'range_bar') {
                        return make_bar(id, data)
                    }
                    if (data.type == 'pie' || data.type == 'legend_pie' || data.type == 'double_pie' || data.type == 'sector_pie' || data.type == 'blank_pie') {
                        return make_pie(id, data)
                    }
                    if (data.type == 'area' || data.type == 'stack_area' || data.type == 'break_area' || data.type == 'curve_area' || data.type == 'range_area' || data.type == 'average_area') {
                        return make_area(id, data)
                    }
                    if (data.type == 'scatter' || data.type == 'subline_scatter' || data.type == '3d_scatter' || data.type == 'bigdata_scatter') {
                        return make_scatter(id, data)
                    }
                }
            } else {
                $("#" + id).append('<div class="error-text">' + resp.desc + '</div>')
            }
        }
    })
}


function make_line(id, data) {
    let dataLen
    if (data.series.length == 0) {
        dataLen = 0
    } else {
        dataLen = data.series[0].data.length
    }
    var chart = Highcharts.chart({
        chart: {
            renderTo: id,
            type: data.chart,
            zoomType: dataLen > 100 ? 'x' : null,
            inverted: data.type == 'reverse_line'
        },
        boost: {
            useGPUTranslations: dataLen > 100
        },
        title: {
            text: data.title
        },
        subtitle: {
            text: data.subtitle
        },
        xAxis: {
            type: 'category',
            categories: data.categories,
            title: {
                text: null
            }
        },
        yAxis: {
            title: {
                text: data.yunit
            }
        },
        plotOptions: {
            spline: {
                marker: {
                    // 线上是否标点
                    enabled: true,

                    // 点的大小，默认4
                    radius: dataLen > 100 ? 2 : 4
                },
                dataLabels: {
                    // 开启数据标签
                    enabled: data.type == 'label_line',
                    allowOverlap: data.type == 'label_line',
                    formatter: function() {
                        return data.labelformat == '' ? this.point.y : eval(data.labelformat)
                    }
                }
            },
            series: {
                turboThreshold: dataLen * 10,
                lineWidth: dataLen > 100 ? 0.5 : 1
            }
        },
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 768
                },
                chartOptions: {
                    plotOptions: {
                        spline: {
                            dataLabels: {
                                allowOverlap: false
                            }
                        }
                    }
                }
            }]
        },
        series: data.series
    });
    return chart
}

function make_column(id, data) {
    let dataLen
    if (data.series.length == 0) {
        dataLen = 0
    } else {
        dataLen = data.series[0].data.length
    }

    var chart = Highcharts.chart({
        chart: {
            renderTo: id,
            type: data.chart
        },
        title: {
            text: data.title
        },
        subtitle: {
            text: data.subtitle
        },
        tooltip: {
            shared: true
        },
        xAxis: {
            categories: data.categories,
            crosshair: true
        },
        yAxis: {
            title: {
                text: data.yunit
            }
        },
        plotOptions: {
            column: {
                borderWidth: 0,
                stacking: data.type == 'stack_column' ? 'normal' : data.type == 'percent_column' ? 'percent' : null,
                dataLabels: {
                    // 开启数据标签
                    enabled: data.type == 'label_column',
                    allowOverlap: data.type == 'label_column',
                    formatter: function() {
                        return data.labelformat == '' ? this.point.y : eval(data.labelformat)
                    }
                }
            },
            series: {
                turboThreshold: dataLen
            }
        },
        series: data.series
    });
    return chart
}

function make_bar(id, data) {

    var chart = Highcharts.chart({
        chart: {
            renderTo: id,
            type: data.type == 'range_bar' ? 'columnrange' : data.chart,
            inverted: data.type == 'range_bar'
        },
        title: {
            text: data.title
        },
        subtitle: {
            text: data.subtitle
        },
        tooltip: {
            shared: true
        },
        xAxis: {
            categories: data.categories,
            crosshair: true
        },
        yAxis: {
            title: {
                text: data.yunit
            }
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                stacking: data.type == 'stack_bar' ? 'normal' : null
            },
            bar: {
                dataLabels: {
                    // 开启数据标签
                    formatter: function() {
                        return data.labelformat == '' ? this.point.y : eval(data.labelformat)
                    }
                }
            },
            columnrange: {
                dataLabels: {
                    // 开启数据标签
                    enabled: true,
                    formatter: function() {
                        return data.labelformat == '' ? this.point.y : eval(data.labelformat)
                    }
                }
            }

        },
        series: data.series
    });
    return chart
}

function make_pie(id, data) {


    var chart = Highcharts.chart({
        chart: {
            renderTo: id
        },
        title: {
            text: data.title
        },
        subtitle: {
            text: data.subtitle
        },
        tooltip: {
            shared: true
        },
        xAxis: {
            categories: data.categories,
            crosshair: true
        },
        yAxis: {
            title: {
                text: data.yunit
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    // 开启数据标签
                    enabled: true,
                    formatter: function() {
                        return data.labelformat == '' ? this.point.y + '  ' + Highcharts.numberFormat(this.percentage, 1) + '%' : eval(data.labelformat)
                    }
                },
                center: data.type == 'sector_pie' ? ['50%', '75%'] : [null, null],
                showInLegend: data.type == 'legend_pie',
                startAngle: data.type == 'sector_pie' ? -90 : 0, // 圆环的开始角度
                endAngle: data.type == 'sector_pie' ? 90 : 360, // 圆环的结束角度
            }

        },
        series: data.series
    });
    return chart
}

function make_area(id, data) {
    let dataLen
    if (data.series.length == 0) {
        dataLen = 0
    } else {
        dataLen = data.series[0].data.length
    }

    var chart = Highcharts.chart({
        chart: {
            renderTo: id,
            type: data.chart,
            zoomType: dataLen > 100 ? 'x' : null
        },
        boost: {
            useGPUTranslations: dataLen > 100
        },
        title: {
            text: data.title
        },
        subtitle: {
            text: data.subtitle
        },
        xAxis: {
            categories: data.categories,
            crosshair: true
        },
        yAxis: {
            title: {
                text: data.yunit
            },
            min: 0
        },
        tooltip: {
            shared: true
        },
        plotOptions: {
            area: {
                stacking: data.type == 'stack_area' ? 'normal' : null,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                },
                dataLabels: {
                    formatter: function() {
                        return data.labelformat == '' ? this.point.y : eval(data.labelformat)
                    }
                }
            },
            series: {
                turboThreshold: dataLen * 10
            }
        },
        series: data.series
    });
    return chart
}

function make_scatter(id, data) {
    let dataLen
    if (data.series.length == 0) {
        dataLen = 0
    } else {
        dataLen = data.series[0].data.length
    }

    var chart = Highcharts.chart({
        chart: {
            renderTo: id,
            type: data.chart,
            zoomType: 'xy'
        },
        boost: {
            useGPUTranslations: dataLen > 1000
        },
        title: {
            text: data.title
        },
        subtitle: {
            text: data.subtitle
        },
        xAxis: {
            title: {
                enabled: true,
                text: data.xunit
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: data.yunit
            }
        },
        tooltip: {
            shared: true
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: data.type == 'bigdata_scatter' ? 0.1 : 4
                },
                dataLabels: {
                    formatter: function() {
                        return data.labelformat == '' ? this.point.y : eval(data.labelformat)
                    }
                }
            }
        },
        series: data.series
    });
    return chart
}