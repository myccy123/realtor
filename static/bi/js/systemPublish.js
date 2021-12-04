/**
 * Created by lenovo on 2016/12/2.
 */
/**************system.html********************/
/*******system 元素树click*********/
$("#system_left_center_maxBox").click(function(e){
    if($(e.target).is("p")){
        $(e.target).siblings().toggleClass('none');
        $(e.target).children("span").toggleClass("glyphicon-triangle-bottom");
    }else if($(e.target).is("span.lispan")){
        $(e.target).parent().siblings().toggleClass('none');
        $(e.target).toggleClass("glyphicon-triangle-bottom");
    }
})



/***************布局模板切换事件监听***************/

$("#sys_modul_class>li").click(function(){
    $("#sys_modul_class>li").removeClass("sye_handle_hover");
    $(".caozuoarea").removeClass("handleAreaHover");
    $(".caozuoarea").hide();
    $(this).addClass("sye_handle_hover");
    if(($(this).attr("data-show"))==="add"){
        $("#sys_add_chartGrid").show();
        $("#sys_chart_dre0").hide();
    }else if(($(this).attr("data-show"))==="explain"){
        $("#sys_add_chartGrid").hide();
        $("#sys_chart_dre0").show();
    }else{
        $("#sys_chart_dre0").hide();
        $("#sys_add_chartGrid").hide();
    }
    var $model=($(this).attr("data-model"))+"area";
    $("div[data-model="+$model+"]").addClass("handleAreaHover");
    $("div[data-model="+$model+"]").show();
})
//说明文本添加说明
$("#sys_chart_dre0").change(function(){
    $("#sys_show_explain").html($("#sys_chart_dre0").val());
})
/******************分类模糊搜索**********************/

$('input[name="Modeltype"]').focus(function(){
    $('.sys_url_class').show();
    $.get("http://www.realtoraccess.com/bi/get/temptype/",function(data){
        var obj= $.parseJSON(data);
        var liHtml="";
        for(var key in obj){
            //console.log(obj[key])
            liHtml+='<li>'+obj[key]+'</li>'
        }
        $('.sys_url_class').html(liHtml);
    })
})
$('input[name="Modeltype"]').keyup(function(){

    var keyV=$('input[name="Modeltype"]').val();
    $.get("http://www.realtoraccess.com/bi/get/temptype/",{keyword:keyV},function(data){
        //console.log(data)
        var obj= $.parseJSON(data);
        var liHtml="";
        for(var key in obj){
            //console.log(obj[key])
            liHtml+='<li>'+obj[key]+'</li>'
        }
        $('.sys_url_class').html(liHtml);

    })
});
$('input[name="tempname"]').blur(function(){
    publishbtnDisabled();
});
$('input[name="Modeltype"]').blur(function(){
    publishbtnDisabled();
})

$("#system").delegate(".sys_url_class>li","click",function(){
    $(this).siblings().removeClass("sys_classhover");
    $(this).addClass("sys_classhover");
    var v=$(this).html();
    $('input[name="Modeltype"]').val(v);
    $('.sys_url_class').hide();
    publishbtnDisabled();
})


