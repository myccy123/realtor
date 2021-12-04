/**
 * Created by lenovo on 2016/12/2.
 */
/****************************detail.html***********************************/



/**************************左边图标栏，icon图标切换,图表区界面切换 ******************************/
$("#chart_lit_img").click(function(e){
    idmun=0;//select id 归零
    classNameNum=0;
    clearInterval(timer);
    timer=null;
    if($(e.target).is("span")){

        $(e.target).parent("p").siblings().removeClass("detail_icon_hover");
        $(e.target).parent("p").addClass("detail_icon_hover");
        var targetname=$(e.target).attr("data-num");

        $('#'+targetname+'_imgbox').siblings().css("display","none");
        $('#'+targetname+'_imgbox').css("display","block");
        $("#detail_show_select_img_box img").removeClass("detail_type_img_hover");
        $('#'+targetname+'_imgbox').children("div:first").children("img").addClass("detail_type_img_hover");

        imgV=$('#'+targetname+'_imgbox .detail_type_img_hover').attr("data-type");

        switch ($('#'+targetname+'_imgbox').attr("id")){
            case "chart1_imgbox":
            case "chart2_imgbox":
            case "chart3_imgbox":

                $("#detail_show_form").load("http://www.realtoraccess.com/static/bi/detail_line_bar.html");
                clearInterval(timer);
                appendChartOption();

                break;
            case "chart4_imgbox":
                $("#detail_show_form").load("http://www.realtoraccess.com/static/bi/detail_linebar_left.html");
                clearInterval(timer);
                appendChartOption()//增加detail页面selcet生成option

                break;
            case "chart5_imgbox":

                $("#detail_show_form").load("http://www.realtoraccess.com/static/bi/detail_pie.html");
                clearInterval(timer);
                appendChartOption()
                //dataSource("http://www.realtoraccess.com/get/tabofdb/",{"db":"visio_pie"});//增加detail页面selcet生成option

                break;
            case "chart6_imgbox":
                $("#detail_show_form").load("http://www.realtoraccess.com/static/bi/detail_pie_panel_map.html");
                clearInterval(timer);
                dataSource("http://www.realtoraccess.com/get/tabofdb/",{"db":"visio_map"});
                break;
            case "chart7_imgbox":
                $("#detail_show_form").load("http://www.realtoraccess.com/static/bi/detail_pie_panel_map.html");
                clearInterval(timer);
                dataSource("http://www.realtoraccess.com/get/tabofdb/",{"db":"visio_dashboard"});
                break;
            case "chart9_imgbox":

                $("#detail_show_form").load("http://www.realtoraccess.com/static/bi/detail_heat_map.html");
                appendChartOption()
                clearInterval(timer);

            default :
                clearInterval(timer);
                timer=null;
        }
    }
})


/**************************图表样式选中  蓝框click（监控图表类型变化)******************************/
var imgV="polyline1";
$("#detail_show_select_img_box img").click(function(e){
    $("#detail_show_select_img_box img").removeClass("detail_type_img_hover");
    $(e.target).addClass("detail_type_img_hover");
    chartSaveStage=0;//保存状态归零
    /*判断图类型函数（data-type）*****/
    switch ( $(e.target).attr("data-type")){
        case "polylinebar2":
            clearInterval(timer);
            $("#detail_show_form").load("http://www.realtoraccess.com/static/bi/detail_linebar_all.html");
            appendChartOption();//增加detail页面selcet生成option
            idmun=2;//select id 归1
            classNameNum=0;
            detailChartPost("http://www.realtoraccess.com/bi/conf/makelinedata/",e);
            break;
        case "polylinebar1":
            clearInterval(timer);
            $("#detail_show_form").load("http://www.realtoraccess.com/static/bi/detail_linebar_left.html");
            appendChartOption();//增加detail页面selcet生成option
            idmun=0;//select id 归零
            classNameNum=0;
            detailChartPost("http://www.realtoraccess.com/bi/conf/makelinedata/",e);

            break;

        case "circlepie":
        case "pie":
            clearInterval(timer);
            appendChartOption();
            //detailChartPost("http://www.realtoraccess.com/config/makepiedata/",e);

            break;
        case "map":
            clearInterval(timer);
            detailChartPost("http://www.realtoraccess.com/bi/conf/makemapdata/",e);

            break;

        case "panel1":
        case "panel2":
        case "panel3":

            detailChartPost("http://www.realtoraccess.com/bi/conf/makedashboarddata/",e);

            break;
        case "hotmap":
            clearInterval(timer);
            detailChartPost("http://www.realtoraccess.com/bi/conf/makethermodynamicdata/",e);
            break;

        default :
            clearInterval(timer);
            detailChartPost("http://www.realtoraccess.com/bi/conf/makelinedata/",e);


    }


})


