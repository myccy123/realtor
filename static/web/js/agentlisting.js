

 $('#header').load('http://www.realtoraccess.com/static/web/header.html',function(data){
		$("#header").html(data);
		 //地理定位
	//地理定位
 // $("#head_location").mouseover(function (){  
 //            $("#head_city").show();  
 //        }).mouseover(function (){  
 //            $("#head_city").show(); 
 //        }); 
 //     $("#head_city").mouseleave(function(){
	// 	    $(this).hide();
	// 	  });

		//房源搜索
		$("#head_nav2_1").mouseover(function(){
		    $(this).next().show();
		    });  
		$("#head_nav2_1").mouseleave(function(){
		    $(this).next().hide();
		    });  

		$("#head_nav2_1").next().mouseleave(function(){
		    $(this).hide();
		  });

		$("#head_nav2_1").next().mouseover(function(){
		    $(this).show();
		  });


		 // $("#head_land_img").click(function(){
		 //   $("#head_land").hide();

		 // })
		 //  $("#head_nav_land").click(function(){
		 //    $("#head_land").show();
		 //    return false;
		    
		 // })
		 // $("#head_login_img").click(function(){
		 //   $("#head_login").hide();

		 // })
		 //  $("#head_nav_login").click(function(){
		 //   $("#head_login").show();
		 //   return false;
		 // })

   //    $("#head_tologin").click(function(){
   //     $("#head_login").hide();
   //     $("#head_land").show();
   //     return false;
   //   })

   //    $("#head_tosignup").click(function(){
   //     $("#head_land").hide();
   //     $("#head_login").show();
   //     return false;
   //   })

	})
$('#footer').load('http://www.realtoraccess.com/static/web/footer.html')
$('#container_right').load('http://www.realtoraccess.com/static/web/sidelogo.html',function(data){
        $("#container_right").html(data)
        $("#weixinclick").hover(function(){  
            $("#serives").show();  
        },function(){  
            $("#serives").hide();  
        })

        $("#APPRAJ").hover(function(){  
            $("#APPxiazai").show();  
        },function(){  
            $("#APPxiazai").hide();  
        })  
         $("#top").click(function(){
          $("html,body").animate({scrollTop:0}, 500);
        });
})

// function addagents(page,rule,order){
// 	$.get('http://www.realtoraccess.com/web/get/agents/',{'page':page,'rule':rule,'order':order},function(data){
// 		setCookie('agentpage',currpage)
// 		reset_pages()
		
// 		var jsn = $.parseJSON(data)
// 		$(".listing").remove()
// 		for(var i=0;i<jsn.length;i++){
// 			var info = jsn[i].selfinfo
// 			info = info!=''?info:'瑞安居-海外房展第一门户！及时发布经纪人推广房源，足不出户即可获取经纪人为您推荐的海外生活动态资讯，手机下载即可与发布海外房源...'
// 			var div = '<div class="listing">\
// 				    <div class="agenttx">\
// 				    	<a href="/web/agent/'+jsn[i].id+'"><img src="'+jsn[i].head+'" alt="海外房产经纪人头像"></a>\
// 				    </div>\
// 				    <div class="agent_clas_tr">\
// 				           <a href="/web/agent/'+jsn[i].id+'"><h1>'+jsn[i].username+'</h1></a>\
// 				           <p class="agent_company">'+jsn[i].corp+'</p>\
// 				           <p class="agent_ad">'+jsn[i].note+'</p>\
// 				    </div>\
// 				    <div class="online">\
// 				       <p>'+info+'</p>\
// 				    	<div class="click_online">即时沟通</div>\
// 				    </div>\
// 				 </div>'
// 			$("#agentlisting_box").append(div)
// 		}
// 	})
// }

// var currule = 'integrity'
// var currthisorder = 'desc'

// if(getCookie('agentpage')){
// 	currpage = getCookie('agentpage')
// }

//addagents(currpage,currule,'desc')
// $(".orderby").eq(0).css('color','red')
// $(".orderby img").eq(0).attr('src','/static/web/images/orderdesc.png')

// $(".orderby").click(function(){
// 	var rule = $(this).attr('dataid')
// 	var currorder = $(this).attr('updown')
// 	var order = currule==rule?currorder=='desc'?'asc':'desc':'desc'
// 	currthisorder = order
// 	$(this).attr('updown',order)
	
// 	$(".orderby").css('color','#5d5d5d')
// 	$(this).css('color','red')
// 	$(".orderby img").attr('src','/static/web/images/order.png')
// 	$(this).children('img').attr('src','/static/web/images/order'+order+'.png')
	