/***************点击数据树生成imglist***************/
$("#system_tree").click(function(e){
    if($(e.target).is("p")){
        var datatypeV=$(e.target).attr("data-num");
        //console.log(datatypeV)
        imglist({datatype:datatypeV});
    }else if($(e.target).is("span.lispan")){
        var datatypeV=$(e.target).parent().attr("data-num");
        imglist({datatype:datatypeV});//传9
    }
})
/*************！！！！数据树添加生成(数据管理下数据树初始化)！！！！！！*****************/
function dataTreeAppend(){
    $.get("http://www.realtoraccess.com/bi/get/userchart",function(data){
        var obj= $.parseJSON(data);
        $("#system_tree").html("");
        //console.log(data)
        for(var key in obj){
            var ulHtml='';
            //console.log(obj[key],key);
            ulHtml='<li data-type='+key+'> ' +
                '<p  class="sys_tree_head_title" data-num='+key+'> ' +
                '<span class="lispan glyphicon glyphicon-triangle-right"></span>' +key+
                '</p> <ul class="none" data-type='+key+'>  </ul> </li>'
            $("#system_tree").append(ulHtml);
            for(var index in obj[key]){
                //console.log(obj[key][index].chartname);
                var liHtml='';
                liHtml='<li> <p class="sys_tree_content_title" data-num="'+obj[key][index].chartid+'">'+obj[key][index].chartname+' </p> </li>';
                var $url=$("#system_tree").find($('ul[data-type='+key+']'));
                $url.append(liHtml);
            }
        }
    })
}
//*******************imglist()******************
function imglist(value){
    $.get("http://www.realtoraccess.com/bi/get/userchart",value,function(data){
        //console.log(value)
        var objdata= $.parseJSON(data);
        //console.log(data)
        var imglist="";
        $("#sys_treeImg").html("")
        for( var key in objdata){
            console.log("图片列表",objdata[key]);
            for(var index in objdata[key]){
                if(objdata[key][index].dataicon){
                    var url=""+objdata[key][index].dataicon;
                    imglist+='<li class="col-xs-12 zero" style="background: #789DB2;margin-top: 2px;position:relative">' +
                            '<h6 style="color:#fff;margin: 2px 5px;padding-right:10px;font-size: 12px"' +
                            'data-chartid="'+objdata[key][index].chartid+'"' +
                            '>标题：'+objdata[key][index].chartname+
                            '<b class="s" style="font-size:18px;position:absolute; top:-3px;right:3px; color:#fff;z-index:10;"' +
                            'data-chartid="'+objdata[key][index].chartid+'"' +
                            '>×</b>' +
                            '</h6>'+
                            '<img src="'+url+'" class="img-responsive" style="background:#fff" ' +
                            'data-wrapurl="'+objdata[key][index].wrapurl+'"' +
                            'data-tag="img1" ' +
                            'data-data="'+objdata[key][index].data+'" ' +
                            'data-ctype="'+objdata[key][index].ctype+'" ' +
                            'data-chartid="'+objdata[key][index].chartid+'"' +
                            'data-srcid="'+objdata[key][index].srcid+'"' +
                            'data-rttype="'+objdata[key][index].rttype+'"'+
                            'data-timewindow="'+objdata[key][index].timewindow+'"'+
                            'data-theme="'+objdata[key][index].theme+'"'+
                            'alt="'+objdata[key][index].chartname+'" ' +
                            'title="'+objdata[key][index].chartname+ '"/>' +
                            '</li>';
                }else{
                    //console.log(objdata[key].wrapurl,objdata[key][index].timewindow)
                    imglist+='<li class="col-xs-12 zero" style="position:relative">' +
                        '<p class="col-xs-12 zero center" draggable="true" style="line-height:30px;style="padding-left:15px;" ' +
                        'data-wrapurl="'+objdata[key][index].wrapurl+'"' +
                        'data-tag="img1" ' +
                        'data-data="'+objdata[key][index].data+'" ' +
                        'data-ctype="'+objdata[key][index].ctype+'"' +
                        'data-chartid="'+objdata[key][index].chartid+'"' +
                        'data-srcid="'+objdata[key][index].srcid+'"' +
                        'data-rttype="'+objdata[key][index].rttype+'"'+
                        'data-theme="'+objdata[key][index].theme+'"'+
                        'data-timewindow='+objdata[key][index].timewindow+
                        '>' +
                        '<b class="s" style="font-size:18px;position:absolute; top:0px;right:3px; color:#fff;z-index:10;">×</b>' +
                        '<span class="col-xs-11">' +objdata[key][index].chartname+'</span></p></li>';
                }
            }
        }
        $("#sys_treeImg").html(imglist)
    })
}
/*********************删除imglist 数据流********************************/
$("#sys_treeImg").delegate("b","click",function(){
    if (confirm('你确定要删除?')==true){
        var chartidV=$(this).parent().attr("data-chartid");
        var $targetli=$(this).parent().parent()
        $.post("http://www.realtoraccess.com/bi/delchart/",{chartid: chartidV},function(data){
            //console.log(data);
            if(data=="ok"){
                dataTreeAppend();//重新生成数据数；
                //window.location.reload();
                $targetli.slideUp();
            }
        })
    }else{
        return false;
    }

})
//数据预览显示×show
$("#sys_treeImg").delegate("li","mouseenter",function(){

    $(this).children().children("b").show();

})
$("#sys_treeImg").delegate("li","mouseleave",function(){

    $(this).children().children("b").hide();

})

