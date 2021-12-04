
// $('#header').load('http://www.realtoraccess.com/static/web/header.html',function(data){
// 		$("#header").html(data);
	//地理定位

 // $("#head_location").mouseover(function (){  
 //            $("#head_city").show();  
 //        }).mouseover(function (){  
 //            $("#head_city").show(); 
 //        }); 
 //     $("#head_city").mouseleave(function(){
 //        $(this).hide();
 //      });

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

	// })
$('#footer').load('http://www.realtoraccess.com/static/web/footerall.html')
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


//seo优化改版删除----2018-3-19
// function appenddom(flag){

//   if(currpage==maxpage && flag == true){
//     alert("已是最后一页!")
//     return

//   }

//   if(flag){
//   currpage++
//   }else{
//     if(currpage <= 1){
//       return
//     }else{
//       currpage--
//     }
//   }

//    $(".zhezao").show()
//   $.get("http://www.realtoraccess.com/web/listing/spread/",{"page":currpage,'type':'listing1'},function(data){

//     $(".zhezao").hide()
//     $(".share_box").remove()
//     var jsn = $.parseJSON(data)
//     for (var j = 0; j < jsn.length; j++) {
//       var head = jsn[j]['head']
//       var from = jsn[j]['from']
//       var username = jsn[j]['username']
//       var img = jsn[j]['img']
//       var price = jsn[j]['price']
//       var areas = jsn[j]['areas']
//       var cityname = jsn[j]['cityname']
//       var housetype = jsn[j]['housetype']
//       var visit = jsn[j]['visit']
//       var good = jsn[j]['good']
//       var corp = jsn[j]['corp']
//       var date = jsn[j]['date']
//       var lastpage = jsn[j]['lastpage']
//       var mls = jsn[j]['mls']
//       var htmlid = jsn[j]['htmlid']
//       var listingtype = jsn[j]['listingtype']
//       maxpage = lastpage
//       var href = listingtype == "listing1" ? '/web/'+listingtype+'/?mls='+mls+'&htmlid='+htmlid : jsn[j]['htmlid']

//       var div1 = j!=3?'<div class="share_box">':'<div class="share_box nomargin">'
//           div1 +=
//             '<div id="share_logo"><img src="'+head+'"></div>\
//             <div class="broker">\
//              <p> '+from+'</p>\
//               <p> <b>'+username+'</b></p>\
//               <p class="type">'+corp+'</p>\
//                     </div>\
//           <div class="above">\
//                 <div id="housepicture"><a href="'+href+'"><img src="'+img+'" alt="瑞安居_海外房产_海外最新房源_海外二手房_mls"></a></div>\
//                 <div class="information">\
//                    <p id="price">&nbsp&nbsp'+price+'&nbsp&nbsp|&nbsp&nbsp'+areas+'</p>\
//                    <p id="adddress">&nbsp&nbsp'+cityname+' &nbsp&nbsp '+housetype+'</p>\
//                 </div>\
//            </div>\
//            <div class="page_view">\
//               <p class="reading"><img src="/static/web/images/reading.png" alt="海外最新房源_阅读量">'+visit+'</p>\
//               <p class="date">'+date+'</p>\
//            </div>\
//          </div>';
//        // console.log(div1)
//       $("#box").append(div1);
   
  

//     };
//   }
//   )
// }

//在售房源翻页

var nowpage = 1
var rightable = Math.ceil($(".share_box").length/4)
if(rightable == 1){
  $("#houseright").hide()
}

$("#houseleft").click(function(){
  $("#box").animate({right:"-="+$(".windowbox").width()+"px"});
  nowpage--
  $("#houseright").show()
  if(nowpage == 1){
    $("#houseleft").hide()
  }
}
)

$("#houseright").click(function(){

  $("#box").animate({right:"+="+$(".windowbox").width()+"px"});
  $("#houseleft").show()
  nowpage++
  if(nowpage == rightable){
    $("#houseright").hide()
  }
}
)


//seo优化改版删除----2018-3-19
//独家发布租售房源
// var currpage2 = 0
// var maxpage2

// function appenddom2(flag){

//   if(currpage2==maxpage2 && flag == true){
//     alert("已是最后一页!")
//     return

//   }

//   if(flag){
//   currpage2++
//   }else{
//     if(currpage2 <= 1){

//     }else{
//       currpage2--
//     }
//   }

//    $(".zhezaotwo").show()

//   $.get("http://www.realtoraccess.com/web/listing/spread/",{"page":currpage2,'type':'listing2'},function(data){

//     $(".zhezaotwo").hide()

//     $(".share_boxtwo").remove()
//     var jsn = $.parseJSON(data)
//     for (var j = 0; j < jsn.length; j++) {
//       var head = jsn[j]['head']
//       var from = jsn[j]['from']
//       var username = jsn[j]['username']
//       var img = jsn[j]['img']
//       var price = jsn[j]['price']
//       var areas = jsn[j]['areas']
//       var cityname = jsn[j]['cityname']
//       var housetype = jsn[j]['housetype']
//       var visit = jsn[j]['visit']
//       var date = jsn[j]['date']

