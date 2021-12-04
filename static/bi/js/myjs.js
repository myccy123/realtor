/**
 * Created by hp on 2016/6/30.
 */
var dbValue;    //mysql 数据树
var tabValue;   //mysql 数据树
var idmun=0;     //detail select id
var classNameNum=0; //筛选项num
var chartSaveStage=0;//detail.html chart 是否在保存状态；
var  filepath="";      //echart引用路径；
var  ctype="";         //echart图表类型；
var indexShowHtml;// 操作区域代码片段；
var newindexShowHtml;//去分号操作区域代码片段；
var dataV;          //detail echart,路径
var ctypeV;         //detail echart,类型
var boxID="";       //echart,id
var  boxidn=0;      //echart,id ++变量
//var newbodyId;      //生成新页面的ID（slice获取）
var allVaule="";       //detail，全局chang键值对(detailChartPost(url,e))；
var timer=null      //定时器
var funcBooLen="false";   //判断函数是否执行完毕
var hasLogined=0; //判断登陆状态，
var isbounced=0;//判断
var echartstarttime;//开始时间
var echartendtime;//结束时间
/**********************************************************弹框******************************************************/
var indexAddData={

    init:function(){
            $("#index_addData").load("http://www.realtoraccess.com/static/bi/addDataBounced.html",function(data){
                $("#index_addData").html(data);
                //nav点击添加数据
                $("#navbox").delegate("#index_add_btn","click",function(e){
                    ($("#index_addData").find(".index_dataItem")).html("");
                    isbounced=1;
                    e.preventDefault();
                    /****************弹出框生成select******************/
                    $.get("http://www.realtoraccess.com/bi/get/sourcename/", function (data) {
                        var obj = $.parseJSON(data);
                        //console.log(data)
                        for (var key in obj) {
                            ($("#index_addData").find(".index_dataItem")).append('<p class="col-xs-12" ' +
                                'data-value="' + obj[key].sourceid + '">'+'<span>' +
                                obj[key].sourcetype+'</span>' + obj[key].sourcename + '</p>')
                        }
                        $("#index_addData").show();
                        //console.log(isbounced)
                        indexAddData.fuzzySearch();
                        indexAddData.selectDate();
                        indexAddData.exitBounced();
                        indexAddData.OkToDeitail();
                    })

                })
            })

        },
    /*模糊搜索监听*/
    fuzzySearch:function(){
        $("#index_addData").delegate("#madule_selectType","keyup",function(){
            var  keywordV=$(this).val();
            $.get("http://www.realtoraccess.com/bi/get/sourcename/",{keyword:keywordV}, function (data) {
                var obj = $.parseJSON(data);
                ($("#index_addData").find(".index_dataItem")).html("")
                for (var key in obj) {
                    ($("#index_addData").find(".index_dataItem")).append('<p class="col-xs-12" ' +
                        'data-value="' + obj[key].sourceid + '">'+'<span>' +
                        obj[key].sourcetype+'</span>' + obj[key].sourcename + '</p>')
                }
            })
        })
    },
    /***选择数据流发送生成数据流详情****/
    selectDate:function(){
        $("#index_addData ").delegate("div.index_dataItem>p","click",function(){

            $("#index_addData ").find("div.index_dataItem>p").removeClass("dataItemActivehover")
            $(this).addClass("dataItemActivehover");

            var v=($(this).html()).slice("14");

            ($("#index_addData ").find("#madule_selectType")).val(v);
            postSourceId("http://www.realtoraccess.com/bi/get/sourceinfo/");
            function postSourceId(URL){
                var sourceidV=$(".dataItemActivehover").attr("data-value");

                $.post(URL,{sourceid:sourceidV},function(data){
                    console.log(data)

                    var obj= $.parseJSON(data);
                    $("#index_model_usrname>span:first-child").css("backgroundImage","url("+obj.srcownerhead+")");
                    $("#index_model_usrname>span:nth-child(2)").html(obj.srcowner);
                    $("#mysqltable_count").html(obj.count);
                    $("#mysqltable_size").html(obj.size);
                    $("#mysqltable_time").html(obj.update);
                    $("#mysqltable_tablename").html(obj.tabname);
                    $("#mysqltable_Date>ul").html("")
                    $("#mysqltable_Text>ul").html("")
                    $("#mysqltable_Number>ul").html("")

                    if(obj.text.length>0){

                        var hv1="";
                        for (var key in obj.text){

                            hv1+="<li class='padding_toporbottom_10'>"+obj.text[key]+"</li> ";

                        }
                        $("#mysqltable_Text>ul").html(hv1);
                    }
                    if(obj.date.length>0){
                        var hv2="";
                        for (var key in obj.date){
                            hv2+="<li class='padding_toporbottom_10'>"+obj.date[key]+"</li> ";
                        }
                        $("#mysqltable_Date>ul").html(hv2);
                    }
                    if(obj.num.length>0){
                        var hv3="";
                        for (var key in obj.num){
                            hv3+="<li class='padding_toporbottom_10'>"+obj.num[key]+"</li> ";
                        }
                        $("#mysqltable_Number>ul").html(hv3);
                    }
                })
            }
        })
    },
    /*****隐藏弹窗*********/
    exitBounced:function(){
        $("#index_addData ").delegate("#index_modlue_hiden_btn","click",function(){
            $("#index_addData").css("display","none");
            isbounced=0;
        })
    },
    /******跳转到detail******/
    OkToDeitail:function(){
        $("#index_addData ").delegate("#index_modlue_okbtn","click",function(){
            window.location.href="http://www.realtoraccess.com/bi/add/chart/";
            isbounced=0;
        })
    }
}
 /**********************************************************↑弹框******************************************************/

