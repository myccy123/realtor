/*仪表盘实时*/
var timer;
function IntervalEchart(panelURL,type,id,stime,i,theme){
    $("#echart>img").css("display","none");
    $("#loadechart").css("display","block");
    $("#polyline_form").css("display","block");
    console.log(myChart)
    var myChart
    if(myChart){
        myChart=null;
    }

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
    if(timer){
        console.log()
        clearInterval(timer);
        timer=null;
    }
    //console.log(panelURL);
    //console.log(ctype);
    if(type=="panel1"){
        panel1();
         timer=setInterval(panel1,stime);
    }else if(type=="panel2"){
        panel2();
          timer=setInterval(panel2,stime);
    }else if(type=="panel3"){
        panel3();
          timer=setInterval(panel3,stime);
    }

    function panel1(){
        $.get(panelURL,{"publish":i},function(data2){
            var effectIndex = parseInt(Math.random()*2);
            var effect = [ 'ring' , 'bubble','spin'];//effect = ['spin' , 'bar' , 'ring' , 'whirling' , 'dynamicLine' , 'bubble'];
            myChart.showLoading({
                text :'正在加载中...',
                effect : effect[effectIndex],
                textStyle : {
                    fontSize : 20
                }
            })

            //console.log(data2);
            var data2= $.parseJSON(data2);
            //console.log(data2);
            //filepath= filepathObj.data+"";
            //console.log(filepath);

            //console.log(ctype);

                //console.log(data2);
                var dataINV=data2.data.data[0].value;
            //console.log(dataINV)
                var option = {
                    title: {
                        text: data2.data.title,
                        subtext: data2.data.subtext
                    },
                    tooltip : {
                        formatter: "{a} <br/>{b} : {c}"+data2.data.unit
                    },
                    toolbox: {
                        show : true,
                        itemSize: 12,
                        orient: 'vertical',
                        x: 'right',
                        y: 'center',
                        feature : {
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    series : [
                        {
                            name:'业务指标',
                            type:'gauge',
                            axisLine: {            // 坐标轴线
                                lineStyle: {       // 属性lineStyle控制线条样式
                                    color: [[data2.data.colordata1, '#228b22'],[data2.data.colordata2, '#48b'],[data2.data.colordata3, '#ff4500']]

                                }
                            },
                           detail :{formatter:'{value}'+data2.data.unit},
                            data:data2.data.data
                        }
                    ]
                };
            //console.log(data2.data.data);



                option.series[0].data[0].value = dataINV ;
                
                myChart.setOption(option);
		myChart.hideLoading();


        })
    }
    function panel2(){
        $.get(panelURL,{"publish":i},function(data2){
            var effectIndex = parseInt(Math.random()*2);
            var effect = [ 'ring' , 'bubble','spin'];//effect = ['spin' , 'bar' , 'ring' , 'whirling' , 'dynamicLine' , 'bubble'];
            myChart.showLoading({
                text : '正在加载中...',
                effect : effect[effectIndex],
                textStyle : {
                    fontSize : 20
                }
            })
            var data2= $.parseJSON(data2);

                //console.log(data2);
                var dataINV=data2.data.data[0].value;
                var option = {
                    title: {
                        text: data2.data.title,
                        subtext: data2.data.subtext
                    },
                    tooltip : {
                        formatter: "{a} <br/>{b} : {c}"+data2.data.unit
                    },
                    toolbox: {
                        show : true,
                        itemSize: 12,
                        orient: 'vertical',
                        x: 'right',
                        y: 'center',
                        feature : {
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    series : [
                        {
                            name:'业务指标',
                            type:'gauge',
                            splitNumber: 10,       // 分割段数，默认为5
                            axisLine: {            // 坐标轴线
                                lineStyle: {       // 属性lineStyle控制线条样式
                                    color: [[data2.data.colordata1, '#228b22'],[data2.data.colordata2, '#48b'],[data2.data.colordata3, '#ff4500']],
                                    //color: [[0.2, '#228b22'],[0.8, '#48b'],[1, '#ff4500']],

                                    width: 8
                                }
                            },
                            axisTick: {            // 坐标轴小标记
                                splitNumber: 10,   // 每份split细分多少段
                                length :12,        // 属性length控制线长
                                lineStyle: {       // 属性lineStyle控制线条样式
                                    color: 'auto'
                                }
                            },
                            axisLabel: {           // 坐标轴文本标签，详见axis.axisLabel
                                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                                    color: 'auto'
                                }
                            },
                            splitLine: {           // 分隔线
                                show: true,        // 默认显示，属性show控制显示与否
                                length :20,         // 属性length控制线长
                                lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                                    color: 'auto'
                                }
                            },
                            pointer : {
                                width : 5
                            },
                            title : {
                                show : true,
                                offsetCenter: [0, '-40%'],       // x, y，单位px
                                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                                    fontWeight: 'bolder'
                                }
                            },
                            detail : {
                                formatter:'{value}'+data2.data.unit,
                                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                                    color: 'auto',
                                    fontWeight: 'bolder'
                                }
                            },
                            data:data2.data.data
                        }
                    ]
                };

                option.series[0].data[0].value =  dataINV;
                
                myChart.setOption(option);
		        myChart.hideLoading();


        })
    }

}