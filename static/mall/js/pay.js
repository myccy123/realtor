

$(".paylist").eq(-1).css("border","none")
$(".productlist").eq(-1).css("border","none")


$(".paylist").click(function(){
	$(".checktail img").attr("src","/static/mall/img/check_normal.png")
	$(this).find(".checktail img").attr("src","/static/mall/img/check_press.png")

})


//地址遮罩
$(".addr").click(function(){
	$(".zzc").show()
	return false
})

$(".confirm").click(function(){

	$.post('http://127.0.0.1:8000/mall/add/addr/',{uid:getCookie('uid') , recvname:$("#rname").val() , recvtel:$("#rtel").val() , addr:$(".typeaddr").val()},function(data){
		$.cookie('addrid', data, { expires: 30, path: '/' });
		$(".nametel").text($("#rname").val()+' '+$("#rtel").val())
		$(".addrdetail").text($(".typeaddr").val())
		$(".zzc").hide()
	})
	
})

$(".cancle").click(function(){
	$(".zzc").hide()
})

$(document).click(function(e){
	if($(e.target).closest(".addrtext").length == 0 && $(".zzc").css("display") != 'none'){
		$(".zzc").hide()
	}
})

function getsign(timestamp,pid){
	paysign = ''
	$.get("http://127.0.0.1:8000/mall/wechat_sign",{timestamp:timestamp,pid:pid},function(data){
		function onBridgeReady(){
		   WeixinJSBridge.invoke(
		       'getBrandWCPayRequest', {
		           "appId":"wxe530c431696402d0",     //公众号名称，由商户传入     
		           "timeStamp":timestamp,         //时间戳，自1970年以来的秒数     
		           "nonceStr":"yujiahao", //随机串     
		           "package":pid,     
		           "signType":"MD5",         //微信签名方式：     
		           "paySign":data //微信签名 
		       },
		       function(res){     
		           if(res.err_msg == "get_brand_wcpay_request:ok" ) {}  // 使用以上方式判断前端返回,微信团队郑重提示：res.err_msg将在用户支付成功后返回    ok，但并不保证它绝对可靠。 
		       }
		   ); 
		}

		if (typeof WeixinJSBridge == "undefined"){
		   if( document.addEventListener ){
		       document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
		   }else if (document.attachEvent){
		       document.attachEvent('WeixinJSBridgeReady', onBridgeReady); 
		       document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
		   }
		}else{
		   onBridgeReady();
		}
	})

}

function getCookie(name)
{
	var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
	if(arr=document.cookie.match(reg))
	return unescape(arr[2]);
	else
	return null;
}

//发起支付
$(".buy").click(function(){

	console.log($("#total_fee").text())
	$.post("http://127.0.0.1:8000/mall/prepay_id/",{openid : getCookie('uid') , total_fee : $("#total_fee").text()} ,function(data){

		var timestamp=new Date().getTime();
		timestamp = timestamp.toString().substring(0,10)
		p = "prepay_id=" + data
		getsign(timestamp,p)

	})
})