/**返回首页**/
$("#usercenter_backInDEX").click(function(){
    window.location.href="http://www.realtoraccess.com/";
})
$("#regist_tologin_btn").click(function(){
    window.location.href="http://www.realtoraccess.com/";
})

/********************************************************login regist*******************************************************************/

/*****************************nav加载******************************/
var nav={
    init:function(){
        $("#navbox").load("http://www.realtoraccess.com/static/bi/nav.html",function(data){
            $("#navbox").html(data);
            $("#navbox").find($("#welcomeUser")).hide();
            $("#navbox").find($("#userImg")).hide();
            $("#navbox").find($("#nav_quit_btn")).hide();
            /*导航切换*/
            $("#navbox").delegate("li.nav_ul_a_item>a","click",function(){
                $("#navbox").find($("li.nav_ul_a_item>a")).removeClass("nav_ul_hover");
                $(this).addClass("nav_ul_hover");

            })


            if($("body").attr("id")=="login"||
                $("body").attr("id")=="regist"){

                $("#navbox").find($("#nav_login_btn")).hide();
                $("#navbox").find($("#nav_quit_btn")).hide();
                $("#navbox").find($("#visoRegist")).hide();
            }else{
                $.get("http://www.realtoraccess.com/bi/haslogin/", function (data) {
                    hasLogined=data;
                    // console.log(hasLogined)
                    //打开或者刷新浏览器，首页记忆登陆
                    if((hasLogined=="1")){
                        $("#navbox").find($("#index_loginTip")).hide();
                        $("#navbox").find($("#index_matchDta")).show();
                        $("#navbox").find($("#index_add_btn_btn")).show();
                        $("#navbox").find($("#nav_sys_btn")).show();
                        nameImg()
                        nav.exitClick();


                    }


                })


            }
        });
    },

    //退出登录
    exitClick:function(){
        $("#navbox").delegate("#nav_quit_btn","click",function(){
            $.get("http://www.realtoraccess.com/bi/logout/",function(data){
                if(data=="0"){
                    window.location.href="http://www.realtoraccess.com/bi/login/";
                    quitShow();
                    hasLogin();
                }
            })
        })
    },

};
/***********判断是否登录**************/
function hasLogin() {
        $.get("http://www.realtoraccess.com/bi/haslogin/", function (data) {
            hasLogined=data;
        })
}
function hasLoginExit() {
    if($("body").attr("id")!=="login"||$("body").attr("id")!=="regist"){
        $.get("http://www.realtoraccess.com/bi/haslogin/", function (data) {
            hasLogined=data;
            if(hasLogined=="0"){
                window.location.href="http://www.realtoraccess.com/bi/login/";
            }
        })
    }

}