/*********删除与增加 布局6 一行3个格子 任意增加删除**********/
//删除
$("#sys_arae6").delegate(".dragTarget","mouseenter" ,function(){
    $(this).children().children("b").show();
})
$("#sys_arae6").delegate(".dragTarget","mouseleave" ,function(){
    $(this).children().children("b").hide();
})
$("#sys_arae6").delegate(".dragTarget>ul>b","click" ,function(){
    if (confirm('你确定要删除?')==true){
        $(this).parent().parent("div").remove();
    }else{
        return false;
    }

})
//增加
$("#sys_add_chartGrid").click(function(){
    $("#sys_arae6").append('' +
        '<div class="col-md-4 col-sm-6 col-xs-12 zero dragTarget"' +
        'data-tag="div1"  data-num="six_1"   data-que="1"  style="cursor:pointer"> ' +
        '<ul class="col-xs-12 zero"> ' +
        '<b class="s">×</b> ' +
        '<li class="col-xs-12 zero center targetli"> ' +
        '<img src="http://www.realtoraccess.com/static/bi/images/sys300.png"' +
        ' class="img-responsive" alt="treesvgimg1" data-data="" data-ctype=""/>' +
        '</li> ' +
        '</ul> </div>')
})



/***************imglist拖动***************/

//拖动生成echart图
$(function(e) {
    var targetImg2;
    var targetImgStr;
    var jdata="";
    var jctype="";
    var wrapurl="";
    var $datatag="";
    var sysimgh="";
    var sysimgw="";
    var rttype="";
    var chartid="";
    var srcid="";
    var timewindow="";
    var theme="";
    $("#sys_treeImg").on("dragstart", function (e) {
        targetImg2 = $(e.target);
        $datatag = $(e.target).attr("data-tag");
        if($datatag =="img1"){
            jdata = $(e.target).attr("data-data");
            jctype = $(e.target).attr("data-ctype");
            wrapurl = $(e.target).attr("data-wrapurl");
            rttype = $(e.target).attr("data-rttype");
            chartid = $(e.target).attr("data-chartid");
            srcid = $(e.target).attr("data-srcid");
            timewindow=$(e.target).attr("data-timewindow");
            theme=$(e.target).attr("data-theme");


            $(".targetli").on("dragover", function (e) {
                e.preventDefault();
                sysimgh=$(this).innerHeight();
                sysimgw=$(this).width();
            })


            $(".targetli").on("drop", function (e) {

                if($datatag =="img1") {
                    boxID = "m" + boxidn;
                    boxidn++;
                    $(this).html('<div id="' + boxID + '" draggable="true" data-tag="div"' +
                        'style=" height:'+sysimgh+'px;width:'+sysimgw+'px;float:none;padding:35px 0;"' +
                        'class="col-xs-12 zero" data-data="' + jdata + '" ' +
                        'data-ctype="' + jctype + '"' +
                        'data-wrapurl="'+wrapurl+'"'+
                        'data-rttype="' + rttype + '"' +
                        'data-chartid="'+chartid+'"'+
                        'data-srcid="' + srcid + '"' +
                        'data-theme="' + theme + '"' +
                        'data-timewindow='+timewindow+

                        '></div>')
                    if(jctype=="panel1"||jctype=="panel2"||jctype=="panel3"){
                        //console.log(wrapurl,jctype, boxID,5000)
                        IntervalEchart(wrapurl,jctype, boxID,5000,"1",theme);
                    }else if(rttype=="rtline"){
                        data=  '{"srcid": "'+srcid+'",' +
                            '"ctype": "'+jctype+'",' +
                            '"tmpid": "'+chartid+'",' +
                            '"rttype": "'+rttype+'",' +
                            '"timewindow":'+timewindow+
                            '}'

                        console.log(data)

                        echartWebSocket('ws://127.0.0.1:9527/real/time/chart',data,1,"rtline",boxID,theme);
                        //echartWebSocket('ws://127.0.0.1:9527/real/time/chart',data,chartSaveStage,rttypeV,myChart);

                    }else{
                        console.log(jdata, jctype, boxID);
                        //pritCharts(jdata, jctype, boxID);
                        var selclassdata0="";
                        var selclassval0="";
                        var selclasscompu0="";

                        var dataObj={
                            selclassdata0:selclassdata0,
                            selclasscompu0:selclasscompu0,
                            selclassval0:selclassval0,
                            chartid:chartid
                         };
                         console.log(dataObj);

                        initEchartNormal(dataObj,jctype,boxID,theme);
                    }
                    $(".handleAreaHover ul").css("background","#fff");
                    $datatag="";
                }
            })
        }
    })
})
/**************echart拖动相互换位置div函数*************/
$(function(e) {
    var $targetImg;//拖动目标

    var $datatag;//拖动目标"data-tag"
    $('[data-tag="div1"]').on("dragstart", function (e) {
        $datatag =$(this).attr("data-tag");
        //console.log($datatag)
        if($(this).attr("data-tag")=="div1"){
            $targetImg = $(this);
            //console.log($targetImg)
        }
    })
    $(".dragTarget").on("dragover", function (e) {
        e.preventDefault();

    })
    $(".dragTarget").on("drop", function (e) {
        if ($datatag == "div1") {
            //console.log($targetImg.attr("data-que"))
            //console.log($(this).attr("data-que"));
            if($targetImg.attr("data-que")>$(this).attr("data-que")){
                $targetImg.insertBefore($(this))
                $(this).css(" animation","float .5s 1s infinite;")
            }else{
                $targetImg.insertAfter($(this))
            }
            $(".dragTarget").each(function(i){
                $(this).attr("data-que",i+"");
            })
            $datatag = "";
        }
    })
})
/*publishbtn禁用*/
function publishbtnDisabled(){
    var tempnameV=$("input[name='tempname']").val();
    var ModeltypeV=$("input[name='Modeltype']").val();
    if(tempnameV!==""&&ModeltypeV!==""){
        $("#sys_fabu").removeAttr("disabled");
    }else{
        $("#sys_fabu").attr("disabled","disabled");
    }
}