//       var lastpage = jsn[j]['lastpage']
//       var mls = jsn[j]['mls']
//       var listingname = jsn[j]['listingname']
//       var htmlid = jsn[j]['htmlid']
//       var listingtype = jsn[j]['listingtype']
//       var href = listingtype == "listing2" ? '/web/'+listingtype+'/?mls='+mls+'&htmlid='+htmlid : jsn[j]['htmlid']
//       maxpage2 = lastpage

//       var div2 = j!=3?'<div class="share_boxtwo">':'<div class="share_box nomargin">'
//           div2 +=
//            '<div id="share_logotwo"><img src="'+head+'"></div>\
//             <div class="brokertwo">\
//              <p> '+from+'</p>\
//               <p> <b>'+username+'</b></p>\
//               <p class="typetwo"><img src="/static/web/images/rentt.png"></p>\
//                     </div>\
//           <div class="abovetwo">\
//                 <div id="housepicturetwo"><a href="'+href+'"><img src="'+img+'" alt="瑞安居_海外房产_海外最新房源_海外二手房_mls"></a></div>\
//                 <div class="informationtwo">\
//                    <p id="pricetwo">&nbsp&nbsp'+price+'&nbsp&nbsp|&nbsp&nbsp'+housetype+'</p>\
//                    <p id="adddresstwo">&nbsp&nbsp'+listingname+'</p>\
//                 </div>\
//            </div>\
//            <div class="page_viewtwo">\
//               <p class="readingtwo"><img src="/static/web/images/reading.png" alt="海外最新房源_阅读量">'+visit+'</p>\
//               <p class="datetwo">'+date+'</p>\
//            </div>\
//          </div>';
    
//       $("#box_2two").append(div2);
   
  

//     };
//   }
//   )
// }

//租售房源翻页

var nowpage2 = 1
var rightable2 = Math.ceil($(".share_boxtwo").length/4)
if(rightable2 == 1){
  $("#rentright").hide()
}


$("#rentleft").click(function(){
  $("#box_2two").animate({right:"-="+$(".windowbox").width()+"px"});
  nowpage2--
  $("#rentright").show()
  if(nowpage2 == 1){
    $("#rentleft").hide()
  }
}
)

$("#rentright").click(function(){

  $("#box_2two").animate({right:"+="+$(".windowbox").width()+"px"});
  $("#rentleft").show()
  nowpage2++
  if(nowpage2 == rightable2){
    $("#rentright").hide()
  }
}
)


//用户图片替换成为压缩图片
// $("[src]").each(function(){
//   if($(this)[0].tagName == 'IMG'){
//     orgsrc = $(this).attr('src')
//     newsrc = $(this).attr('src').replace('/userimgs/','/agentimgs_small/').replace('/agentimgs/','/agentimgs_small/').replace('/sp_users/','/agentimgs_small/')
//     $(this).attr('src',newsrc)
//   }
// })


//seo优化改版删除----2018-3-19
// var currpageagent = 0
// var maxpageagent

// function appenddomagent(flag){

//   if(currpageagent==maxpageagent && flag == true){
//     alert("已是最后一页!")
//     return
//   }

//   if(flag){
//   currpageagent++
//   }else{
//     if(currpageagent <= 1){

//     }else{
//       currpageagent--
//     }
//   }

//    $(".zhezaoth").show()
   
//   $.get("http://www.realtoraccess.com/web/mysite/spread/",{page:currpageagent},function(data){

//    $(".zhezaoth").hide()
//      $(".agent_informationth").remove()
//     var jsn = $.parseJSON(data)
//       for (var j = 0; j < jsn.length; j++) {
//       var username = jsn[j]['username']
//       var userid = jsn[j]['userid']
//       var img = jsn[j]['img']
//       var usercity = jsn[j]['usercity']
//       var corp = jsn[j]['corp']
//       var wechat = jsn[j]['wechat']
//       var note = jsn[j]['note']
//       var auth = jsn[j]['auth']
//       var lastpage = jsn[j]['lastpage']
//       var vipicon = auth==1?'<div class="bigvip"><img src="/static/web/images/bigvip.png"></div>':'<div class="bigvip"></div>'
//       var viptxt = auth==1?'<p>认证经纪</p>':'<p>&nbsp;</p>'
//       maxpageagent = lastpage
 

//       var divagent = j!=3?'<div class="agent_informationth">':'<div class="agent_informationth nomargin">'
//           divagent +=
//              '<div class="agent_informationth" id="agentfirstth">\
//                        <div class="agent_headth" align="center"><a href="/web/agent/?userid='+userid+'"><img src="'+img+'" alt="海外房产经纪头像"></a></div>'+vipicon+'\
//                        <div class="agentrenz">'+viptxt+'\
//                       </div>\
//                        <div class="agentnameth">\
//                             <p>'+usercity+' &nbsp 经纪</p>\
//                             <h1>'+username+'</h1>\
//                             <p>'+corp+'</p>\
//                        </div>\
//                        <div class="agent_adth">\
//                          <p>'+note+'</p>\
//                          <div class="weixsoanth"> <img src="'+wechat+'"></div>\
//                        </div>\
//                     </div>';
//      $(".counselor_boxth").append(divagent);
//     };