/*退出后显示注册和登录*/
function quitShow(){
    if(getCookie("id")){
        $("#navbox").find($("#nav_login_btn")).css("display","block");
        $("#navbox").find($("#visoRegist")).css("display","block");
        $("#navbox").find($("#nav_quit_btn")).css("display","none");
        $("#navbox").find($("#welcomeUser")).css("display","none");
        $("#navbox").find($(".user_logined_name")).html("");
        $("#navbox").find($(".nav_logined_img")).css({
            "background":"none",
            "width":"0","padding":"0"
        });
    }
}
/*名称头像退出显示，登录注册隐藏*/
function nameImg(){

    $("#navbox").find($("#welcomeUser")).show();
    $("#navbox").find($("#userImg")).show();
    $("#navbox").find($("#nav_quit_btn")).show();
    $("#navbox").find($("#nav_login_btn")).hide();
    $("#navbox").find($("#visoRegist")).hide();
    var $name=$("#navbox").find($("#welcomeUser span"))
    $name.html(getCookie("username"))

    var head=getCookie("head")
    $("#navbox").find($(".nav_logined_img")).css({
        "display":"block",
        "width":"30px",
        "height":"30px",
        "border-radius":"50%",
        "background":"url("+head+") no-repeat center center",
        "background-size": "contain"
    });
}
/****************************登录******************************/
var login={
    //初始登录
    init:function(){
        $(".login_delv").click(function(){
            var loginV=$("#loginForm").serialize()
            //console.log(loginV)
            $.post("http://www.realtoraccess.com/web/signin/",loginV,function(data){
                console.log (data)
                var obj= $.parseJSON(data)
                if(obj['rescode']!="0"){
                    $(".login_error_tip").show();
                }else{
                    $(".login_delv").val("登录中...")

                    if( $("#login_rad").is(':checked')){
                        setCookie("headimg",'');
                        var name=$('[name="userid"]').val();
                        var value=$('[name="passwd"]').val()
                        setCookie("id",loginV['userid']);
                        setCookie("visioUser",name);
                        setCookie("visioPsw",value);
                        hasLogin()
                        nameImg();
                    }
                    // console.log(document.cookie)
                    window.location.href="http://www.realtoraccess.com/bi/";
                }
            })
        })
    },
    /*登录页 记录密码后登陆页*/
    remberpsw:function(){
        if(getCookie("visioUser")){
            $('[name="user"]').val(getCookie("visioUser"));
            $('[name="psw"]').val(getCookie("visioPsw"));
            $("#login_rad").attr("checked",true);
            hasLogin();
            login.logined="ture";
        }
    },

}


/***************JS操作cookies方法!*******************/
// 写cookies
function setCookie(name,value) {
     var Days = 30;
     var exp = new Date();
     exp.setTime(exp.getTime() + Days*24*60*60*1000);
     document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString() + ";domain=realtoraccess.com";
 }
//读取cookies
function getCookie(name) {
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg)){
        return unescape(arr[2]).replace(/\"/g, "");
    }else{ return null;}
}

/**********************************regist.html**********************************/
/****注册表单******/
var regist={
    //提交表单验证
    click:function(){
        $("#regist_form button").click(function (){
            regist.serverTest()
        })
    },
    //失去焦点验证
    blur:function(){
        regist.webTest();
    },
    //客户端验证 提交是否禁用
    webTest:function(){
        var userv="";
        var pswv="";
        var rpswv="";
        var emailv="";
        var checkv=false;

        function submitTest(){
            if(userv==""||pswv==""||rpswv==""||emailv==""||checkv==false){
                $("#reg_submit_btn").attr("disabled","disabled")
                $("#reg_submit_btn").css("background","#9e9e9e")
            }else {
            $("#reg_submit_btn").css("background","#5bc0de")
                $("#reg_submit_btn").removeAttr("disabled")
            }
        }
        $("#name2").blur(function(){
            userv=$("#name2").val()
            submitTest()
            if($("#name2").val()!==""){
                /*正则验证呢*/
            }
        })
        $("#pwd1").blur(function(){
            pswv=$("#pwd1").val()
            submitTest()
            if($("#pwd1").val()!==""){
                /*正则验证呢*/
            }

        })
        $("#pwd2").blur(function(){
            rpswv=$("#pwd2").val()
            submitTest()
            if($("#pwd2").val()!==""){
                /*正则验证呢*/
            }

        })
        $("#email").blur(function(){
            emailv=$("#email").val()
            submitTest()
            if($("#email").val()!==""){
                /*正则验证呢*/
            }
        })
        $("#reg_check").click(function(){
            checkv=$("#reg_check").is(":checked")
            submitTest()
        })
    },
    //服务器验证
    serverTest:function(){
        var values=$("#regist_form").serialize();
        //console.log(values)
        $.post("http://www.realtoraccess.com/account/signupdata/",values,function(data){
                //console.log(data)
                $("#regist_form div.padding_zero span.help-block").html("必填*")
                if(data=="ok"){
                    $("#regist_suc").fadeIn();
                }else if(data=="user"){
                    $("#regist_user").html("!用户名存在")
                }else if(data=="email->Enter a valid email address.|||"){
                    $("#regist_email").html("!邮箱格式不正确")
                }else if(data=="repwd"){
                    $("#regist_rpsw").html("!两次密码输入不一致")
                }

            }
        )
    }

}