/**************************detail页面  change (detail全页面监控所有变化)******************************/
$("#detail").change(function(e){
    chartSaveStage=0;//保存状态归零
    changChooseURL(e);
    saveIsDisabled();
    //recordSourceOpition()

})
//记录用户选择OPTION
$("#detail").delegate(".deatil_sel_checked","change",function(){
    recordSourceOpition();
})
//保存btn是否禁用；
function saveIsDisabled(){
    var $save=$("#detail").find($("#detail_chart_sv"));
    if(($("#detail").find($("#polyline_maintitle"))).val()!==""){
        $save.removeAttr("disabled");
    }else if(($("#detail").find($("#polyline_maintitle"))).val()==""){
        $save.attr("disabled","disabled");
    }
}
//URL分配；
function changChooseURL(e){
    clearInterval(timer);
    switch ( $(".detail_type_img_hover").attr("data-type")){
        case "polylinebar2":

            detailChartPost("http://www.realtoraccess.com/bi/conf/makelinedata/",e);

            break;

        case "polylinebar1":

            detailChartPost("http://www.realtoraccess.com/bi/conf/makelinedata/",e);

            break;

        case "circlepie":
        case "pie":
            //detailChartPost("http://www.realtoraccess.com/config/makelinedata/",e);
            detailChartPost("http://www.realtoraccess.com/bi/conf/makepiedata/",e);

            break;

        case "map":

            detailChartPost("http://www.realtoraccess.com/bi/conf/makemapdata/",e);
            break;
        case "panel1":
        case "panel2":
        case "panel3":
            detailChartPost("http://www.realtoraccess.com/bi/conf/makedashboarddata/",e);
            break;
        case "hotmap":
            clearInterval(timer);
            detailChartPost("http://www.realtoraccess.com/bi/conf/makethermodynamicdata/",e);
            break;
        default :
            detailChartPost("http://www.realtoraccess.com/bi/conf/makelinedata/",e);
    }
}


/******************筛选面板******************/
//删除
$("#detail").delegate(".class_data_item_outer_box","mouseenter",function(){
    $("#detail").find(".class_data_item_max_box b").hide();
    $(this).find("b").show();
    $("#detail").find(".class_data_item_outer_box ").removeClass("dataitemhover");
    $(this).addClass("dataitemhover");
});
$("#detail").delegate(".class_data_item_outer_box","mouseleave",function(){
    $("#detail").find(".class_data_item_max_box b").hide();
    $(this).removeClass("dataitemhover");
});
$("#detail").delegate(".class_data_item_max_box b","click",function(e){
    if(confirm("您确定删除此项吗？")){
        $(this).parent().remove();
        chartSaveStage=0;//保存状态归零
        changChooseURL(e);
        classInputAgainSort()
        recordSourceOpition()
    }else{
        return false;
    }
});

//增加
$("#detail").delegate(".class_data_item_add_box","click",function(){
    var firstslectoptionlist=$('select[name="selclassdata0" ]').html();
    classNameNum++;
    var outerIterm='<div  class="class_data_item_outer_box row zero ">' +

        '<div class="class_data_item_inner_box form-group col-xs-4 zero">' +
        '<label class="col-xs-5 zero">数据项：</label> ' +
        '<select name="selclassdata'+classNameNum+'"  class="class_data_souce_selec col-xs-7 zero"> ' +
        firstslectoptionlist +
        '</select> ' +
        '</div> ' +
        '<div class="class_data_item_inner_box selclasscomputerbox col-xs-4 zero"> ' +
        '<label class="col-xs-5 zero">条件：</label> ' +
        '<select name="selclasscompu'+classNameNum+'"    class="selclasscomputer col-xs-7 zero"> ' +
        '<option value="">请选择</option> ' +
        '<option value="eq">等于</option> ' +
        '<option value="noeq">不等于</option> ' +
        '<option value="gt">大于</option> ' +
        '<option value="gteq">大于等于</option> ' +
        '<option value="lt">小于</option> ' +
        '<option value="lteq">小于等于</option> ' +
        '<option value="blank">为空</option> ' +
        '<option value="noblank">不为空</option> ' +
        '<option value="data" class="s">请选择</option>'+
        '</select> ' +
        '</div> ' +
        '<div class="class_data_item_inner_box datavaluebox col-xs-4 zero"> ' +
        '<label class="col-xs-5 zero">值：</label> ' +
        '<input name="selclassval'+classNameNum+'"   class="selclassval col-xs-7 zero" type="text" placeholder=" 请输入"/> '+
        '</div> ' +
        '<b class="s">×</b> ' +
        '</div>';
    $("#detail").find(".class_data_item_max_box ").append(outerIterm);

    classInputAgainSort();
    chartSaveStage=0;//保存状态归零


});
//筛选表单强制排序
function classInputAgainSort(){
    var $date=$("#detail").find(".class_data_souce_selec");
    //console.log($date);
    $date.each(function(i){
        $(this).attr("name","selclassdata"+i);
    });
    var $computer=$("#detail").find(".selclasscomputer");
    $computer.each(function(i){
        $(this).attr("name","selclasscompu"+i);
    })
    var $valueV=$("#detail").find(".selclassval");
    $valueV.each(function(i){
        $(this).attr("name","selclassval"+i);
    })
}
//筛选面板选择判断
// select1数据源选择
$("#detail").delegate(".class_data_souce_selec","click",function(e){
    console.log(this)
    var datetype=($(this).find("option:selected")).attr("data-rttype");
    var name=$(this).attr("name");
    var nameNum=name.slice(-1);
    //console.log(nameNum);
    if(datetype=="rtline"){
        $(this).parents().siblings(".class_data_item_inner_box").hide();
        var $slect=$(this).parents().siblings(".selclasscomputerbox").children(".selclasscomputer");
        $slect.val("data");
        $(this).parents().siblings(".date_echart_time_box").remove();
        var echartDateH='<div class="class_data_item_inner_box date_echart_time_box col-xs-4 zero"> ' +
            '<label class="col-xs-5 zero">开始日期：</label> ' +
            '<input class="col-xs-7 zero laydate-icon laydate_start"  id="startDate'+nameNum+'" ' +
            'data-start="1900/06/16/00:00:00"' +
            ' data-end="2099/06/16/23:59:59" type="text" placeholder=" 请选择日期"/> ' +
            '</div> ' +
            '<div class="class_data_item_inner_box date_echart_time_box col-xs-4 zero"> ' +
            '<label class="col-xs-5 zero">结束日期：</label> ' +
            '<input class="col-xs-7 zero laydate-icon laydate_end"  id="endDate'+nameNum+'"' +
            'data-start="1900/06/16/00:00:00"' +
            'data-end="2099/06/6/23:59:59" type="text" placeholder=" 请选择日期"/>' +
            ' </div>'
        $(this).parents().parents(".class_data_item_outer_box").append(echartDateH);

    }else{
    	$(this).parents().siblings(".date_echart_time_box").remove();
        //($("#detail").find(".date_echart_time_box")).remove();
        $(this).parents().siblings(".class_data_item_inner_box").show();
        var $slect=$(this).parents().siblings(".selclasscomputerbox").children(".selclasscomputer");
        $slect.val("");

    }
    chartSaveStage=0;//保存状态归零
    changChooseURL(e);

});
// select1数据源选择
$("#detail").delegate(".selclasscomputer","click",function(e){
    var dateV=($("#detail").find(".selclasscomputer option:selected")).val();
    if((dateV=="blank")||(dateV=="noblank")){
        $(this).parents().siblings(".datavaluebox").hide();

    }else{
        $(this).parents().siblings(".datavaluebox").show();

    }
    chartSaveStage=0;//保存状态归零
    changChooseURL(e);

});


