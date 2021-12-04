
imgMiddle("#index_start_img img");//文字垂直居中
imgMiddle("#index_page3_img>img");
imgMiddle(".loading>img");

//makeW("#index_page1_box")
makeH("#index_page1_box");
makeH("#index_page2_box");
makeH("#index_page3_box");
makeH("#index_page4_box");
makeH("#index_page5_box");
makeH("#index_page6_box");
makeH("#index_page7_box");
makeH("#login section");
makeH("#registBack")

/********文字上下垂直居中******/
function imgMiddle(id){

    var h=$(window).outerHeight();
    var mh=$(id).height();
    //console.log(mh)
    $(id).height(mh)
    $(id).css("margin-top",(h-mh)/2);
    //console.log(h)
}


divMiddle("#regist_content","#registBack")
divMiddle(".deatilsaveSuccess",".selectpage")
//div上下垂直居中 .deatilsaveSuccess{
function divMiddle(zid,fid){
    var wh=$(window).outerHeight();
    var mh=$(zid).height();
    var fh=$(fid).height();
    $(fid).css("padding-top",(wh-mh)/2);
    $(fid).height(fh-(wh-mh)/2);
}
/********设置100%高度******/
function makeH(id){
    var h=$(window).outerHeight();
    $(id).height(h)
}
function makeW(id){
    var w=$(window).outerWidth();
    $(id).width(w)
}
/***************首页固定高度滚动************/
if($("body").attr("id")=="index"){
    if(isbounced==0){

        indexSrcoll();
        $('.box').css({'overflow': 'hidden'})
    }


}
function indexSrcoll() {
    var h = $(window).outerHeight();

    var bodyEl = $('html,body'); //ff和ie需要html，chrome需要body，万恶的兼容性啊

    var srollBtn = $('#index_sroll>li');

    var boxEl = $('.box');
    //console.log(boxEl.length)

    var boxIndex = 0; //定义一个变量保存上次滚动到的是第几个box
    // 隐藏页面滚动条并且初始化页面位置为顶部
    //bodyEl.scrollTop(0);
    bodyEl.css({'overflow': 'hidden'}).scrollTop(0);
    /**
     * 为按钮绑定事件
     * @returns {undefined}
     */
    srollBtn.click(function () {
        var btnIndex = $(this).index();

        var tarBoxTop = boxEl.eq(btnIndex).offset().top; //取得box的offset.top值
        //console.log( boxEl.eq(btnIndex))
        //console.log( tarBoxTop)
        var isAnimate = bodyEl.is(":animated"); //当前是否处于动画状态
        //console.log(isAnimate)
        var m = btnIndex - boxIndex; //算当前的按钮和当前显示的box的差值
        //如果是0就不操作于不是动画状态才执行
        if (m != 0 && !isAnimate) {
            //如果是1代表是临近的
            if (m == 1 || m == -1) {
                $(".slidshow").hide();
                $(".slidshow").slideDown(1000);
                bodyEl.animate({scrollTop: tarBoxTop}, 1000);
                //console.log(10)
            } else {
                $(".slidshow").hide();
                $(".slidshow").slideDown(1000);
                bodyEl.animate({scrollTop: tarBoxTop}, 1000);
                /*bodyEl.fadeOut(400);
                 //console.log(11)
                 setTimeout(function () {
                 bodyEl.fadeIn(400).scrollTop(tarBoxTop);
                 }, 400);*/
            }
            //改变右侧按钮的焦点
            $(srollBtn).removeClass('srollHover');
            $(this).addClass('srollHover');
            boxIndex = btnIndex;
            //console.log(15)
        }
    });

    /**
     * 鼠标滚轮触发后的事件
     */

    var mouseWheel = function (event) {
        if (!event) {
            event = window.event;
        }
        var delta = 0;//为了保存滚轮的滚动值
        var tarBoxTop = boxEl.eq(boxIndex).offset().top; //取得当前box的offset.top值

        var isAnimate = bodyEl.is(":animated"); //当前是否处于动画状态
        //取滚轮滚动的值
        if (event.wheelDelta) {
            delta = event.wheelDelta / 120;//兼容chrome
            if (window.opera) {//兼容opera
                delta = -delta;
            }
        } else if (event.detail) {
            delta = -event.detail / 3;//兼容ff
        }

        //判断是否弹框
        if(isbounced==0){
            //判断是向上滚还是向下

            if (delta > 0) {
                if (boxIndex != 0) {
                    if (!isAnimate) {
                        $(".slidshow").hide();
                        $(".slidshow").slideDown(1000);
                        bodyEl.animate({scrollTop: tarBoxTop - h}, 1000);
                        boxIndex--;
                    }
                }
            } else {
                if (boxIndex != (boxEl.length - 1)) {
                    if (!isAnimate) {
                        $(".slidshow").hide();
                        $(".slidshow").slideDown(1000);
                        bodyEl.animate({scrollTop: tarBoxTop + h}, 1000);
                        boxIndex++;
                    }
                }
            }

        }

        //改变右侧按钮的焦点
        $(srollBtn).removeClass('srollHover').eq(boxIndex).addClass('srollHover');
    };
    //绑定滚轮事件

    if (window.addEventListener) {
        window.addEventListener('DOMMouseScroll', mouseWheel, false); //火狐和IE
    }
    window.onmousewheel = document.onmousewheel = mouseWheel; //chrome});




    /*****************************返回顶部******************************/

    $(window).scroll(function () {
        if ($(window).scrollTop() >= ($(window).outerHeight() - 10)) {
            $('#backUp').show();
        } else {
            $('#backUp').hide();
        }
        if ($(window).scrollTop() > ($("body").height() - $(window).height() - $("#footerbox").height())) {
            $('#backDown').hide();
        }
        else {
            $('#backDown').show();
        }
    })
    $('#backUp').click(function () {
        $('body,html').animate({'scrollTop': '0px'}, 1000);
        boxIndex = 0;
        $(srollBtn).removeClass('srollHover');
        $('[data-num="index_page1"]').addClass('srollHover');
    })
    $('#backDown').click(function () {
        $('body,html').animate({'scrollTop': $("body").height() + 'px'}, 1000);
        boxIndex = 7;
        $(srollBtn).removeClass('srollHover');
        $('[data-num="index_page8"]').addClass('srollHover');
        $('#backDown').hide();
    })
}