$("body").on("click",".selfpage",function(){
    console.log(getCookie('id'))
    $(this).attr('href','/web/agent/?userid='+getCookie('id'));
    return true;
})


/**********************************userCenter.html**********************************/
/*************个人中心发送修改*****************/
$("#userCenter_editSve").click(function(){
    var values=$("#userCenter_editFORM").serialize();

    $.post("http://www.realtoraccess.com/account/selfdata/",values,function(data){
        //console.log(data);
    })
})

/**************加群组*********************/

$("#add_tankuang01").click(function(e){
    e.preventDefault();
    $("#user_right_addTeam").fadeIn();
})
$("#user_right_addTeam button").click(function(){
    var Tname=$("#user_right_addTeam input").val();
    $(".user_right_overflowBox").append('<div class="row col-md-4 col-sm-6  col-xs-12 coleveryTD zero">' +
        ' <div class="user_right_zu_zutubiao col-xs-6"> </div> <div class="col-xs-6  margin_left_zero padding_zero "> ' +
        '<span class="fourtyCenter">'+Tname+'</span> </div> </div>')
    $("#user_right_addTeam").fadeOut();
})
/*******************加好友********************/
$("#add_tankuang02").click(function(e){
    e.preventDefault();
    $("#user_right_addFrend").fadeIn();
})
$("#user_right_addFrend button").click(function(){
    var Tname=$("#user_right_addFrend input").val();
    $("#user_fre_add").append('<div class="row col-md-4 col-sm-6  col-xs-12 coleveryTD zero">' +
        ' <div class="user_right_zu_zutubiao col-xs-6"> </div> <div class="col-xs-6  margin_left_zero padding_zero "> ' +
        '<span class="fourtyCenter">'+Tname+'</span> </div> </div>')
    $("#user_right_addFrend").fadeOut();
})


/*************显示删除并修改*****************/
$("#user_add_team .coleveryTD").click(function(){
    //console.log($(this))
    $(".coleveryTD").css("border","1px solid transparent");
    $(this).css("border","1px solid red");
    $("#edit_user_team").css("display","block");
    $("#delet_user_team").css("display","block");
})


/**************个人中心与群组切换************************/
$("#user_left_toggl p[data-num]").click(function(){
    //console.log($(this).attr("data-num"))
    $("#user_left_toggl p[data-num]").removeClass("userCenter_active");
    $(this).addClass("userCenter_active");
    if($(this).attr("data-num")=="2"){
        $("#userCenter_right_form>div").fadeOut();
        $("#user_group_tip").fadeIn();
        /*//$("#user_left_toggl p:nth-child(4) span").css("background",'url("http://www.realtoraccess.com/static/bi/images/zu_white_icon.png") no-repeat 25px center');
        $("#user_left_toggl p:nth-child(4) span").css("color",'#fff')
        //$("#user_left_toggl p:nth-child(3) span").css("background",'url("http://www.realtoraccess.com/static/bi/images/gerenxinxi_gray_icon.png") no-repeat 30px center');
        $("#user_left_toggl p:nth-child(3) span").css("color",'#8c8c8c')*/
    }else if($(this).attr("data-num")=="1"){
        $("#userCenter_right_form>div").fadeOut();
        $("#user_center_tip").fadeIn();
        /*//$("#user_left_toggl p:nth-child(4) span").css("background",'url("http://www.realtoraccess.com/static/bi/images/zu_gray_icon.png") no-repeat 25px center');
        $("#user_left_toggl p:nth-child(4) span").css("color",'#8c8c8c')
        //$("#user_left_toggl p:nth-child(3) span").css("background",'url("http://www.realtoraccess.com/static/bi/images/gerenxinxi_white_icon.png") no-repeat 30px center');
        $("#user_left_toggl p:nth-child(3) span").css("color",'#fff')*/
    }
})