//时间插件墨绿皮肤
$("#detail").delegate(".laydate_start","click",function(e){
    var name=$(this).attr("id");
    var nameNum=name.slice(-1);
    dateStartAPI(nameNum,e);
});
$("#detail").delegate(".laydate_end","click",function(e){
    var name=$(this).attr("id");
    var nameNum=name.slice(-1);
    dateEndAPI(nameNum,e);
});


function dateStartAPI(num,e){
    laydate.skin('molv');
    var start = {
        elem: '#startDate'+num,
        format: 'YYYY/MM/DD/hh:mm:ss',
        min: '1900-06-16 00:00:00', //设定最小日期为当前日期
        max: '2099-06-16 23:59:59', //最大日期
        istime: true,
        istoday: false,
        choose: function(datas){
            min = datas; //开始日选好后，重置结束日的最小日期

            ($("#detail").find('input.selclassval')).attr("data-start",min);
            var startime=($("#detail").find('input.selclassval')).attr("data-start")
            var endtime=($("#detail").find('input.selclassval')).attr("data-end");
            var time=startime+","+endtime;
            var $input=($("#detail").find('input[name="selclassval'+num+'"]'));
            $input.val(time);
            //console.log($input,$input.val())

            chartSaveStage=0;//保存状态归零
            changChooseURL(e);
        }
    };
    laydate(start);
}
function dateEndAPI(num,e){
    laydate.skin('molv');
    var end = {
        elem: '#endDate'+num,
        format: 'YYYY/MM/DD/hh:mm:ss',
        min: '1900-06-16 00:00:00',
        max: '2099-06-16 23:59:59',
        istime: true,
        istoday: false,
        choose: function(datas){
            max = datas; //结束日选好后，重置开始日的最大日期
            ($("#detail").find('textarea[name="inputendtime0" ]')).val(max);
            var endtime=($("#detail").find('input.selclassval')).attr("data-end",max);
            endtime=($("#detail").find('input.selclassval')).attr("data-end")
            var startime=($("#detail").find('input.selclassval')).attr("data-start");
            var time=startime+","+endtime;
            var $input=($("#detail").find('input[name="selclassval'+num+'"]'));
            $input.val(time);
            //console.log($input,$input.val())

            chartSaveStage=0;//保存状态归零
            changChooseURL(e);
        }
    };
    laydate(end);
}




