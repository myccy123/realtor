function pritCharts(filename, type, id, theme) {
    //console.log(filename)
    var chartype;
    var booleany;
    var myChart;
    var option;
    if (type == "polybar1" || type == "polybar2" || type == "polybar3" || type == "polybar4" || type == "polybar5") {
        chartype = "bar";
        booleany = true;
    } else if ((type == "polyline1" || type == "polyline2" || type == "polyline3" || type == "polyline4" || type == "polyline5")) {
        chartype = "line";
        booleany = false;
    }
    switch (theme) {
        case "e_blue":
            myChart = echarts.init(document.getElementById(id), e_blue);
            break;
        case "e_dark":
            myChart = echarts.init(document.getElementById(id), e_dark);
            break;
        case "e_gray":
            myChart = echarts.init(document.getElementById(id), e_gray);
            break;
        case "e_green":
            myChart = echarts.init(document.getElementById(id), e_green);
            break;
        case "esl":
            myChart = echarts.init(document.getElementById(id), esl);
            break;
        case "e_helianthus":
            myChart = echarts.init(document.getElementById(id), e_helianthus);
            break;
        case "e_infographic":
            myChart = echarts.init(document.getElementById(id), e_infographic);
            break;
        case "e_macarons":
            myChart = echarts.init(document.getElementById(id), e_macarons);
            break;
        default :
            myChart = echarts.init(document.getElementById(id), "");
            break;
    }
    meChart = myChart;//留住myChart
    window.addEventListener("resize", myChart.resize);
    var effectIndex = parseInt(Math.random() * 2);
    var effect = ['ring', 'bubble', 'spin'];//effect = ['spin' , 'bar' , 'ring' , 'whirling' , 'dynamicLine' , 'bubble'];
    myChart.showLoading({
        text: '正在加载中...',
        effect: effect[effectIndex],
        textStyle: {
            fontSize: 20
        }
    });
    $.getJSON(filename, function (data2) {
        //console.log(data2)

        if (type == "polyline3" || type == "polybar3" || type == "polybar4") {
            option = {
                title: {
                    text: data2.title,
                    subtext: data2.subtext,
                },
                tooltip: {},
                legend: {
                    data: data2.yname,
                    x: 'center',
                    y: 'bottom',
                    /*orient : 'vertical'*/
                },
                toolbox: {
                    show: true,
                    itemSize: 12,
                    orient: 'vertical',
                    x: 'right',
                    y: 'center',
                    feature: {
                        dataView: {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                grid: {
                    containLabel: true,
                },
                calculable: true,
                /*dataZoom : {
                 show : true,
                 realtime : true,
                 start : 0,
                 end : 100
                 },*/

                xAxis: [
                    {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value}' + data2.xunit
                        }
                    }
                ],


                yAxis: [
                    {
                        
                        type: 'category',
                        axisLine: {onZero: false},
                        axisLabel: {
                            formatter: '{value}' + data2.lyunit
                        },
                        boundaryGap: booleany,
                        data: data2.xAxis
                    }
                ],

                series: function () {

                    var serie = [];
                    for (var i = 0; i < data2.series.length; i++) {
                        var item = {
                            name: data2.series[i].name,
                            smooth: true,
                            data: data2.series[i].data,
                            type: chartype//图形类型
                        }
                        if (type == "polybar4") {
                            item.stack = '总量';
                        }
                        serie.push(item);
                    }
                    ;
                    return serie;
                }()
            };
        } else if (type == "polyline1" || type == "polyline2" || type == "polyline4" || type == "polyline5" || type == "polybar1" || type == "polybar2") {
            option = {
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,
                    x: 'center',
                    y: 'bottom',
                    /*orient : 'vertical'*/
                },
                grid: {
                    containLabel: true,
                },
                toolbox: {
                    show: true,
                    itemSize: 12,
                    orient: 'vertical',
                    x: 'right',
                    y: 'center',
                    feature: {
                        dataView: {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                calculable: true,
                /*dataZoom: {
                 show: true,
                 realtime: true,
                 start: 0,
                 end: 100
                 },*/
                xAxis: {
                    type: 'category',
                    boundaryGap: booleany,
                    axisLabel: {
                        formatter: '{value}' + data2.xunit
                    },
                    data: data2.xAxis
                },
                yAxis: {
                    name:data2.lyunit,
                    type: 'value',
                    axisLabel: {
                        formatter: '{value}'  // + data2.lyunit
                    }
                },

                series: function () {
                    var serie = [];
                    for (var i = 0; i < data2.series.length; i++) {
                        var item = {
                            name: data2.series[i].name,
                            smooth: true,
                            data: data2.series[i].data,
                            //  stack:data2.series[i].stack, //堆积?//2 5
                            // itemStyle: {normal: {areaStyle: {type: 'default'}}},//面积图///4 5
                            type: chartype//图形类型??????????????????/
                        }
                        if (type == "polyline1" || type == "polybar1") {

                            item.markLine = {
                                data: [
                                    {type: 'average', name: '平均值'}
                                ]
                            }
                            item.type = chartype;
                            //item.areaStyle = {normal: {}}
                        }
                        ;
                        if (type == "polyline2" || type == "polybar2") {
                            item.stack = "总量";
                            // item.areaStyle = {normal: {}}
                        }
                        if (type == "polyline4") {
                            item.itemStyle = {normal: {areaStyle: {type: 'default'}}};
                        }
                        if (type == "polyline5") {
                            item.stack = "总量"//;data2.series[i].stack//
                            item.itemStyle = {normal: {areaStyle: {type: 'default'}}};
                        }
                        serie.push(item);
                    }
                    ;
                    return serie;
                }()
            };
        } else if (type == "pie" || type == "circlepie") {
            option = {
                title: {
                    text: data2.title,
                    subtext: data2.subtext,
                    x: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c}" + data2.lyunit + " ({d}%)"
                },
                legend: {
                    //orient : 'vertical',
                    //x : 'left',
                    y: 'bottom',
                    data: data2.yname
                },
                toolbox: {
                    show: true,
                    itemSize: 12,
                    orient: 'vertical',
                    x: 'right',
                    y: 'center',
                    feature: {
                        //  mark : {show: true},
                        dataView: {show: true, readOnly: false},
                        magicType: {
                            show: true,
                            type: ['pie', 'funnel'],
                            option: {
                                funnel: {
                                    x: '25%',
                                    width: '50%',
                                    funnelAlign: 'left',
                                    max: 1548
                                }
                            }
                        },
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                calculable: true,
                series: function () {
                    var serie = [];
                    var item = {
                        name: data2.data[0].seriesname,
                        smooth: true,
                        type: 'pie',
                        center: ['50%', '50%'],
                        itemStyle: {
                            normal: {
                                label: {
                                    show: false,
                                    formatter: '{d}%'
                                    // formatter: '{b} : {c} ({d}%)'
                                },
                                labelLine: {
                                    show: false
                                }
                            },
                            emphasis: {
                                label: {
                                    show: true,
                                    position: 'center',
                                    textStyle: {
                                        fontSize: '10',
                                        fontWeight: 'bold'
                                    }
                                }
                            }
                        },
                        data: data2.data
                    }

                    if (type == "pie") {
                        item.radius = '55%';
                    }
                    if (type == "circlepie") {
                        item.radius = ['40%', '60%'];
                    }
                    serie.push(item);
                    return serie;

                }()
            }
        } else if (type == "polylinebar1" ) {
            option = {
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,
                    x: 'center',
                    y: 'bottom',
                    /*orient : 'vertical'*/
                },
                grid: {
                    containLabel: true,
                },
                toolbox: {

                    show: true,
                    itemSize: 12,
                    orient: 'vertical',
                    x: 'right',
                    y: 'center',
                    feature: {
                        magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                calculable: true,
                /*dataZoom : {
                 show : true,
                 realtime : true,
                 start : 0,
                 end : 100
                 },*/
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    axisLabel: {
                        formatter: '{value}' + data2.xunit
                    },
                    data: data2.xAxis
                },

                yAxis: [
                    {
                        type : 'value',
                        name : data2.ylname,
                        boundaryGap: [0.2, 0.2],
                        min:"auto",
                        max:"auto",
                        splitNumber:5,
                        axisLabel : {
                            formatter:  '{value}'+ data2.lyunit//左y轴单位
                        }
                    }

                ],
                series: function () {

                    var serie = [];
                    for (var i = 0; i < data2.series.length; i++) {
                        var dataStrArr = [];
                        dataStrArr = data2.series[i].data;
                        dataIntArr = dataStrArr.map(function (data) {
                            return +data;
                        });

                        var item = {
                            name: data2.series[i].name,
                            smooth: true,
                            data: dataIntArr,
                            type: data2.series[i].type,//图形类型
                            yAxisIndex:data2.series[i].yAxisIndex,
                            //areaStyle: {normal: {}}
                        }
                        serie.push(item);
                    }
                    ;
                    return serie;
                }()
            };
        } else if (type == "polylinebar2") {
            option = {
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,
                    x: 'center',
                    y: 'bottom',
                    /*orient : 'vertical'*/
                },
                grid: {
                    containLabel: true,
                },
                toolbox: {

                    show: true,
                    itemSize: 12,
                    orient: 'vertical',
                    x: 'right',
                    y: 'center',
                    feature: {
                        magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                calculable: true,
                /*dataZoom : {
                 show : true,
                 realtime : true,
                 start : 0,
                 end : 100
                 },*/
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    axisLabel: {
                        formatter: '{value}' + data2.xunit
                    },
                    data: data2.xAxis
                },

                yAxis: [
                    {
                        type : 'value',
                        name : data2.ylname,
                        boundaryGap: [0.2, 0.2],
                        min:"auto",
                        max:"auto",
                        splitNumber:5,
                        axisLabel : {
                            formatter:  '{value}'+ data2.lyunit//左y轴单位
                        }
                    }
                    ,
                    {
                        type : 'value',
                        name : data2.yrname,
                        boundaryGap: [0.2, 0.2],
                        splitNumber:5,
                        axisLabel : {
                            formatter: '{value}'+ data2.ryunit//右y轴单位
                        }
                    }
                ],
                series: function () {

                    var serie = [];
                    for (var i = 0; i < data2.series.length; i++) {
                        var dataStrArr = [];
                        dataStrArr = data2.series[i].data;
                        dataIntArr = dataStrArr.map(function (data) {
                            return +data;
                        });

                        var item = {
                            name: data2.series[i].name,
                            smooth: true,
                            data: dataIntArr,
                            type: data2.series[i].type,//图形类型
                            yAxisIndex:data2.series[i].yAxisIndex,
                            //areaStyle: {normal: {}}
                        }
                        serie.push(item);
                    }
                    ;
                    return serie;
                }()
            };
        } else if (type == "map") {
            option = {
                // backgroundColor: '#1b1b1b',
                // color: ['gold','aqua','lime'],
                title: {
                    text: data2.title,
                    subtext: data2.subtext,
                    sublink: '',
                    x: 'center'
                },
                tooltip: {
                    trigger: 'item'

                },
                legend: {
                    orient: 'vertical',
                    x: 'left',
                    data: data2.dataname,
                },
                dataRange: {
                    min: 0,
                    max: data2.dataRangemax,
                    calculable: true,
                    color: ['maroon', 'purple', 'red', 'orange', 'yellow', 'lightgreen']
                },
                toolbox: {
                    show: true,
                    orient: 'vertical',
                    x: 'right',
                    y: 'center',
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },

                series: [
                    {
                        name: data2.dataname,
                        type: 'map',

                        mapType: 'china',
                        hoverable: false,
                        roam: true,
                        itemStyle: {

                            normal: {
                                borderColor: '#87cefa',
                                borderWidth: 1           // 标注边线线宽，单位px，默认为1
                                // color: '#1b1b1b',


                            }
                        },
                        data: [],
                        markPoint: {
                            symbolSize: 5,       // 标注大小，半宽（半径）参数，当图形为方向或菱形则总宽度为symbolSize * 2
                            //  selectedMode: 'multiple',
                            itemStyle: {
                                normal: {
                                    borderColor: '#87cefa',
                                    borderWidth: 1,            // 标注边线线宽，单位px，默认为1
                                    // color: '#1b1b1b',
                                    label: {
                                        show: false
                                    }
                                },
                                emphasis: {
                                    borderColor: '#1e90ff',
                                    borderWidth: 5,
                                    label: {
                                        show: false
                                    }
                                }
                            },
                            data: data2.series
                        },

                        geoCoord: data2.seriesname
                    },
                    {
                        name: 'Top5',

                        type: 'map',
                        mapType: 'china',
                        data: [],
                        markPoint: {
                            symbol: 'emptyCircle',
                            symbolSize: function (v) {
                                return 10 + v / 100
                            },
                            effect: {
                                show: true,
                                shadowBlur: 0
                            },
                            itemStyle: {
                                normal: {
                                    label: {show: false}
                                }
                            },
                            data: data2.series1
                        }
                    }
                ]
            }
        } else if (type == "hotmap") {
            var hours = data2.xAxis;
            var days = data2.yname;
            var data = data2.series;
            data = data.map(function (item) {
                return [item[1], item[0], item[2] || '-'];
            });

            option = {
                title: {
                    text: data2.title,
                    subtext: data2.subtext,
                    left: 'center'
                },
                //backgroundColor: '#404a59',
                tooltip: {
                    position: 'top'
                },
                animation: false,
                /* grid: {
                 top: "middle"
                 },*/
                xAxis: {
                    type: 'category',
                    data: hours,
                    splitArea: {
                        show: true
                    }
                },
                yAxis: {
                    type: 'category',
                    data: days,
                    splitArea: {
                        show: true
                    }
                },
                visualMap: {
                    type: 'piecewise',
                    left: 'right',
                    //top:'bottom',
                    bottom: '20%',
                    pieces: [
                        /*{value: 0, label: '离线', color: '#DDDDDD'},
                         {min: 1, max: 49, label: '优', color: '#46CE16'},
                         {min: 50, max: 99, label: '良', color: '#EFDC34'},
                         {min: 100, max: 199, label: '轻度污染', color: '#FFAA00'},
                         {min: 200, max: 299, label: '中度污染', color: '#FF431A'},
                         {min: 300, max: 499, label: '重度污染', color: '#D20043'},
                         {min: 500, label: '严重污染', color: '#9C0950'}*/
                    ],

                },
                series: [{
                    name: data2.dataname,
                    type: 'heatmap',
                    data: data,
                    label: {
                        normal: {
                            show: false
                        }
                    },
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }]
            };
            /*自定义区区间*/
            if(dataObj.hotRank){
                for(var key in dataObj.hotRank){
                    if( Number(key)<dataObj.hotRank.length-1){
                        option.visualMap.pieces[key]={
                            min: dataObj.hotRank[key].Clow,
                            max: dataObj.hotRank[key].Chigh,
                            label: dataObj.hotRank[key].idx_type,
                            color: dataObj.colorList[key]
                        };
                    }else{
                        option.visualMap.pieces.push({
                            min: dataObj.hotRank[key].Clow,
                            /*max: (dataObj.hotRank.length-1).Chigh,*/
                            label: dataObj.hotRank[key].idx_type,
                            color: dataObj.colorList[key]
                        })
                    }
                }
                if(dataObj.initObj){
                    option.visualMap.pieces.unshift(dataObj.initObj);
                }

            }
        }


        myChart.setOption(option);
        myChart.hideLoading();
    });
}