/****************************mysql.html***********************************/
/****下一步btn取消禁用****/
function nextStepNoDisabled(){
    var mysqle_dataSource=$("#mysqle_dataSource");
    var mysqle_permiss=$("#mysqle_permiss").val();
    var mysqle_ip=$("#mysqle_ip").val();
    var mysqle_user=$("#mysqle_user").val();
    var mysqle_psw=$("#mysqle_psw").val();
    var mysqle_port=$("#mysqle_port").val();
    if(mysqle_dataSource==""||mysqle_permiss==""||mysqle_ip==""||mysqle_user==""||mysqle_psw==""||mysqle_port==""){
        $("#mysql_submit").attr("disabled","disabled")
        $("#mysql_submit").css("background","#708999")
    }else {
        $("#mysql_submit").css("background","#11C756")
        $("#mysql_submit").removeAttr("disabled")
    }
}

$("#mysqle_dataSource").blur(function(){
    var mysqle_dataSource=$("#mysqle_dataSource").val();
    nextStepNoDisabled()
    if($("#mysqle_dataSource").val()!==""){
        /*正则验证呢*/
    }
})
$("#mysqle_permiss").blur(function(){
    var mysqle_dataSource=$("#mysqle_permiss").val()
    nextStepNoDisabled()
    if($("#mysqle_permiss").val()!==""){
        /*正则验证呢*/
    }
})
$("#mysqle_ip").blur(function(){
    var mysqle_dataSource=$("#mysqle_ip").val()
    nextStepNoDisabled()
    if($("#mysqle_ip").val()!==""){
        /*正则验证呢*/
    }
})
$("#mysqle_user").blur(function(){
    var mysqle_dataSource=$("#mysqle_user").val()
    nextStepNoDisabled()
    if($("#mysqle_user").val()!==""){
        /*正则验证呢*/
    }
})
$("#mysqle_port").blur(function(){
    var mysqle_dataSource=$("#mysqle_port").val()
    nextStepNoDisabled()
    if($("#mysqle_port").val()!==""){
        /*正则验证呢*/
    }
})
$("#mysqle_psw").blur(function(){
    var mysqle_dataSource=$("#mysqle_psw").val()
    nextStepNoDisabled()
    if($("#mysqle_psw").val()!==""){
        /*正则验证呢*/
    }
})


/***mysql表单post***/
$("#mysql_submit").click(function(){
    $(".loading").show();
    postMysqlForm();
})

$("#mysql_ok").click(function(){
    $(".loading").show();

    //var values=$("#mysql_form").serialize();
    var checkv=$("#mysqle_timely").attr("checked");
    var values=($("#mysql_form").serialize())+"&checked="+checkv;
    //console.log(values);
        newValues=values+"&db="+dbValue+"&tab="+tabValue;
    $("#mysql_ok").attr("disabled","disabled")
    $("#mysql_ok").css("background","#708999")
    $("#mysql_ok").val("配置数据中....");
    $.post("http://www.realtoraccess.com/bi/conf/dbtab/", newValues,function(data,status){
        //console.log(data,status);
        $("#mysql_name").html( $("#mysql_name").html()+"<li>"+$("#mysqle_dataSource").val()+"</li>");
        if(status=="success"){
            $('.loading').hide();
        }
        window.location.reload();
    })
})

function postMysqlForm(){
    var checkv=$("#mysqle_timely").attr("checked");
    //console.log(checkv);
    var values=($("#mysql_form").serialize())+"&checked="+checkv;
    //console.log(values)



    $("#mysql_submit").attr("disabled","disabled")
    $("#mysql_submit").css("background","#708999")
    $("#mysql_submit").html("开始加载数据库...")

    $.post("http://www.realtoraccess.com/bi/conf/connstr/",values,function(data,status){
        // console.log(data,status);
        var obj = $.parseJSON(data);
        //console.log(obj);
                var i=0;
                for (var key in obj) {
                    //console.log(key);
                    if(obj[key].length>0) {
                        $(".mysqle_treeBox").append('<ul><li data-num="'+key+'"'+'><p><span class="glyphicon glyphicon-plus"></span><lable >' + key + '</lable></p></li></ul>')
                        for (var index in obj[key]) {
                            $(".mysqle_treeBox").children().children('li:eq('+i+')').append('<ul  class="none"><li><p>' + obj[key][ index] + '</p></li></ul>')
                        }
                    }else{
                        $(".mysqle_treeBox").append('<ul><li><p><lable>' + key + '</lable></p></li></ul>')
                    }
                    i++;
                    $(".dataStepForm").hide();
                    $(".step1").css("background","url('http://www.realtoraccess.com/static/bi/images/step1w.png') no-repeat center center")
                    $(".step2").css("background","url('http://www.realtoraccess.com/static/bi/images/step2w.png') no-repeat center center")
                    $("#mysqle_tree").show();
                }
        if(status=="success"){
            $('.loading').hide();
        }

    })
}
//*****************数据流删除************************//