/**********发布click*****/

//储存片段及页面跳转
$("#sys_fabu").click(function(){
    indexShowHtml=$(".handleAreaHover").html();
    newindexShowHtml=indexShowHtml.replace(/[;]/g," ");
    var tempnameV=$("input[name='tempname']").val();
    var ModeltypeV=$("input[name='Modeltype']").val();
    //console.log(indexShowHtml);
    var htmltop=''
    var htmlbot=''
    var allHtmlV=htmltop+ newindexShowHtml+htmlbot;
    var postV={}
    postV["allHtml"]=allHtmlV
    postV["Mhtml"]=newindexShowHtml
    postV["Mstatus"]="0"
    postV["Modeltype"]=ModeltypeV
    postV["tempname"]=tempnameV

    //兼容safari
    var winRef = window.open("", "_blank");

    $.post("http://www.realtoraccess.com/bi/add/template/",postV,function(data){
        console.log(data);
        loc();

        function loc(){
            winRef.location=data+"?Mstatus=0";//改变页面的 location
        }
        //setTimeout(loc(),800);
    })
});
/********************系统管理切换*****************/
$("#system_left_maxBox_maxBox h4").click(function(){
    $("#system_left_maxBox_maxBox h4").removeClass('sys_c0ntrol_click_hover');
    $(this).addClass("sys_c0ntrol_click_hover");
    var sysv=$(this).attr("data-name");
    $(".rightHideContent").hide();
    $("[data-name="+sysv+"_content]").show();
    var $content=$("[data-name="+sysv+"]")
    console.log($content)
    if(($content.attr("data-name"))=="sys2"){
        urllistappend()
    }
    if(($(".sye_handle_hover").attr("data-show"))==="explain"){
        $("#sys_add_chartGrid").hide();
        $("#sys_chart_dre0").show();
    }
    $("#sys_treeImg").html("")
});
$("#system_tree").click(function(){
    $("#system_left_maxBox_maxBox h4").removeClass('sys_c0ntrol_click_hover');
    $(this).addClass("sys_c0ntrol_click_hover");
    var $me=$(this).siblings("h4.dataclass");
    $me.addClass("sys_c0ntrol_click_hover");
    var sysv=$me.attr("data-name");
    $(".rightHideContent").hide();
    $("[data-name="+sysv+"_content]").show();
    var $content=$("[data-name="+sysv+"]")
    console.log($content)
    if(($content.attr("data-name"))=="sys2"){
        urllistappend()
    }
    if(($(".sye_handle_hover").attr("data-show"))==="explain"){
        $("#sys_add_chartGrid").hide();
        $("#sys_chart_dre0").show();
    }
    $("#sys_treeImg").html("")
});