// detail 折线图柱状图混合图页面初始化
/***************增加detail页面 折线 柱状 混合图 热力图 selcet生成option***************/
function appendChartOption(){
    $.get("http://www.realtoraccess.com/bi/get/sourceinfo2/",function(data){
        //http://www.realtoraccess.com/get/sourceinfo2/"后台将弹框选中数据流存入此处，
        //console.log("sourceinfo2此处判断是否为实时数据项realtime：设计图片的.detail_type_img_hover类型的自定义属性data-db进行判断",data);

        gederOpition(data);
        //
        function gederOpition(data){
            var obj= $.parseJSON(data);
            //data-db修改
            //console.log(obj);
            $(".realtimetype").attr("data-db","");
            //如果为实时
            var $realtime=$("#detail").find("#mysqle_timely");
            if($realtime.is(":checked")){
                $(".realtimetype").attr("data-db","realtime");
                dateergodicObj(obj.date,"#detail_sel_x","");
                dateergodicObj(obj.num,"#detail_sel_x","");
                dateergodicObj(obj.text,"#detail_sel_x","");
                $("#timewindowbox").show();
                $(".source_sort").hide();
            }else{
                $("#timewindowbox").hide();
                $(".realtimetype").attr("data-db","");
                textergodicObj(obj.date,"#detail_sel_x",'');
                textergodicObj(obj.num,"#detail_sel_x",'');
                textergodicObj(obj.text,"#detail_sel_x",'');
                $(".source_sort").show();
            }

            ergodicObj(obj.num,"#detail_sel_y",'<option value="">请选择</option>');
            ergodicObj(obj.num,"#detail_sel_y0",'<option value="">请选择</option>');
            ergodicObj(obj.num,"#detail_sel_y1",'<option value="">请选择</option>');
            /*图例*/
            textergodicObj(obj.num,"#Legend_",'');
            textergodicObj(obj.text,"#Legend_",'');
            textergodicObj(obj.date,"#Legend_",'');
            /*热力图*/
            textergodicObj(obj.num,"#row_mark_sel_x",'');
            textergodicObj(obj.text,"#row_mark_sel_x",'');
            textergodicObj(obj.date,"#row_mark_sel_x",'');

            textergodicObj(obj.num,"#col_mark_sel_x",'');
            textergodicObj(obj.text,"#col_mark_sel_x",'');
            textergodicObj(obj.date,"#col_mark_sel_x",'');

            textergodicObj(obj.num,"#deatil_data_sel_x",'');
            textergodicObj(obj.text,"#deatil_data_sel_x",'');
            textergodicObj(obj.date,"#deatil_data_sel_x",'');


            textergodicObj(obj.text,".class_data_souce_selec","");//筛选项sel1
            textergodicObj(obj.num,".class_data_souce_selec","");//筛选项sel1
            dateergodicObj(obj.date,".class_data_souce_selec","");//筛选项sel1

            /*textergodicObj(obj.text,".tabHightSourceSelect",'<option value="">请选择</option>');
            ergodicObj(obj.num,".tabHightSourceSelect",'<option value="">请选择</option>');
            textergodicObj(obj.date,".tabHightSourceSelect",'<option value="">请选择</option>');*/

        }
    })
}

/*********记忆选中OPTION(数据源排序初始化)***********/
function recordSourceOpition(){
    var arr=[];
    var $option=$("#detail").find(".deatil_sel_checked");
    $option.each(function(){
        var val=$(this).val();
        arr.push(val);
    })
    ergodicObj(arr,".tabHightSourceSelect",'<option value="">请选择</option>');
}
// detail 仪表图 地图 环形图 饼图页面初始化
/********增加detail页面 仪表图 地图 环形图 数据源selcet生成option*********/
function dataSource(url,val){
    $.get(url,val,function(data){
        var obj= $.parseJSON(data);
        console.log(obj)

        ergodicObj(obj,"#detail_sel_y",'<option value="">请选择数据源</option>')
        ergodicObj(obj,"#detail_sel_x",'<option value="">请选择数据源</option>')
        //ergodicObj(obj,".tabHightSourceSelect",'<option value="">请选择</option>')//排序字符集
    })
}
/*遍历mun对象,生成option 单一类型添加（html） 普通情况（非实时）通用*/
function ergodicObj(obj,id,stri){
    var str=stri;
    if(obj.length>0){
        for (var key in obj){
            //console.log(obj[key])
            str+='<option value="'+obj[key]+'" data-xtype="" data-date="no">'+obj[key]+'</option>'
        }
        $(id).html(str);
    }
}

/*遍历date对象,生成option,data-rttype="rtline"只为web实时用*/
function dateergodicObj(obj,id,stri){
    var str=stri;
    if(obj.length>0){
        //$("#"+id).html("");
        for (var key in obj){
            //console.log(obj[key])
            str+='<option value="'+obj[key]+'"data-rttype="rtline">'+obj[key]+'</option>'
        }
        ($("#detail").find(id)).append(str);
    }
}
/*遍历t对象,生成option,全部添加(append)*/
function textergodicObj(obj,id,stri){
    var str=stri;
    if(obj.length>0){
        for (var key in obj){
            //console.log(obj[key])
            str+='<option value="'+obj[key]+'"data-rttype="">'+obj[key]+'</option>'
        }
        ($("#detail").find(id)).append(str);
    }
}

