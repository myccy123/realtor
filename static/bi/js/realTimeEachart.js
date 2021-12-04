var first;
function echartWebSocket(url,data,chartSaveStage,rttypeV,id,isClose,theme){
    switch (theme){
        case "e_blue":
            myChart = echarts.init(document.getElementById(id),e_blue);
            break;
        case "e_dark":
            myChart = echarts.init(document.getElementById(id),e_dark);
            break;
        case "e_gray":
            myChart = echarts.init(document.getElementById(id),e_gray);
            break;
        case "e_green":
            myChart = echarts.init(document.getElementById(id),e_green);
            break;
        case "esl":
            myChart = echarts.init(document.getElementById(id),esl);
            break;
        case "e_helianthus":
            myChart = echarts.init(document.getElementById(id),e_helianthus);
            break;
        case "e_infographic":
            myChart = echarts.init(document.getElementById(id),e_infographic);
            break;
        case "e_macarons":
            myChart = echarts.init(document.getElementById(id),e_macarons);
            break;
        default :
            myChart = echarts.init(document.getElementById(id),"");
            break;
    }
    meChart=myChart;//留住myChart
    window.addEventListener("resize",myChart.resize);
    var effectIndex = parseInt(Math.random()*2);
    var effect = [ 'ring' , 'bubble'];

    myChart.showLoading({
        text : '正在加载中...',
        effect : effect[effectIndex],
        textStyle : {
            fontSize : 20
        }
    });

    var Obj= $.parseJSON(data);
    console.log("载体属性：",data,Obj.tmpid,Obj.srcid,Obj.ctype,Obj.timewindow);
    var type=Obj.ctype;
    //未发布多次改动停掉长连接或者事件监听接口isClose强制停掉长连接(不用此接口可以不传)，发布后不停

    if(chartSaveStage=="0"||isClose==true){
        if(first){first.close()}

    }
    var ws;
    ws = new WebSocket('ws://59.110.6.161:9527/real/time/chart');//'ws://59.110.6.161:9527/real/time/chart'
    ws.onopen = function(){  //成功连接到服务器的回调函数
        console.log('成功连接到WS服务器');
        ws.send( '{"chartid":"'+Obj.tmpid+'","srcid":"'+Obj.srcid+'","save":"'+chartSaveStage+'","trtype":"'+rttypeV+'","timewindow":"'+Obj.timewindow+'"}' );
        console.log('客户端发送消息完毕');
        console.log( '{"chartid":"'+Obj.tmpid+'","srcid":"'+Obj.srcid+'","save":"'+chartSaveStage+'","trtype":"'+rttypeV+'","timewindow":"'+Obj.timewindow+'"}');
        first = ws;
    };
    var flag = true;
    ws.onmessage = function(event) {
        console.log('接收到服务器的消息:');
        var JSON = $.parseJSON(event.data);
        console.log(JSON);

        var data2 = $.parseJSON(JSON);
        var chartype ;
        var booleany ;
        //console.log(data2);
        // 增加数组
        function addArray(data2){
            var axisData;
            var tmp = [];
            axisData = (new Date()).toLocaleTimeString();
            for (var i = 0; i < data2.series.length; i++) {
                var d = i;
                var darry = [];
                darry.push(i);
                var data = data2.series[i].data[0];
                darry.push(data);
                darry.push(false);//控制左右，往左
                darry.push(false);

                if (i == data2.series.length - 1) {
                    darry.push(data2.xAxis[0]);
                }
                tmp.push(darry);
            }
            // 动态数据接口 addData
            console.log(tmp)
            //myChart = echarts.init(document.getElementById(id));
           // console.log(myChart)
            myChart.addData(tmp);

        }
        if (type=="polybar1"||type=="polybar2"||type=="polybar3"||type=="polybar4"||type=="polybar5") {
            chartype="bar";
            booleany=true;
        } else if( (type=="polyline1"||type=="polyline2"||type=="polyline3"||type=="polyline4"||type=="polyline5")) {
            chartype="line";
            booleany=false;
        }
        var xdata=[];
        var ydata=[];
        //时间窗口定长
        var timewindowNum=Number(Obj.timewindow)
        if(timewindowNum>0){
            for(var i=0;i<timewindowNum;i++){
                xdata.push("");
                ydata.push(0);
                //console.log(xdata,ydata);
            }
        }

        if(flag){
            if(type=="polyline3"||type=="polybar3"||type=="polybar4"){
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
                    /*dataZoom : {
                     show : true,
                     realtime : true,
                     start : 0,
                     end : 100
                     },*/

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
                                formatter: '{value}'+data2.lyunit
                            },
                            boundaryGap : booleany,
                            data : xdata
                        }
                    ],

                    series:  function(){

                        var serie=[];
                        for( var i=0;i <data2.series.length;i++){
                            var dataStrArr = [];
                            dataStrArr = ydata;
                            dataIntArr = dataStrArr.map(function (data) {
                                return +data;
                            });

                            var item={
                                name:data2.series[i].name,
                                smooth:true,
                                data:dataIntArr,
                                type:chartype//图形类型
                            }
                            if(type=="polybar4"){
                                item. stack='总量';
                            }
                            serie.push(item);
                        };return serie;}()
                }
            }else if(type=="polyline1"||type=="polyline2"||type=="polyline4"||type=="polyline5"||type=="polybar1"||type=="polybar2") {
                var option = {
                    title: {
                        text: data2.title,
                        subtext:data2.subtext
                    },
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        data: data2.yname
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
                    calculable: false,///?
                    /*dataZoom: {
                     show: true,
                     realtime: true,
                     start: 0,
                     end: 100
                     },*/
                    xAxis: [{
                        type: 'category',//?
                        boundaryGap: booleany,
                        axisLabel : {
                            formatter: '{value}'+data2.xunit
                        },
                        data:xdata
                    }],
                    yAxis: [{
                        type: 'value',
                        axisLabel: {
                            formatter: '{value}' + data2.lyunit
                        }
                    }],
                    series: function () {
                        var serie = [];
                        for (var i = 0; i < data2.series.length; i++) {
                            var dataStrArr = [];
                            dataStrArr = ydata;
                            dataIntArr = dataStrArr.map(function (data) {
                                return +data;
                            });
                            // console.info(dataIntArr);
                            var item = {
                                name: data2.series[i].name,
                                smooth:true,
                                data: dataIntArr,
                                type: chartype
                            }
                            if(type=="polyline1"||type=="polybar1"){

                                item.markLine={
                                    data: [
                                        {type: 'average', name: '平均值'}
                                    ]
                                }
                                item.type= chartype;
                                item.areaStyle={normal: {}}
                            };
                            if(type=="polyline2"||type=="polybar2"){
                                item. stack='总量';
                            }
                            if(type=="polyline4"){
                                item. itemStyle={normal: {areaStyle: {type: 'default'}}};
                            }
                            if(type=="polyline5"){
                                item. stack='总量';
                                item. itemStyle={normal: {areaStyle: {type: 'default'}}};
                            }

                            serie.push(item);
                        };
                        return serie;
                    }()
                };
            }else if(type=="polylinebar1"||type=="polylinebar2")
            {
                var option = {
                    title: {
                        text: data2.title,
                        subtext:data2.subtext
                    },
                    tooltip: {
                        trigger: 'item'
                    },
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
                            magicType : {show: true, type: [ 'line','bar', 'stack', 'tiled']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    /* dataZoom : {
                     show : true,
                     realtime : true,
                     start : 0,
                     end : 100
                     },*/
                    calculable: false,///?
                    xAxis: [{
                        type: 'category',//?
                        boundaryGap : true,
                        axisLabel : {
                            formatter: '{value}'+data2.xunit
                        },
                        data:xdata
                    }],
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
                            dataStrArr = ydata;
                            dataIntArr = dataStrArr.map(function (data) {
                                return +data;
                            });
                            // console.info(dataIntArr);
                            var item = {
                                name: data2.series[i].name,
                                smooth:true,
                                data: dataIntArr,
                                type:data2.series[i].type,//图形类型
                                yAxisIndex: data2.series[i].yAxisIndex,
                                areaStyle: {normal: {}}
                            }

                            serie.push(item);
                        };
                        return serie;
                    }()
                };
            }
            console.log(chartype)
            myChart.hideLoading();


            myChart.setOption(option);
            flag = false;
            addArray(data2)
        } else{
            addArray(data2)

        }
    }

    ws.onerror = function(evt)
    {
        console.log("错误信息：",evt);
        //window.location.reload();
        echartWebSocket(url,data,chartSaveStage,rttypeV,id);
        console.log(url,data,chartSaveStage,rttypeV,id);
    };
}