//url管理
// 列表折叠；s

$("#url_list_right").delegate("div.url_list_right_content p","click",function(){

    $(this).children("span").toggleClass("glyphicon-plus-sign");
    $(this).children("span").toggleClass("glyphicon-minus-sign");
    $(this).siblings("ul").toggleClass("s");

})
//url列表生成
function urllistappend(){
    $("p.url_load").show();

    var visioid=getCookie("id");
    $.get("http://www.realtoraccess.com/bi/geturls/",{userid:visioid},function(data){

        $(".url_list_right_content").html("");
        var obj= $.parseJSON(data);
        for(var key in obj){
            var p='<div> ' +
                '<p><span class="glyphicon glyphicon-plus-sign "></span>'+key+'</p> ' +
                '<ul  class="s" data-name='+key+'></ul></div>';
            $(".url_list_right_content").append(p);
            if( key=="未分类"){

                for(var index in obj[key]){
                    var li='<li class="urlli" data-id='+obj[key][index].urlid+' ' +
                        'data-url='+obj[key][index].url+' '+'data-name='+obj[key][index].urlname+' ' +
                        ''+'data-type='+key+'>'
                        +obj[key][index].urlname+''+obj[key][index].urlid+'<b class="s">×</b></li>';
                    ($(".url_list_right_content").find('ul[data-name='+key+']')).append(li);
                }
            }else{
                for(var index in obj[key]){
                    var li='<li class="urlli" data-id='+obj[key][index].urlid+' ' +
                        'data-url='+obj[key][index].url+' '+'data-name='+obj[key][index].urlname+' ' +
                        ''+'data-type='+key+'>'
                        +obj[key][index].urlname+'<b class="s">×</b></li>';
                    ($(".url_list_right_content").find('ul[data-name='+key+']')).append(li);
                }
            }
        }
        $(".url_load").hide();
    });

}
//移入移出，删除url；
$(".url_list_right_content").delegate("li","mouseenter",function(){
    $(this).children("b").show();
})
$(".url_list_right_content").delegate("li","mouseleave",function(){
    $(this).children("b").hide();
});
$(".url_list_right_content").delegate("li>b","click",function(){
    if (confirm('你确定要删除?')==true){
        $(this).parent("li").remove();
        var id=($(this).parent("li")).attr("data-id");
        $.post("http://www.realtoraccess.com/bi/delurl/",{urlid:id},function(data){
            //console.log(data)
            urllistappend()
        })
    }else{
        return false;
    }
})
//点击li
$(".url_list_right_content").delegate("li","click",function(){
    var list=$(".url_list_right_content").find($('li.urlli'));
    list.removeClass("urllihover");
    $(this).addClass("urllihover");
    var urlname=$(this).attr("data-name");
    var id=$(this).attr("data-id");
    var type=$(this).attr("data-type");
    $('input[name="urlname"]').val(urlname);
    $('input[name="urlname"]').attr("data-id",id);
    $('input[name="urltype"]').val(type);
    $('span.urlid').html("<b>ID：</b>"+id);
    initChart(id,"url_edior_echart",585,{});
    $(".url_edior_echart_tile").hide();
    $("#url_edior_echart").css("height","620px");
})