/*********************************饼图图例显示图里选择改变*******************************************/
$("#detail").delegate("#deatil_selxckeck","click",function(){
    var $checkbox=$("#detail").find($("#deatil_selxckeck"));
    var $zhou=$("#detail").find($("#deatil_selx_box"));
    var $add=$("#detail").find($("#deatil_sel_addSelect"));
    var $yfrom=$("#detail").find($("#y_all_form"));
    var $xfrom=$("#detail").find($("#right_dim_x"));
    var $slex=$("#detail").find($("#detail_sel_x"));

    var yhtml='<div class="row zero dimybox"> ' +
        '<b class="s">×</b> ' +
        '<div class="col-xs-12 padding_zero Mcenter" > ' +
        '<label  class="col-xs-5 zero">数值：</label> ' +
        '<select name="selyF0" id="detail_sel_y" class="col-xs-7  deatil_sel_checked zero"> ' +
        '<option value="">请选择</option> ' +
        '</select> ' +
        '</div> ' +
        '<div class="col-xs-12 padding_zero Mcenter"> ' +
        '<label  class="col-xs-5 zero">计算规则：</label> ' +
        '<select name="selyS0" id="detail_sel_y_accut" class="col-xs-7 zero"> ' +
        '<option value="sum">总和</option> ' +
        '<option value="count">个数</option> ' +
        '<option value="avg">平均</option> ' +
        '</select> ' +
        '</div> ' +
        '<div class="form-group col-xs-12 zero Mcenter"> ' +
        '<label for="polyline_yuint" class="col-xs-5 zero">单位：</label> ' +
        '<input id="polyline_yuint" name="lyuint" class="col-xs-7 zero" type="text" placeholder="请输入"/> ' +
        '</div> ' +
        '</div>'
    var xzhouhtml='<div class="col-xs-12 padding_zero Mcenter" id="deatil_selx_box"> ' +
        '<label class="col-xs-5 zero">轴分类：</label> ' +
        '<select name="selx" id="detail_sel_x" class="col-xs-7 deatil_sel_checked zero"> ' +
        '<option value="">请选择</option> ' +
        '</select> ' +
        '</div>'

    console.log($checkbox.is(":checked"))
    var slexhtml='<select name="selx" id="detail_sel_x" class="col-xs-7 deatil_sel_checked zero"> ' +
        '<option value="">请选择</option> ' +
        '</select>'
    $slex.html(slexhtml)
    if($checkbox.is(":checked")){
        $add.hide();
        $zhou.show();

        $yfrom.html(yhtml)
    }else{
        $add.show();
        $zhou.hide();
    }
    appendChartOption()
});


/*****************  !!!!!!!!!!!!!!!!!!!!!!!!!!!detail全页面表单详情键值对POST（全页面post引擎函数）!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*********************************/

var first;//留住上一个ws
var imgBase64//echartbase64码
var getImageV//获取一个当前图表的img
var meChart;//留住

function detailChartPost(url,e){
    var $charticon=$("#detail").find($("#charticon"));
    if((meChart)&&(chartSaveStage==1)){
        //var getImageV=meChart.getImage();
        var getDataURL=meChart.getDataURL("png");
        var getDataURLdata = encodeURIComponent(meChart.getDataURL("png"));
        $charticon.val(getDataURL);
        //console.log("base64:", getDataURL)
    }

    var classV=($("#detail").find($("#detail_tab_class_set"))).serialize();//图表标题，分类，描述
    //console.log(classV);
    var chartitleV=($("#detail").find($("#detail_tab_base_set"))).serialize();//图表标题，分类，描述
    //console.log(chartitleV);

    if($(e.target).attr("data-type")){
        imgV=$(e.target).attr("data-type");//锁定默认第一个类型图
    }
    var dbV="&db="+($("#detail").find($(".detail_type_img_hover"))).attr("data-db")//数据库键值对
    //console.log(dbV);
    if(dbV=="&db="||dbV=="&db=undefined"){
        dbV="";//双y轴检测，否侧键值对出错
    }
    var legend=($("#detail").find($("#Legend_"))).val();
    if(!legend){
        legend="";
    }
    //console.log(legend)
    //console.log(imgV);
    //只有双y混合图可用；
    var bothYV="&"+($("#detail").find($("#y_all_left_form"))).serialize()+"&"+($("#detail").find($("#y_all_right_form"))).serialize()//双轴值
    //console.log("双y混合图",bothYV);
    if(bothYV=="&&"){
        bothYV="";//双y轴检测，否侧键值对出错
    }

    var yVaule="&"+($("#detail").find($("#y_all_form"))).serialize();
    if(yVaule=="&"){
        yVaule="";//y轴检测，否侧键值对出错
    }
    //console.log("双y轴",yVaule)

    var xVaule="&"+($("#detail").find($("#right_dim_x"))).serialize();
    //console.log(xVaule)
    if(xVaule=="&"){
        xVaule="";//y轴检测，否侧键值对出错
    }

    var rttypeV=($("#detail").find($("#detail_sel_x>option:selected"))).attr("data-rttype");//实时选项
    if(!rttypeV){
        rttypeV="";
    }
    //console.log("实时",rttypeV);

    var timewindow="&"+$("#detail_tab_hight_set").serialize()
        //console.log(timewindow);
    //timewindow防止为undefined
   if(timewindow=='&timewindow=undefined'){
       timewindow='&timewindow='
   }

    xVaule=xVaule+"&rttype="+rttypeV;
    //console.log(xVaule)
    if(xVaule=="&selx="){
        xVaule="";//x轴检测，否侧键值对出错
    }
    //console.log(xVaule);

    if(yVaule!=="&selyF0="){//防止点击图片类型，echart过早替换图片
        //console.log(xVaule);
        //console.log(yVaule);
        allVaule= classV+bothYV+yVaule+xVaule+"&ctype="+imgV+"&saveV="+chartSaveStage+"&"+chartitleV+dbV+timewindow+"&legend="+legend;
        //console.log("待传入",allVaule);
        $.post(url,allVaule,function(data){
            if(data=='nothing'){
            	return;
            }
            var saveObj= $.parseJSON(data);
            //console.log(data,saveObj.done);
            //跳转页面
            if(saveObj.done=="1"){
                $(".loading").hide();
                $(".selectpage").show();
                //window.open("http://www.realtoraccess.com/config/distribute/");
            }

            if(dbV=="&db=visio_dashboard"){
                //实时仪表盘
                //console.log(allVaule);
                console.log("实时仪表盘")
                var Obj= $.parseJSON(data);
                var panelURL=Obj.url;
                ctype=$(".detail_type_img_hover").attr("data-type");
                //console.log(Obj.url);
                IntervalEchart(panelURL,ctype,"detail_main",5000,0);

            }else if(dbV=="&db=realtime"){
                //实时柱状图，折线图。折柱混合图 websoket
                console.log("websoket")
                echartWebSocket('ws://127.0.0.1:9527/real/time/chart',data,chartSaveStage,rttypeV,"detail_main");

            }else{
                //普通情况
                var filepathObj= $.parseJSON(data);
                filepath= filepathObj.jsn+"";
                ctype=filepathObj.ctype;
                pritCharts(filepath,ctype,"detail_main",filepathObj.theme);
                //console.log('普通情况');
            }
            ($("#detail_show_form").find($(".detail_img_map"))).css("display","none");
            ($("#detail_show_form").find($("#loadechart"))).css("display","block");

        })
    }

}



