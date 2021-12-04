function initChart(hId,divId,height,dataObj,chartSaveStage,isClose){
                /*编号，id名(没有#),高度，筛选对象，是否保存（1保存，0不保存），是否关闭(true,false)*/
    $.get("http://www.realtoraccess.com/bi/get/div?id="+hId+"&Mstatus=0",function (data){

        $("#"+divId).html(data);
        var newid=hId;
        $('[draggable="true"]').each(function(){
            var jdata=$(this).attr("data-data");
            var jctype=$(this).attr("data-ctype");
            $(this).attr("id",divId+hId+newid+"00");

            var rttype = $(this).attr("data-rttype");
            var chartid = $(this).attr("data-chartid");

            var srcid = $(this).attr("data-srcid");
            var boxID=$(this).attr("id");
            var wrapurl = $(this).attr("data-wrapurl");
            var timewindow=$(this).attr("data-timewindow");
            var theme=$(this).attr("data-theme");
            if(!theme){
                theme=""
            }


            $(this).css("height",height+"px");
            $(this).css("width","100%");
            $(this).children().children().children().css("width","100%");
            $(this).children().css({"width":"100%","position":"relative","overflow":"hidden", "height": height+"px"});
            $("#sys_show_explain").fadeIn();
            $("#sys_chart_dre0").css("display","none");
            $(this).attr("draggable","false");
            newid++;
            if(jctype=="panel1"||jctype=="panel2"||jctype=="panel3"){
                IntervalEchart(wrapurl,jctype, boxID,5000,chartSaveStage,theme);
            }else if(rttype=="rtline") {
                data=  '{"srcid": "'+srcid+'",' +
                    '"ctype": "'+jctype+'",' +
                    '"tmpid": "'+chartid+'",' +
                    '"rttype": "'+rttype+'",' +
                    '"timewindow":'+timewindow+
                    '}'
                echartWebSocket('ws://127.0.0.1:9527/real/time/chart', data, 1, "rtline", boxID,isClose,theme);
            }else{
                dataObj.chartid=chartid;

                initEchartNormal(dataObj, jctype, boxID,theme);
            }
        })
    })
}