//   }
//   )
// }


//经纪推荐
var nowpage3 = 1
var rightable3 = Math.ceil($(".agent_informationth").length/4)
$("#houseleftth").hide()
if(rightable3 == 1){
  $("#houserightth").hide()
}


$("#houseleftth").click(function(){
  console.log($(".agent_informationth").eq(0).width())
  $(".counselor_boxth").animate({right:"-="+$(".agent_informationth").width()*4+"px"});
  nowpage3--
  $("#houserightth").show()
  if(nowpage3 == 1){
    $("#houseleftth").hide()
  }
}
)

$("#houserightth").click(function(){

  $(".counselor_boxth").animate({right:"+="+$(".agent_informationth").width()*4+"px"});
  $("#houseleftth").show()
  nowpage3++
  if(nowpage3 == rightable3){
    $("#houserightth").hide()
  }
}
)


//首页房源搜索
$("#search_clas_two").click(function(){
  $("#searchsj").animate({left:'435px'});

});

$("#search_clas_first").click(function(){
  $("#searchsj").animate({left:'305px'});
   $("#input_house").attr({placeholder:"  请输入MLS，查找房源"});

    
});



$("#search_clas_two").click(function(){
	
  $("#input_house").attr({placeholder:"  请输入楼盘名称，查找房源"});

});

var stype = 'listing1'
$("#search_clas_first").click(function(){
  stype = 'listing1'
});
$("#search_clas_two").click(function(){
  stype = 'listing2'
});

$("#magnifying_glass").click(function(){
  var q = $("#input_house").val()

  $("#searchlink").attr("href","/web/search/?q="+q+"&qtype="+stype)
  return true
});


 
//热门公众号
     $("#hover1").mouseover(function(){
    $("#hover1_up").show();
  });
        $("#hover1_up").mouseleave(function(){
    $("#hover1_up").hide();
  });
          $("#hover2").mouseover(function(){
    $("#hover2_up").show();
  });
        $("#hover2_up").mouseleave(function(){
    $("#hover2_up").hide();
  });
             $("#hover3").mouseover(function(){
    $("#hover3_up").show();
  });
        $("#hover3_up").mouseleave(function(){
    $("#hover3_up").hide();
  });
             $("#hover4").mouseover(function(){
    $("#hover4_up").show();
  });
        $("#hover4_up").mouseleave(function(){
    $("#hover4_up").hide();
  });
   

var newsnum = 0
var tik = setInterval(poll,3000);

function poll(){
	
	$(".news li").css("display","none")
	
	var currli = $(".news li").eq(newsnum)
	currli.css("display","block")
	$(".news ul").hide()
	currli.parent().show()
	
	var newsobj = $("[dataid='"+currli.parent().attr('class')+"']")
	var picurl = newsobj.attr('pic')
    $("#headline_li").css('background-image', "url('/static/web/images/"+picurl+"')")
    $(".categories").css("background-color","");
    newsobj.css("background-color","gray");
	
	newsnum++
	if(newsnum == 13){
		newsnum = 0
	}
}

$(".categories").click(function(){
	var newsobj = $(this)
	var picurl = newsobj.attr('pic')
    $("#headline_li").css('background-image', "url('/static/web/images/"+picurl+"')")
    $(".categories").css("background-color","");
    newsobj.css("background-color","gray");
	
    newsnum = parseInt($(this).attr('subnum'))
    
    $(".news li").css("display","none")
	var currli = $(".news li").eq(newsnum)
	currli.css("display","block")
	$(".news ul").hide()
	currli.parent().show()
	
    newsnum++
    clearInterval(tik)
    tik = setInterval(poll,3000);
})

$(".news li").mouseover(function(){
	clearInterval(tik)
})

$(".news li").mouseout(function(){
	tik = setInterval(poll,3000);
})
 
           $('.sz').eq(0).animationCounter({
  start: $('.sz').eq(0).text()-1000,
  end: $('.sz').eq(0).text(),
  step: 1,
  delay: 1
});  
$('.sz').eq(1).animationCounter({
  start: 0,
  end: $('.sz').eq(1).text(),
  step: 1,
  delay: 20
});  
$('.sz').eq(2).animationCounter({
  start: 0,
  end: $('.sz').eq(2).text(),
  step: 1,
  delay: 1
});  
$('.sz').eq(3).animationCounter({
  start: 0,
  end: $('.sz').eq(3).text(),
  step: 1,
  delay: 20
});  
$('.sz').eq(4).animationCounter({
  start: 0,
  end: $('.sz').eq(4).text(),
  step: 1,
  delay: 3
});  


$("#free").click(function(){
	window.open("http://webmainland.mikecrm.com/T7krWtW")
})

// $("#magnifying_glass").height(45)
// alert($("#magnifying_glass").height())
// alert($('.search').height())
//alert(document.body.clientWidth)
if(1){
    $("#magnifying_glass").height($('.search').height())
}