/**************chart是否保存状态**************/
$("#detail_show_form").click(function(e){
    if($(e.target).attr("id")=="detail_chart_sv"){
        $(".loading").show();
        clearInterval(timer);
        chartSaveStage=1;
        changChooseURL(e);
        //window.location.href="http://www.realtoraccess.com/config/distribute/";
    }
});
$(".detail_lacal").click(function(e){
    $(".selectpage").hide();
        $(".loading").hide();
    }
)


/*重新添加数据btn*/
$("#detail_show_form").delegate("#againAddData","click",function(){
    $("#index_addData").load("http://www.realtoraccess.com/static/bi/addDataBounced.html",function(data){
        $("#index_addData").html(data);
        /****************弹出框生成select******************/
        $.get("http://www.realtoraccess.com/get/sourcename/", function (data) {
            var obj = $.parseJSON(data);
            for (var key in obj) {
                ($("#index_addData").find(".index_dataItem")).append('<p class="col-xs-12" ' +
                    'data-value="' + obj[key].sourceid + '">'+'<span>' +
                    obj[key].sourcetype+'</span>' + obj[key].sourcename + '</p>')
            }
            $("#index_addData").show();

            indexAddData.fuzzySearch();
            indexAddData.selectDate();
            indexAddData.exitBounced();
            indexAddData.OkToDeitail();
        })
        indexAddData.isBounced=true;

    })

})



/*********************分类模糊搜索************************/
$("#detail_show_form").delegate("#polyline_classify","keyup",function(){
    var keywordV=($("#detail_show_form").find($("#polyline_classify"))).val();
    //console.log(keywordV)
    $.get("http://www.realtoraccess.com/bi/get/datatype/",{keyword:keywordV},function(data){
        analysisClassData(data);

    })
})
//解析模糊分类对象；
function analysisClassData(data){
    //console.log(data)
    var obj=$.parseJSON(data);
    //console.log(data)
    var classH='';
    for(var key in obj){
        classH+="<p>"+obj[key]+"</p>"
    }
    ($("#detail").find($(".class_fuzzy_search"))).html(classH);
}
//获取焦点，获得所有
$("#detail_show_form").delegate("#polyline_classify","focus",function(){
    $("#detail_show_form").find($("div.class_fuzzy_search")).show()
    $.get("http://www.realtoraccess.com/bi/get/datatype/",function(data){
        analysisClassData(data);
    })
})
$("#detail_show_form").delegate(".class_fuzzy_search>p","click",function(){
    $(this).siblings("p").removeClass("classphover");
    $(this).addClass("classphover");
    var v=$(this).html();
    ($("#detail_show_form").find($("#polyline_classify"))).val(v);
    ($("#detail_show_form").find(".class_fuzzy_search")).hide();

})

