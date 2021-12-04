$(document).ready(function() {
    //下载页获取手机高度
    $("#downloadsite").css("height", screen.height + 'px')
    //$("#selfad").css("height",screen.width*0.6)

    var timestamp = new Date().getTime();
    timestamp = timestamp.toString().substring(0, 10)
    var url = window.location.href;
    url = encodeURIComponent(url.split('#')[0])

    var signature;
    var imgurl;
    var notes;
    notes = '瑞安居：海外房展第一门户 海外房源|便利分享|门户展示|即时沟通'

    if ($('body').attr('id') == 'listing') {
        imgurl = $('#slider img:first').attr('src')
    } else if ($('body').attr('id') == 'article') {
        imgurl = $('#atcimg').attr('src')
    } else if ($('body').attr('id') == 'mysite') {
        imgurl = $('#selfad img:first').attr('src')
        notes = $('#add').text()
    } else if ($('body').attr('id') == 'freeedit') {
        imgurl = 'http://www.realtoraccess.com/static/img/logo.png'
    }


    $.get('http://www.realtoraccess.com/weixin/jsapi/?timestamp=' + timestamp + '&url=' + url, function(data) {
        signature = data;
        wx.config({
            debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
            appId: 'wxcd1c7e6e724cc101', // 必填，公众号的唯一标识
            timestamp: timestamp, // 必填，生成签名的时间戳
            nonceStr: 'realter', // 必填，生成签名的随机串
            signature: signature, // 必填，签名，见附录1
            jsApiList: ['onMenuShareAppMessage', 'onMenuShareTimeline'] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
        });

        wx.ready(function() {
            wx.onMenuShareAppMessage({
                title: '', // 分享标题
                desc: notes, // 分享描述
                link: '', // 分享链接
                imgUrl: imgurl, // 分享图标
                type: '', // 分享类型,music、video或link，不填默认为link
                dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
                success: function() {
                    // 用户确认分享后执行的回调函数
                },
                cancel: function() {
                    // 用户取消分享后执行的回调函数
                }
            });
            wx.onMenuShareTimeline({
                title: '', // 分享标题
                link: '', // 分享链接
                imgUrl: imgurl, // 分享图标
                success: function() {
                    // 用户确认分享后执行的回调函数
                },
                cancel: function() {
                    // 用户取消分享后执行的回调函数
                }
            });
        });
    })
})

/*
var is_weixin = (function(){return navigator.userAgent.toLowerCase().indexOf('micromessenger') !== -1})();
var is_android = (function(){return navigator.userAgent.toLowerCase().indexOf('android') !== -1})();
window.onload = function() {
	var winHeight = typeof window.innerHeight != 'undefined' ? window.innerHeight : document.documentElement.clientHeight; //兼容IOS，不需要的可以去掉
	var btn = document.getElementById('applink');
	var tip = document.getElementById('weixin-tip');
	var close = document.getElementById('close');
	if (is_weixin && is_android) {
		btn.onclick = function(e) {
			tip.style.height = winHeight + 'px'; //兼容IOS弹窗整屏
			tip.style.display = 'block';
			return true;
		}
		close.onclick = function() {
			tip.style.display = 'none';
		}
	}
}*/

$(function() {
    $("#slider").excoloSlider({
        mouseNav: false,
        interval: 3000, // = 5 seconds
        playReverse: false

    });
});