// 	for(var i=0; i<lastpage; i++){
// 		if(i<4){
// 			$('.page').eq(i).text(i+1)
// 		}
// 	}
// 	$(".page").removeClass('selpage')
// 	$(".page").eq(0).addClass('selpage')
	
// 	addagents('1',rule,order)
// 	currpage = 1
// 	currule = rule
// })



// function getCookie(name)
// {
// 	var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
// 	if(arr=document.cookie.match(reg))
// 	return unescape(arr[2]);
// 	else
// 	return null;
// }

// function setCookie(name,value)
// {
// 	document.cookie = name + "="+ escape (value);
// }

var currpage = parseInt($(".pageclick").attr("currpage"))
var lastpage = parseInt($("#tip").attr('page'))
reset_pages()

$(".page").click(function(){
	currpage = parseInt($(this).text())
	jump()
	//addagents(currpage,currule,currthisorder)
})

$("#nextpage").click(function(){
   if(currpage == lastpage){
       return
   }
   currpage++
   jump()
   //addagents(currpage,currule,currthisorder)
})

$("#prevpage").click(function(){
	if(currpage == 1){
		return
	}
	currpage--
	jump()
	//addagents(currpage,currule,currthisorder)
})

$("#confirm").click(function(){
	var to = parseInt($("#ipt").val())
	currpage = to
	jump()
	//addagents(currpage,currule,currthisorder)
})

function jump(){
	urls = window.location.pathname.split('-')
	urls.pop()

	if(urls.length != 2){
		window.location.href = ''+currpage
	}else{
		urls.push(currpage+'')
		target = urls.join('-')
		window.location.href = target
	}
}

function reset_pages(){
	var ddd = '<span id="ddd" class="pagedot">...</span>'
	$(".pagedot").remove()
	
	if(lastpage > 5 && (currpage < lastpage -1 || (lastpage == 6 && currpage == 5))){
		$(ddd).insertAfter($(".page").eq(-1))
	}
	
	if(currpage > 5){
		$(ddd).insertAfter($(".page").eq(1))
		if(currpage != lastpage){
			$(".page").eq(2).text(currpage-1)
			$(".page").eq(2).attr('p',currpage-1)
			$(".page").eq(3).text(currpage)
			$(".page").eq(3).attr('p',currpage)
			$(".page").eq(4).text(currpage+1)
			$(".page").eq(4).attr('p',currpage+1)
		}else{
			$(".page").eq(2).text(currpage-2)
			$(".page").eq(2).attr('p',currpage-2)
			$(".page").eq(3).text(currpage-1)
			$(".page").eq(3).attr('p',currpage-1)
			$(".page").eq(4).text(currpage)
			$(".page").eq(4).attr('p',currpage)
		}
	}else{
		$(".page").eq(2).text(3)
		$(".page").eq(2).attr('p',3)
		$(".page").eq(3).text(4)
		$(".page").eq(3).attr('p',4)
		$(".page").eq(4).text(5)
		$(".page").eq(4).attr('p',5)
	}

	$(".page").removeClass('selpage')
	$("[p='"+currpage+"']").addClass('selpage')
}





$("#magnifying_glass").click(function(){
	var searchof = $("#search").val()
	$.get('http://www.realtoraccess.com/web/find/agent/',{'searchof':searchof},function(data){
		console.log(data)
		var jsn = $.parseJSON(data)
		$(".listing").remove()
		$(".pageclick").empty()
		$("#date").text(jsn.length)
		for(var i=0;i<jsn.length;i++){
			var info = jsn[i].selfinfo
			info = info!=''?info:'欢迎您来我的中文网站，我是一名专业的海外房产经纪人。在这里您将看到我的介绍，我所代理的特色房源和我的团队介绍，无论您是首次置业者...'
			var div = '<div class="listing">\
				    <div class="agenttx">\
				    	<a href="/web/agent/'+jsn[i].id+'"><img src="'+jsn[i].head+'"></a>\
				    </div>\
				    <div class="agent_clas_tr">\
				           <a href="/web/agent/'+jsn[i].id+'"><h1>'+jsn[i].username+'</h1></a>\
				           <p class="agent_company">'+jsn[i].corp+'</p>\
				           <p class="agent_ad">'+(jsn[i].note==''?'海外房产投资估价':jsn[i].note)+'</p>\
				    </div>\
				    <div class="online">\
				       <p>'+info+'</p>\
				    	<div class="click_online">即时沟通</div>\
				    </div>\
				 </div>'
			$("#agentlisting_box").append(div)
		}
	})
})
//即时沟通点击事件
// $('body').on('click','.click_online',function(){
// 	$(".agent_sm").show();
// })

// $("#sms").click(function(){
// 	$(".agent_sm").hide();
// })