/*删除y轴div.dimybox,重新name排序*/
$("#detail_show_form").delegate("div.dimybox>b","click",function(e){
    if(confirm("您确定删除此项吗？")){
        $(this).parent().remove();
        sellistAgainSort(1);
        chartSaveStage=0;//保存状态归零
        changChooseURL(e);
    }else{
        return false;
    }

})
$("#detail_show_form").delegate("div.yalldimybox>b","click",function(e){
    if(confirm("您确定删除此项吗？")){
        $(this).parent().remove();
        sellistAgainSort(2);
        chartSaveStage=0;//保存状态归零
        changChooseURL(e);
    }else{
        return false;
    }

})
/*重新name排序*/
/*直线slcet*/
function sellistAgainSort(p){
    var $sellist1=$("#detail_show_form").find($(".yDimSlect1"));
    var $sellist2=$("#detail_show_form").find($(".yDimSlect2"));
    var $sellist3=$("#detail_show_form").find($(".yDimSlect3"));
    var $sellist4=$("#detail_show_form").find($(".yDimSlect4"));

    $sellist1.each(function(i){
        //console.log(i);
        //console.log($sellist1)
        $(this).attr("id","detail_sel_y"+(i+p)+"");
        $(this).attr("name","selyF"+(i+p)+"")

    })
    $sellist2.each(function(i){
        $(this).attr("id","detail_sel_y_accut"+(i+p)+"");
        $(this).attr("name","selyS"+(i+p)+"");
    })

    if($sellist3){
        $sellist3.each(function(i){
            $(this).attr("id","detail_sel_y_type"+(i+p)+"");
            $(this).attr("name","selySt"+(i+p)+"")
        })
    }

    if($sellist4){
        $sellist4.each(function(i){

            $(this).attr("name","yAxisIndex"+(i+p)+"")
        })
    }
}