$("#mysql_name").delegate("li","mouseenter",function(){

    $(this).children("b").show();
    $(this).css({background:"#11C756"})
    $(this).children("span,p").css({color:"#fff"});

})
$("#mysql_name").delegate("li","mouseleave",function(){

    $(this).children("b").hide();
    $(this).css({background:"none"})
    $(this).children("span,p").css({color:"#748693"});
})
$("#mysql_name").delegate("b","click",function(){

    if (confirm('你确定要删除?')==true){
        var sourceidV=$(this).parent("li").attr("data-id");
        var $targetli=$(this).parent()
        $.post("http://www.realtoraccess.com/config/delsource/",{sourceid: sourceidV},function(data){
            //console.log(data);
            if(data=="ok"){
                //console.log(1)
                //console.log($(this).parent())
                $targetli.slideUp();
            }
        })
    }else{
        return false;
    }

});
//addexcel 数据流删除
$(".excel_source_list").delegate("li","mouseenter",function(){

    $(this).children("b").show();
    $(this).css({background:"#11C756"});
    $(this).children("span,p").css({color:"#fff"});

})
$(".excel_source_list").delegate("li","mouseleave",function(){

    $(this).children("b").hide();
    $(this).css({background:"none"})
    $(this).children("span,p").css({color:"#748693"});
})
$(".excel_source_list").delegate("b","click",function(){

    if (confirm('你确定要删除?')==true){
        var sourceidV=$(this).parent("li").attr("data-id");
        var $targetli=$(this).parent()
        $.post("http://www.realtoraccess.com/config/delsource/",{sourceid: sourceidV},function(data){
            //console.log(data);
            if(data=="ok"){
                //console.log(1)
                //console.log($(this).parent())
                $targetli.slideUp();
            }
        })
    }else{
        return false;
    }

});
/*************mysqle_tree折叠*************/
$(".mysqle_treeBox").click(function(e){
    //console.log($(e.target));
    if( $(e.target).is("p")){
            $(e.target).siblings().toggleClass('none');
            $(e.target).children("span").toggleClass("glyphicon-minus");
            if(!($(e.target).parent().parent().parent().is("div"))){
                //$(e.target).parent().parent().siblings("ul").removeClass("mysqltreehover");
                $(".mysqle_treeBox ul").removeClass("mysqltreehover");
                $(e.target).parent().parent().addClass("mysqltreehover");
                tabValue=$(".mysqltreehover").children().children("p").html();
                dbValue=$(".mysqltreehover").siblings("p").children("lable").html();

                if($(".mysqle_treeBox").find(".mysqltreehover").length){
                    //console.log( $(".mysqle_treeBox").find(".mysqltreehover"))

                    $("#mysql_ok").removeAttr("disabled");
                    $("#mysql_ok").css("background","#11C756");
                }

            }
    }else if( $(e.target).is("span")){
            $(e.target).parent().siblings().toggleClass('none');
            $(e.target).toggleClass("glyphicon-minus");
    }
})


/***select权限生成***/
function addOption(id){
    $.get("http://www.realtoraccess.com/bi/get/perm/",function(data){
        var obj = $.parseJSON(data);
        console.log(obj)
        if( !$(id).html()){
            for(var key in obj){
                $(id).append('<option value="'+key+'">'+obj[key]+'</option>')
            }
        }
    })
}
/********************************excel***************************************/
//获取文件名称
$(".excel_input_submit").change(function(){

    var file = $(".excel_input_submit").val();
    var fileName = getFileName(file);

    $(".excel_input_file>span").html(fileName)
    var soutceName=$("#excel_dataSource").val();

    if(!soutceName){
        $("#excel_dataSource").val(fileName);
    }

})
//获取文件名称正则
function getFileName(o){
    var pos=o.lastIndexOf("\\");
    return o.substring(pos+1);
}


/****************************↑mysql.html***********************************/