//首页微信图标
$('.ewm a').hover(function(){
    $(this).siblings('.ewmIcon').css('display','block');
},function(){
    $(this).siblings('.ewmIcon').css('display','none');
})



$(window).ready(function(){
    //console.log(document.cookie)
    hasLogin();
    indexAddData.init();
    nav.init();
    login.init();
    regist.click();
    regist.blur();
    //console.log(document.cookie);

    if($("body").attr("id")=="matchMysql"){
        $.get("http://www.realtoraccess.com/bi/haslogin/", function (data) {
            hasLogined=data;
            //console.log(hasLogined)
            if(hasLogined=="1"){
                addOption("#mysqle_permiss");//macthMysql select权限生成
            }
        })
    }
    if($("body").attr("id")=="macthexcel"){
        $.get("http://www.realtoraccess.com/bi/haslogin/", function (data) {
            hasLogined=data;
            console.log(hasLogined)
            if(hasLogined=="1"){
                addOption("#excel_permiss");//macthMysql select权限生成
            }
        })
    }
    if($("body").attr("id")=="detail"){
        appendChartOption();//增加detail页面selcet生成option
        laydate.skin('molv');;//时间插件


    }
    if($("body").attr("id")=="system"){
        dataTreeAppend();//增加system页面数据树生成数据片段

    }

    modelShow()//echart推送；
    chartSaveStage=0;//保存状态
    clearInterval(timer);
})