//允许编辑$
$(".url_edior_item").delegate(".urleid","click",function(){
    $(".url_edior_item input").removeAttr("disabled");
    $(this).html("保存");
    $(this).css("color","red");
    $(this).addClass("urlsave");
    $(this).removeClass("urleid");
});
//保存
$(".url_edior_item").delegate(".urlsave","click",function(){
    var name=$('input[name="urlname"]').val();
    var type=$('input[name="urltype"]').val();
    var id=$('input[name="urlname"]').attr("data-id");
    //console.log(name,type,id)
    $.post("http://www.realtoraccess.com/bi/updateurl/",{urlid:id,urlname:name,urltype:type},function(data){
        //console.log(data);
        urllistappend();
    })
    $(this).html("编辑");
    $(this).css("color","#314F60");
    $(".url_edior_item input").attr("disabled","disabled");
    $(this).addClass("urleid");
    $(this).removeClass("urlsave");
    $('.url_edior_class').hide();
});
//url模糊搜索
$('input[name="urltype"]').focus(function(){
    $('.url_edior_class').show();
    $.get("http://www.realtoraccess.com/bi/get/temptype/",function(data){
        var obj= $.parseJSON(data);
        var liHtml="";
        for(var key in obj){
            liHtml+='<p>'+obj[key]+'</p>'
        }
        $('.url_edior_class').html(liHtml);
    })
})
$('input[name="urltype"]').keyup(function(){

    var keyV=$('input[name="urltype"]').val();
    $.get("http://www.realtoraccess.com/bi/get/temptype/",{keyword:keyV},function(data){
        //console.log(data)
        var obj= $.parseJSON(data);
        var liHtml="";
        for(var key in obj){
            //console.log(obj[key])
            liHtml+='<p>'+obj[key]+'</p>'
        }
        $('.url_edior_class').html(liHtml);

    })
});

$('.url_edior_item').delegate(".url_edior_class p","click",function(){
    var v=$(this).html();
    $('input[name="urltype"]').val(v);
    $('.url_edior_class').hide();
})



/*************publish.html推送函数**************/
function modelShow(){
    // console.log(111)
    // console.log($("body").attr("id")=="publish")
    if($("body").attr("id")=="publish"){
        var urlidV=$("#publish").attr("data-num");
        console.log(urlidV);
        //initChart(idV,"allsvg",400,"1");
        var selclassdata0="";//分类
        var selclassval0="";//分类值



        var dataObj={
            selclassdata0:selclassdata0,
            selclasscompu0:"eq",
            selclassval0:selclassval0,
            chartid:""
        };
        console.log(dataObj);

        initChart(urlidV,"allsvg",400,{});

    }
}
$(function(){
    modelShow()
})