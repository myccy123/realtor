

$('#header').load('http://www.realtoraccess.com/static/web/header.html',function(data){
		$("#header").html(data);
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

var polllen = $(".small_ul").children().length
var rcnt = polllen-2
var lcnt = 0

$("#small_right").click(function(){
	if(rcnt > 0){
		var passed = $(".small_center")
		passed.prev().hide()
		passed.removeClass()
		passed.addClass('small_f_l lifirst')
		passed.next().addClass('small_center')
		rcnt--
		lcnt++
	}
})

$("#small_left").click(function(){
	if(lcnt > 0){
		var passed = $(".small_center")
		passed.prev().prev().show()
		passed.prev().removeClass()
		passed.prev().addClass('small_center')
		passed.removeClass()
		passed.addClass('small_f_l lilast')
		rcnt++
		lcnt--
	}
})

$(".small_li").click(function(){
	var img = $(this).children().first().clone()
	$("#big_houseimg").empty()
	$("#big_houseimg").append(img)
})

$(function(){
	var img = $(".small_ul").children().first().children().first().clone()
	$("#big_houseimg").empty()
	$("#big_houseimg").append(img)
})


//recommend listing
// $(function(){
// 	$.getJSON('http://www.realtoraccess.com/web/rcmd/listing', function(data){
// 		for(var i=0; i< data.length; i++){
			
// 			div1 = '<div class="li_house" id="houseone">\
// 				<a href="/web/listing1/?mls='+data[i].mls+'"><img src="'+data[i].img+'"></a>\
// 				<p><span class="house_city">'+data[i].city+'</span><span class="house_price">'+data[i].price+'</span></p>\
// 				<p class="house_type">'+data[i].housetype+'</p>\
// 				<p class="house_address">'+data[i].addr+'</p>\
// 				<p class="turnover_time">'+data[i].date+'</p>\
// 				</div>'
			
// 			$("#house_recommend").append(div1)
// 		}
// 		});
// })

//房源推荐

$(function(){
	$.getJSON('http://www.realtoraccess.com/web/rcmd/listing', function(data){
		for(var i=0; i< data.length; i++){
			
			div1 = '<div class="share_box_2two">\
                           <div class="abovetwo">\
		                <div id="housepicturetwo"><a href="/web/listing1/'+data[i].mls+'"><img src="'+data[i].img+'"\
		               alt="mls"></a></div>\
		                <div class="informationtwo">\
		                   <p id="pricetwo">&nbsp'+data[i].price+'|&nbsp'+data[i].areas+'</p>\
		                   <p id="adddresstwo">'+data[i].city+'/'+data[i].housetype+'</p>\
		                </div>\
		           </div>\
		           <div class="page_viewtwo">\
		              <p class="readingtwo"><img src="/static/web/images/reading.png">'+data[i].visit+'</p>\
		              <p class="datetwo">'+data[i].date+'</p>\
		           </div>\
		         </div>'
			
			$("#box_2two").append(div1)
		}
		});
})



//
////recommend news
//$(function(){
//	$.getJSON('http://www.realtoraccess.com/news/rcmd/news', function(data){
//		for(var i=0; i< data.length; i++){
//			div1 = '<div class="news_li">\
//			<a href="/news/'+data[i].aid+'"><img src="'+data[i].img+'"></a>\
//			<div class="news_box">\
//			<a href="/news/'+data[i].aid+'"><p class="news_">'+data[i].title+'</p></a>\
//			<p class="news_time">'+data[i].date+'</p>\
//			</div>\
//		</div>'
//			
//			$("#house_news").append(div1)
//		}
//		});
//})


function GetQueryString(name)
{
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null)return  unescape(r[2]); return null;
}
var mls = $("body").attr('mls')

$("#linkman").click(function(){
	var name = $("#inname").val()
	var tel = $("#intel").val()
	var msg = $("#inmsg").val()
	var userid = $(".card_right").attr("uid")
	console.log(name)
	console.log(tel)
	if(name == '' || tel ==  ''){
		alert("请输入姓名和电话！")
		return
	}
	$.post('http://www.realtoraccess.com/web/call/agent/',{userid:userid,name:name,tel:tel,msg:msg,mls:mls},function(data){
		if(data == 'ok'){
			alert("您的信息已提交给经纪人，谢谢！")
			$("#inname").val('')
			$("#intel").val('')
			$("#inmsg").val('')
		}else{
			alert("服务器繁忙，请稍后再试！")
		}
	})
})

//页面内跳转
$("#describe").click(function(){
	$("html,body").animate({scrollTop:$("#house_describe").offset().top}, 300)
	// $("#describe").css("background-color","#c9bc9c").css("color","#fff");
	// $(".nav_b_color").css("background-color","").css("color","black");
});
$("#tabulate").click(function(){
	$("html,body").animate({scrollTop:$(".house_tabulate_box").offset().top}, 300);
});
$("#broker").click(function(){
	$("html,body").animate({scrollTop:$("#headline_box").offset().top}, 300);
});
$("#lx").click(function(){
	$("html,body").animate({scrollTop:$("#house_broker").offset().top}, 300);
});
$("#recommend").click(function(){
	$("html,body").animate({scrollTop:$("#issuehouse").offset().top}, 300);
});
$("#house_round").click(function(){
	$("html,body").animate({scrollTop:$("#house_circum").offset().top}, 300);
});


// 、、新闻
$('.news1').show()
$(".categories:eq(0)").css("background-color","gray");
var kh
$(function(){
    var i=0 
    var max=3
    var kk=$(".categories").eq(0)

    function khj(){

      $('.'+kk.attr('dataid')).children('li').css("display","none")

      $('.'+kk.attr('dataid')).children().eq(i).css("display","block")
      
      i++
      if(i==max){
        i = 0
      }
    }
    clearInterval(kh)
    kh = setInterval(khj,2000); 
})

$(".categories").click(function(){

    var picurl = $(this).attr('pic')
    $("#headline_li").css('background-image', "url('/static/web/images/"+picurl+"')")
    $(".categories").css("background-color","");
    $(this).css("background-color","gray");
    $(".news ul").hide()
    $(this).attr('dataid')
    $('.'+$(this).attr('dataid')).show()
    var i=0 
    var max=$('.'+$(this).attr('dataid')).children('li').length

    var kk=$(this)

    function khj(){

      $('.'+kk.attr('dataid')).children('li').css("display","none")

      $('.'+kk.attr('dataid')).children().eq(i).css("display","block")
      
      i++
      if(i==max){
        i = 0
      }
    }
    clearInterval(kh)
    kh = setInterval(khj,2000); 

 });

$("#taugth").click(function(){
	$(".fdj").show()
})

$(".changee").click(function(){
	$(".fdj").hide()
})

$("#change").click(function(){
	var curragent = $(".card_right").attr('uid')
	$.getJSON('http://www.realtoraccess.com/web/other/agent/?mls='+mls+'&userid='+curragent, function(data){
		var div = '<div class="agenthead"><a href="/web/agent/?userid='+data.userid+'"><img src="'+data.head+'"></a></div>\
				            <div class="card_right" uid="'+data.userid+'">\
				        <p class="f_t">'+data.usercity+'&nbsp经纪</p>\
						<p class="f_t" id="f_tc">'+data.username+'</p>\
						<p class="f_corp">'+data.corp+'</p>\
					</div>'
		$(".card_box").empty()
		
		$(".card_box").append(div)
		$("#a_tell").text(data.tel)
		
		
		
	})
})

$(document).ready(function() {
	var address = $("body").attr('addr')
	var price = $("body").attr('price')
	//参数说明  地图中心点(与地址一致或自己设定)/价格/房源地址/地图放大倍数默认10
	$("#map").mapmarker(address, price, address,12);
});

