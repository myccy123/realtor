
/*****echart函数*********/
/*function pritCharts(filename,type,id) {
    var chartype;
    var booleany ;
    if (type=="polybar1"||type=="polybar2"||type=="polybar3")
    {chartype="bar";
        booleany=true;
    } else
    {chartype="line";
        booleany=false;
    }
    var myChart = echarts.init(document.getElementById(id));
    /!*window.onresize = function () {
        myChart.resize(); //使第一个图表适应
    }*!/
    window.addEventListener("resize",myChart.resize)
    $.getJSON(filename, function (data2) {

        if(type=="polyline3"||type=="polybar3"){
            var option={
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,
                    y:'center',
                    orient : 'vertical',
                    x:'right'
                },
                toolbox: {
                    show : true,
                    itemSize:12,
                    //orient : 'vertical',
                    x: 'right',
                    y: 'top',
                    feature : {
                        dataView : {show: true, readOnly: false},
                        magicType : {show: true, type: [ 'line','bar', 'stack', 'tiled']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                dataZoom : {
                    show : true,
                    realtime : true,
                    start : 0,
                    end : 100
                },

                xAxis : [
                    {
                        type : 'value',
                        axisLabel : {
                            formatter: '{value}'+ data2.xunit
                        }
                    }
                ],



                yAxis : [
                    {
                        type : 'category',
                        axisLine : {onZero: false},
                        axisLabel : {
                            formatter: '{value}'+data2.yunit
                        },
                        boundaryGap : booleany,
                        data : data2.xAxis
                    }
                ],

                series:  function(){

                    var serie=[];
                    for( var i=0;i <data2.series.length;i++){
                        var item={
                            name:data2.series[i].name,
                            data:data2.series[i].data,
                            type:chartype//图形类型
                        }
                        serie.push(item);
                    };return serie;}()
            };
        }else if(type=="polyline1"||type=="polyline2"||type=="polyline4"||type=="polyline5"||type=="polybar1"||type=="polybar2")
        {
            option = {
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,
                    y:'center',
                    orient: 'vertical',
                    x:'right'
                },
                toolbox: {
                    show: true,
                    itemSize: 12,
                    //orient: 'vertical',
                    x: 'right',
                    y: 'top',
                    feature: {
                        dataView: {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                calculable: true,
                dataZoom: {
                    show: true,
                    realtime: true,
                    start: 0,
                    end: 100
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: booleany,
                    data: data2.xAxis
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {
                        formatter: '{value}' + data2.yunit
                    }
                },

                series:  function(){
                    var serie=[];
                    for( var i=0;i < data2.series.length;i++){
                        var item={
                            name:data2.series[i].name,
                            data:data2.series[i].data,
                            //  stack:data2.series[i].stack, //堆积?//2 5
                            // itemStyle: {normal: {areaStyle: {type: 'default'}}},//面积图///4 5
                            type: chartype//图形类型??????????????????/
                        }
                        if(type=="polyline1"||type=="polybar1"){
                            item.markPoint={
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            }
                            item.markLine={
                                data: [
                                    {type: 'average', name: '平均值'}
                                ]
                            }
                            item.type= chartype;
                            item.areaStyle={normal: {}}
                        };
                        if(type=="polyline2"||type=="polybar2"){
                            item. stack=data2.series[i].stack;
                        }
                        if(type=="polyline4"){
                            item. itemStyle={normal: {areaStyle: {type: 'default'}}};
                        }
                        if(type=="polyline5"){
                            item. stack=data2.series[i].stack;
                            item. itemStyle={normal: {areaStyle: {type: 'default'}}};
                        }
                        serie.push(item);
                    };
                    return serie;
                }()
            };
        }else if(type=="polypie"||type=="polyciclepie")
        {
            option = {
                title : {
                    text: data2.title,
                    subtext: data2.subtext,
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient : 'vertical',
                    x : 'left',
                    y:'top',
                    data:data2.yname
                },
                toolbox: {
                    show : true,
                    feature : {
                        //  mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType : {
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
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series:  function(){
                    var serie=[];
                    var item=  {
                        name:'访问量',
                        type:'pie',
                        center: ['60%', '50%'],
                        itemStyle : {
                            normal : {
                                label : {
                                    show : true,
                                    formatter: '{d}%'
                                    // formatter: '{b} : {c} ({d}%)'
                                },
                                labelLine : {
                                    show : true
                                }
                            },
                            emphasis : {
                                label : {
                                    show : true,
                                    position : 'center',
                                    textStyle : {
                                        fontSize : '10',
                                        fontWeight : 'bold'
                                    }
                                }
                            }
                        },
                        data:data2.data
                    }
                    if(type=="polypie"){
                        item. radius ='55%';
                    }
                    if(type=="polyciclepie"){
                        item. radius =['40%', '60%'];
                    }
                    serie.push(item);
                    return serie;

                }()
            }
        }else if(type=="polylinebar")
        {
            option={
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,
                    y:'center',
                    orient : 'vertical',
                    x:'right'
                },
                toolbox: {
                    show : true,
                    show : true,
                    itemSize:12,
                    //orient : 'vertical',
                    x: 'right',
                    y: 'top',
                    feature : {
                        magicType : {show: true, type: [ 'line','bar', 'stack', 'tiled']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis: {
                    type : 'category',
                    boundaryGap : true,
                    data:data2.xAxis
                },
                yAxis : [
                    {
                        type : 'value',
                        name : data2.ylname,
                        boundaryGap: [0.2, 0.2],
                        min:580,
                        max:650,
                        splitNumber:5,
                        axisLabel : {
                            formatter:  '{value}'+ data2.ylunit
                        }
                    }
                    ,
                    {
                        type : 'value',
                        name : data2.yrname,
                        boundaryGap: [0.2, 0.2],
                        splitNumber:5,
                        axisLabel : {
                            formatter: '{value}'+ data2.yrunit
                        }
                    }
                ],
                series:  function(){

                    var serie=[];
                    for( var i=0;i <data2.series.length;i++){
                        var dataStrArr = [];
                        dataStrArr =data2.series[i].data;
                        dataIntArr=dataStrArr.map(function(data){
                            return +data;
                        });
                        console.info(dataIntArr);
                        var item={
                            name:data2.series[i].name,
                            data:dataIntArr,
                            type:data2.series[i].type,//图形类型
                            yAxisIndex: data2.series[i].yAxisIndex,
                            areaStyle: {normal: {}}
                        }
                        serie.push(item);
                    };
                    return serie;}()
            };
        }
        myChart.setOption(option);
    });
}*///4icon_top
function pritCharts(filename,type,id) {
    var chartype;
    var booleany ;
    if (type=="polybar1"||type=="polybar2"||type=="polybar3")
    {chartype="bar";
        booleany=true;
    } else
    {chartype="line";
        booleany=false;
    }
    var myChart = echarts.init(document.getElementById(id));
    window.addEventListener("resize",myChart.resize);
    $.getJSON(filename, function (data2) {

        if(type=="polyline3"||type=="polybar3"){
            var option={
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,x:'right',orient : 'vertical'
                },
                toolbox: {
                    show : true,
                    itemSize:12,
                    orient : 'vertical',
                    x: 'right',
                    y: 'center',
                    feature : {
                        dataView : {show: true, readOnly: false},
                        magicType : {show: true, type: [ 'line','bar', 'stack', 'tiled']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                dataZoom : {
                    show : true,
                    realtime : true,
                    start : 0,
                    end : 100
                },

                xAxis : [
                    {
                        type : 'value',
                        axisLabel : {
                            formatter: '{value}'+ data2.xunit
                        }
                    }
                ],



                yAxis : [
                    {
                        type : 'category',
                        axisLine : {onZero: false},
                        axisLabel : {
                            formatter: '{value}'+data2.yunit
                        },
                        boundaryGap : booleany,
                        data : data2.xAxis
                    }
                ],

                series:  function(){

                    var serie=[];
                    for( var i=0;i <data2.series.length;i++){
                        var item={
                            name:data2.series[i].name,
                            data:data2.series[i].data,
                            type:chartype//图形类型
                        }
                        serie.push(item);
                    };return serie;}()
            };
        }else if(type=="polyline1"||type=="polyline2"||type=="polyline4"||type=="polyline5"||type=="polybar1"||type=="polybar2")
        {
            option = {
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,x:'right',orient : 'vertical'
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
                dataZoom: {
                    show: true,
                    realtime: true,
                    start: 0,
                    end: 100
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: booleany,
                    data: data2.xAxis
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {
                        formatter: '{value}' + data2.yunit
                    }
                },

                series:  function(){
                    var serie=[];
                    for( var i=0;i < data2.series.length;i++){
                        var item={
                            name:data2.series[i].name,
                            data:data2.series[i].data,
                            //  stack:data2.series[i].stack, //堆积?//2 5
                            // itemStyle: {normal: {areaStyle: {type: 'default'}}},//面积图///4 5
                            type: chartype//图形类型??????????????????/
                        }
                        if(type=="polyline1"||type=="polybar1"){
                            item.markPoint={
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            }
                            item.markLine={
                                data: [
                                    {type: 'average', name: '平均值'}
                                ]
                            }
                            item.type= chartype;
                            item.areaStyle={normal: {}}
                        };
                        if(type=="polyline2"||type=="polybar2"){
                            item. stack=data2.series[i].stack;
                        }
                        if(type=="polyline4"){
                            item. itemStyle={normal: {areaStyle: {type: 'default'}}};
                        }
                        if(type=="polyline5"){
                            item. stack=data2.series[i].stack;
                            item. itemStyle={normal: {areaStyle: {type: 'default'}}};
                        }
                        serie.push(item);
                    };
                    return serie;
                }()
            };
        }else if(type=="polypie"||type=="polyciclepie")
        {
            option = {
                title : {
                    text: data2.title,
                    subtext: data2.subtext,
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient : 'vertical',
                    x : 'left',
                    // y:'top',
                    data:data2.yname
                },
                toolbox: {
                    show : true,
                    feature : {
                        //  mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType : {
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
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series:  function(){
                    var serie=[];
                    var item=  {
                        name:'访问量',
                        type:'pie',
                        center: ['60%', '50%'],
                        itemStyle : {
                            normal : {
                                label : {
                                    show : true,
                                    formatter: '{d}%'
                                    // formatter: '{b} : {c} ({d}%)'
                                },
                                labelLine : {
                                    show : true
                                }
                            },
                            emphasis : {
                                label : {
                                    show : true,
                                    position : 'center',
                                    textStyle : {
                                        fontSize : '10',
                                        fontWeight : 'bold'
                                    }
                                }
                            }
                        },
                        data:data2.data
                    }
                    if(type=="polypie"){
                        item. radius ='55%';
                    }
                    if(type=="polyciclepie"){
                        item. radius =['40%', '60%'];
                    }
                    serie.push(item);
                    return serie;

                }()
            }
        }else if(type=="polylinebar")
        {
            option={
                title: {
                    text: data2.title,
                    subtext: data2.subtext
                },
                tooltip: {},
                legend: {
                    data: data2.yname,x:'right',orient : 'vertical'
                },
                toolbox: {
                    show : true,
                    show : true,
                    itemSize:12,
                    orient : 'vertical',
                    x: 'right',
                    y: 'center',
                    feature : {
                        magicType : {show: true, type: [ 'line','bar', 'stack', 'tiled']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis: {
                    type : 'category',
                    boundaryGap : true,
                    data:data2.xAxis
                },
                yAxis : [
                    {
                        type : 'value',
                        name : data2.ylname,
                        boundaryGap: [0.2, 0.2],
                        min:580,
                        max:650,
                        splitNumber:5,
                        axisLabel : {
                            formatter:  '{value}'+ data2.ylunit
                        }
                    }
                    ,
                    {
                        type : 'value',
                        name : data2.yrname,
                        boundaryGap: [0.2, 0.2],
                        splitNumber:5,
                        axisLabel : {
                            formatter: '{value}'+ data2.yrunit
                        }
                    }
                ],
                series:  function(){

                    var serie=[];
                    for( var i=0;i <data2.series.length;i++){
                        var dataStrArr = [];
                        dataStrArr =data2.series[i].data;
                        dataIntArr=dataStrArr.map(function(data){
                            return +data;
                        });
                        console.info(dataIntArr);
                        var item={
                            name:data2.series[i].name,
                            data:dataIntArr,
                            type:data2.series[i].type,//图形类型
                            yAxisIndex: data2.series[i].yAxisIndex,
                            areaStyle: {normal: {}}
                        }
                        serie.push(item);
                    };
                    return serie;}()
            };
        }
        myChart.setOption(option);
    });
}

$(document).ready(function(){
    if($("body").attr("id")=="page2"){
        pritCharts("http://www.realtoraccess.com/data/chartdata/cpu.txt","polybar1","test202");
        pritCharts("http://www.realtoraccess.com/data/chartdata/network.txt","polyline1","test201");
        pritCharts("http://www.realtoraccess.com/data/chartdata/sysres.txt","polybar3","test203");
        pritCharts("http://www.realtoraccess.com/data/chartdata/datacnt.txt","polyline4","test204");
    }
    if($("body").attr("id")=="page3"){
        pritCharts("http://www.realtoraccess.com/data/chartdata/network.txt","polybar1","test301");
        pritCharts("http://www.realtoraccess.com/data/chartdata/err.txt","polyline1","test302");
        pritCharts("http://www.realtoraccess.com/data/chartdata/mem.txt","polyline4","test303");
    }
    if($("body").attr("id")=="page1"){
        pritCharts("http://www.realtoraccess.com/data/chartdata/err.txt","polyline1","test102");
        pritCharts("http://www.realtoraccess.com/data/chartdata/mem.txt","polybar2","test103");
        pritCharts("http://www.realtoraccess.com/data/chartdata/cpu.txt","polyline1","test104");
        pritCharts("http://www.realtoraccess.com/data/chartdata/network.txt","polyline5","test101");
        pritCharts("http://www.realtoraccess.com/data/chartdata/sysres.txt","polybar3","test105");
        pritCharts("http://www.realtoraccess.com/data/chartdata/datacnt.txt","polyline4","test106");
    }

});
if($("body").attr("id")!=="page3"){
    var pageDrag;
    var pageDrop;
    $("#allsvg div").on("dragstart",function(e){
        console.log($(this))
        pageDrag=$(this);

    })
    $("#allsvg div").on("dragover",function(e){
        e.preventDefault();
        $(this);
        pageDrop=$(this);
    })
    $("#allsvg div").on("drop",function(e){
        $(this).insertAfter(pageDrag);

    })
}
if($("body").attr("id")=="page3"){
    var pageDrag3;
    var pageDrag3Id;
    var pageDrop3Id;
    var pageDrop3;
    $("#allsvg1 div").on("dragstart",function(e){
        console.log($(this))
        pageDrag=$(this).clone();
        console.log(pageDrag)
        console.log($(this).clone())

    })
    $("#allsvg1 div").on("dragover",function(e){
        e.preventDefault();
        //console.log($(this))
        pageDrop=$(this);

        console.log( $(e.target))
    })
    $("#allsvg1 div").on("drop",function(e){
        //$(this).html(pageDrag);
        //pageDrag.html(pageDrop3)

    })}

