var timestamp = new Date().getTime();
timestamp = timestamp.toString().substring(0, 10);
var url = window.location.href;
url = encodeURIComponent(url.split('#')[0]);
var signature;
var wxImgUrl = ''

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
            title: 'RealtorAccess – 海外房展第一门户', // 分享标题
            desc: '海外大牌经纪品牌网站，学区房、移民地产、楼花暗盘投资首选。', // 分享描述
            link: '', // 分享链接
            imgUrl: wxImgUrl, // 分享图标
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
            title: 'RealtorAccess – 海外房展第一门户；', // 分享标题
            link: '', // 分享链接
            imgUrl: wxImgUrl, // 分享图标
            success: function() {
                // 用户确认分享后执行的回调函数
            },
            cancel: function() {
                // 用户取消分享后执行的回调函数
            }
        });
    });
})