/******************y轴增加新select******************/
$("#detail_show_form").click(function(e){
    if($(e.target).attr("data-target")=="addsel"){
        idmun++;
        //console.log(idmun)

        var firstOptionV = $("#detail_sel_y").html();
        //console.log( firstOptionV)
        var hv1=
            ' <div class="row zero dimybox" style="height:88px;border-top: 1px dotted #10C757;padding: 15px 0;"> ' +
            '<b>×</b> ' +
            '<div class="col-xs-12 padding_zero Mcenter" > ' +
            '<label  class="col-xs-5 zero">Y轴：</label> ' +
            '<select name="selyF' + idmun + '" id="detail_sel_y' + idmun + '" ' +
            'class="col-xs-7 yDimSlect1 deatil_sel_checked zero"> ' + firstOptionV + '</select> ' +
            '</div> ' +
            '<div class="col-xs-12 padding_zero Mcenter"> ' +
            '<label  class="col-xs-5 zero">计算规则：</label> ' +
            '<select name="selyS' + idmun + '" id="detail_sel_y_accut' + idmun + '" ' +
            'class="col-xs-7 yDimSlect2 zero"> ' +
            '<option value="sum">总和</option> ' +
            '<option value="count">个数</option> ' +
            '<option value="avg">平均</option> ' +
            '</select> ' +
            '</div> ' +
            '</div>'

        var hv2=
            '<div class="row zero dimybox dimyletfbox deitail_y1" data-num="0"  style="height:120px;border-top: 1px dotted #10C757;padding: 15px 0;"> ' +
            '<b style="position: absolute;top: -2px;right: 3px;color: #4E7E9A;font-size: 14px;">×</b> ' +
            '<div class="col-xs-12 padding_zero Mcenter" style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero" style="text-align: right;line-height: 24px;">Y轴：</label> ' +
            '<select name="selyF' + idmun + '" id="detail_sel_y' + idmun + '" class=" yDimSlect1 deatil_sel_checked col-xs-7 zero"> ' +
            firstOptionV+
            '</select> ' +
            '</div> ' +
            '<div class="col-xs-12 padding_zero Mcenter"  style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero" style="text-align: right;line-height: 24px;">计算规则：</label> ' +
            '<select name="selyS' + idmun + '" id="detail_sel_y_accut' + idmun + '" class=" yDimSlect2 col-xs-7 zero"> ' +
            '<option value="sum">总和</option> ' +
            '<option value="count">个数</option> ' +
            '<option value="avg">平均</option> ' +
            '</select> ' +
            '</div> ' +
            '<div class="col-xs-12 padding_zero Mcenter"  style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero" style="text-align: right;line-height: 24px;">图型：</label> ' +
            '<select name="selySt' + idmun + '" id="detail_sel_y_type' + idmun + '" class="  yDimSlect3 col-xs-7 zero"> ' +
            '<option value="line" >折线图</option> ' +
            '<option value="bar">柱状图</option> ' +
            '</select> ' +
            '</div> ' +
            '<div class="" > ' +
            '<select name="yAxisIndex' + idmun + '" id="yAxisIndex' + idmun + '" class="s" style="display: none"> ' +
            '<option value="0">"0"</option> ' +
            '</select> ' +
            '</div> ' +

            '</div>'

        var hv3=

            '<div  style="height: 120px;border-top: 1px dotted #10C757;padding: 12px 0; margin-bottom: 5px;background: #fff;position: relative;" class="row zero deitail_y1 yalldimybox" data-num="0"> ' +
            '<b class="" style="position: absolute;top: -2px;right: 3px;color: #4E7E9A;font-size: 14px;">×</b> ' +
            '<div class="col-xs-12 padding_zero Mcenter" style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero" style="text-align: right;line-height: 24px;">左Y轴：</label> ' +
            '<select name="selyF' + idmun + '" id="detail_sel_y' + (idmun+1) + '" class="col-xs-7 deatil_sel_checked zero yDimSlect1"> ' +
            firstOptionV +
            '</select> ' +
            '</div> ' +
            '<div class="col-xs-12 padding_zero Mcenter" style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero"style="text-align: right;line-height: 24px;">计算规则：</label> ' +
            '<select name="selyS' + idmun + '" id="detail_sel_y_accut' + idmun + '" class="col-xs-7 zero yDimSlect2"> ' +
            '<option value="sum">总和</option> ' +
            '<option value="count">个数</option> ' +
            '<option value="avg">平均</option> ' +
            '</select> ' +
            '</div> ' +
            '<div class="col-xs-12 padding_zero Mcenter" style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero" style="text-align: right;line-height: 24px;">图型：</label> ' +
            '<select name="selySt' + idmun + '" id="detail_sel_y_type' + idmun + '" class="col-xs-7 zero yDimSlect3"> ' +
            '<option value="line" >折线图</option> ' +
            '<option value="bar">柱状图</option> ' +
            '</select> ' +
            '</div> ' +
            '<div class="" > ' +
            '<select name="yAxisIndex' + idmun + '" class="s yDimSlect4" style="display: none"> ' +
            '<option value="0">"0"</option><!--代表左轴数据--> ' +
            '</select> ' +
            '</div> ' +

            '</div>'

        var hv4=

            '<div  style="height: 120px;border-top: 1px dotted #10C757;padding: 12px 0; margin-bottom: 5px;background: #fff;position: relative;" class="row zero deitail_y1 yalldimybox" data-num="0"> ' +
            '<b class="" style="position: absolute;top: -2px;right: 3px;color: #4E7E9A;font-size: 14px;">×</b> ' +
            '<div class="col-xs-12 padding_zero Mcenter" style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero" style="text-align: right;line-height: 24px;">右Y轴：</label> ' +
            '<select name="selyF' + (idmun+1) + '" id="detail_sel_y' + (idmun+1) + '" class="col-xs-7 deatil_sel_checked zero yDimSlect1"> ' +
            firstOptionV +
            '</select> ' +
            '</div> ' +
            '<div class="col-xs-12 padding_zero Mcenter" style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero" style="text-align: right;line-height: 24px;">计算规则：</label> ' +
            '<select name="selyS' + (idmun+1) + '" id="detail_sel_y_accut' + (idmun+1) + '" class="col-xs-7 zero yDimSlect2"> ' +
            '<option value="sum">总和</option> ' +
            '<option value="count">个数</option> ' +
            '<option value="avg">平均</option> ' +
            '</select> ' +
            '</div> ' +
            '<div class="col-xs-12 padding_zero Mcenter" style="padding: 5px 10px 5px 5px;"> ' +
            '<label  class="col-xs-5 zero"style="text-align: right;line-height: 24px;">图型：</label> ' +
            '<select name="selySt' + (idmun+1) + '" id="detail_sel_y_type' + (idmun+1) + '" class="col-xs-7 zero yDimSlect3"> ' +
            '<option value="line" >折线图</option> ' +
            '<option value="bar">柱状图</option> ' +
            '</select> ' +
            '</div> ' +
            '<div class="" > ' +
            '<select name="yAxisIndex' + (idmun+1) + '" class="s yDimSlect4" style="display: none"> ' +
            '<option value="1">"1"</option><!--代表右轴数据--> ' +
            '</select> ' +
            '</div> ' +

            '</div>'

        if($(e.target).is("span")) {

            switch ($(e.target).parent().attr("id")){
                case "deatil_sel_addSelect":

                    dimyHiger();
                    $("#y_all_form").append(hv1);
                    sellistAgainSort(1);
                    break;

                case "deatil_sel_addSelect_y0":

                    dimyHiger(1);
                    $("#y_all_form").append(hv2);
                    sellistAgainSort(1)
                    break;

                case "deatil_sel_addSelect_yleft":

                    $("#y_all_left_form").append(hv3);
                    sellistAgainSort(2)
                    break;
                case "deatil_sel_addSelect_yRighe":

                    $("#y_all_right_form").append(hv4);
                    sellistAgainSort(2)
                    break;
            }

        }else if($(e.target).is("button")){
            switch ($(e.target).attr("id")){
                case "deatil_sel_addSelect":

                    dimyHiger()
                    $("#y_all_form").append(hv1);
                    sellistAgainSort(1);
                    break;
                case "deatil_sel_addSelect_y0":
                    dimyHiger();
                    $("#y_all_form").append(hv2);
                    sellistAgainSort(1)
                    break;
                case "deatil_sel_addSelect_yleft":

                    $("#y_all_left_form").append(hv3);
                    sellistAgainSort(2)
                    break;
                case "deatil_sel_addSelect_yRighe":

                    $("#y_all_right_form").append(hv4);
                    sellistAgainSort(2)
                    break;
            }

        }
    }
})

/*******折线图柱状图 y轴修改h500********/
function dimyHiger(){
    ($("#detail_show_form").find("#y_all_form")).animate({height:"435px"},1000)
}
