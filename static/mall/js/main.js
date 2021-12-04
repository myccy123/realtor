
function getCookie(name)
{
	var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
	if(arr=document.cookie.match(reg))
	return unescape(arr[2]);
	else
	return null;
}

function setCookie(cname,cvalue)
{
  var d = new Date();
  d.setTime(d.getTime()+(50*60*1000));
  var expires = "expires="+d.toGMTString();
  document.cookie = cname + "=" + cvalue + "; domain=/" ;
}


$(".addr").click(function(){
	if(getCookie('uid').length > 1){

		$(".zzc").show()
		return false
	}else{
		jump_wechat_login()
	}

	
})

$(".confirm").click(function(){
	$.post('http://127.0.0.1:8000/mall/add/addr/',{uid:getCookie('uid') , recvname:$("#rname").val() , recvtel:$("#rtel").val() , addr:$(".typeaddr").val()},function(data){
		$.cookie('addrid', data, { expires: 30, path: '/' });
		$("#address").text($("#rname").val()+' '+$("#rtel").val()+' '+$(".typeaddr").val())
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

function jump_wechat_login(){
	url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxe530c431696402d0&redirect_uri="+window.location.href+"&response_type=code&scope=snsapi_userinfo&state=yujiahao"
	window.open(url)
}

$(".userinfo").click(function(){
	jump_wechat_login()
})


$(".buy").click(function(){
	if(getCookie('uid').length > 1){

		$.cookie('set_id', $("#selset").attr('setid'), { expires: 30, path: '/' });
		alert(getCookie(set_id))
		return true

	}else{
		jump_wechat_login()
	}
})
