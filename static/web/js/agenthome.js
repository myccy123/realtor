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

     //  $("#head_tologin").click(function(){
     //   $("#head_login").hide();
     //   $("#head_land").show();
     //   return false;
     // })

     //  $("#head_tosignup").click(function(){
     //   $("#head_land").hide();
     //   $("#head_login").show();
     //   return false;
     // })

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

//页面内跳转
$("#agentintroduce").click(function(){
	$(this).css("background","#ea7865").siblings().css("background","#EEDC82"); 
});
$("#compony").click(function(){
	$("html,body").animate({scrollTop:$("#introduce2").offset().top}, 300);
	$(this).css("background","#ea7865").siblings().css("background","#EEDC82"); 
});
$("#teammm").click(function(){
	$("html,body").animate({scrollTop:$(".clasily").offset().top}, 300);
	$(this).css("background","#ea7865").siblings().css("background","#EEDC82"); 
});
$("#successss").click(function(){
	$("html,body").animate({scrollTop:$("#agentsuccess").offset().top}, 300);
	$(this).css("background","#ea7865").siblings().css("background","#EEDC82"); 
});



var polllen = $("#ul_box").children().length
var cnt = polllen/2
var cnt2 = 0


$("#arrows_up").click(function(){
	if(cnt > 1){
		$("#ul_box").animate({top:'-=500px'},500)
		cnt--
		cnt2++
	}
})

$("#arrows_down").click(function(){
	if(cnt2 > 0){
		$("#ul_box").animate({top:'+=500px'},500)
		cnt++
		cnt2--
	}
})

$(function(){

	if($(".part1_right").attr("identity") == '0'){
		$("#iden").empty()
	}


	var star = parseInt($("#datastar").attr("stars"))
	for (var i = 0; i < 5; i++) {
		if(i<star){
			$("#datastar").append('<img src="/static/web/images/xx.png">')
		}else{
			$("#datastar").append('<img src="/static/web/images/whitestar.png">')  //todo
		}
	}
})

var newspage
var newscurr = 1

// 新闻
$(function(){
	$.get("http://www.realtoraccess.com/web/news/history/",{"userid":$("body").attr("username")},function(data){
		var jsn = $.parseJSON(data)
		newspage = jsn.page
    if(jsn.articles.length == 0){
      $("#headline_box").hide()
      return
    }
		for (var j = 0; j < jsn.articles.length; j++) {
		    
		      var id = jsn.articles[j]['id']
		      var date = jsn.articles[j]['date']
		      var title = jsn.articles[j]['title']
		      var img = jsn.articles[j]['img']
		      var visit = jsn.articles[j]['visit']

		      var div2 = '<div class="share_boxtwo">\
				          <div class="abovetwo">\
		              <div id="housepicturetwo"><a href="/news/'+id+'"><img src="'+img+'"></a></div>\
		              <div class="informationtwo">\
		                 <p id="newstitle">'+title+'</p>\
		              </div></div>\
			         <div class="page_viewtwo">\
			            <p class="readingtwo"><img src="/static/web/images/reading.png">'+visit+'</p>\
			            <p class="datetwo">'+date+'</p>\
			         </div></div>'
		    
		      $(".news_wrapper").append(div2);
		    };
	})
})

$("#newslefttwo").click(function(){
	if(newscurr == 1){
		return
	}else{
		newscurr--
		$(".news_wrapper").animate({left: '+=1144px'},'fast')
	}
})

$("#newsrighttwo").click(function(){
	if(newscurr == newspage){
		return
	}else{
		console.log(newspage)
		newscurr++
		$(".news_wrapper").animate({left: '-=1144px'},'fast')
	}
})




//经纪房源发布记录
var currpage2 = 0
var maxpage2

function appenddom2(flag){

  if(currpage2==maxpage2 && flag == true){
    alert("已是最后一页!")
    return

  }

  if(flag){
  currpage2++
  }else{
    if(currpage2 <= 1){
    	return
    }else{
      currpage2--
    }
  }

   $(".zhezaotwo").show()

  $.get("http://www.realtoraccess.com/web/share/history/",{"userid":$("body").attr("username"),"page":currpage2},function(data){



    $(".zhezaotwo").hide()
    $(".share_houses").remove()
    var jsn = $.parseJSON(data)
    if(jsn.length == 0){
      $("#issuehouse").hide()
      $("#box_2two").hide()
    }
    for (var j = 0; j < jsn.length; j++) {
    
      var img = jsn[j]['img']
      var price = jsn[j]['price']
      var areas = jsn[j]['areas']
      var cityname = jsn[j]['cityname']
      var housetype = jsn[j]['housetype']
      var visit = jsn[j]['visit']
      var date = jsn[j]['date']
      var lastpage = jsn[j]['lastpage']
      var mls = jsn[j]['mls']
      var href = jsn[j]['href']
      maxpage2 = lastpage

      var div2 = j!=3?'<div class="share_boxtwo share_houses">':'<div class="share_boxtwo share_houses nomargin">'
          div2 +=
           '<div class="abovetwo">\
                <div id="housepicturetwo"><a href="'+href+'"><img src="'+img+'" \
                alt="瑞安居_海外房产经纪分享房源"></a></div>\
                <div class="informationtwo">\
                   <p id="pricetwo">&nbsp&nbsp'+price+'&nbsp&nbsp|&nbsp&nbsp'+areas+'</p>\
                   <p id="adddresstwo">&nbsp&nbsp'+cityname+' '+housetype+'</p>\
                </div>\
           </div>\
           <div class="page_viewtwo">\
              <p class="readingtwo"><img src="/static/web/images/reading.png">'+visit+'</p>\
              <p class="datetwo">'+date+'</p>\
           </div>\
         </div>';
    
      $("#box_2two").append(div2);
   
  

    };
  }
  )
}

appenddom2(true)

$("#houselefttwo").click(function(){
  appenddom2(false)
}
)

$("#houserighttwo").click(function(){

  appenddom2(true)

 if(currpage2==maxpage2){
   $("#iconrighttwo").hide();
 }
}
)

function GetQueryString(name)
{
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null)return  unescape(r[2]); return null;
}



//评论
$("#button").click(function(){
  var comment = $("#input_evaluate").val()
  console.log(comment)
 

  $.post('http://www.realtoraccess.com/web/comment/',{"comment":comment,"userid":GetQueryString('userid')},function(data){
    if(data == 'ok'){
      //alert("评论成功")
   }else{
      alert("服务器繁忙，请稍后再试！")
    }
  })
  
  $(".conment_box").children().eq(0).before('<p>'+comment+'</p>');

})

//点击查看更多评论

var lookmorepage = 1
$(".lookmore").click(function(){
  $.get('http://www.realtoraccess.com/web/get/comment/',{"page":lookmorepage,"userid":GetQueryString('userid')},function(data){
    var comms = $.parseJSON(data)
    for(var i=0;i<comms.length;i++){
      $(".conment_box").append('<p>'+comms[i].comment+'</p>');
    }
    lookmorepage++
  })
})

//图片轮播
$(document).ready(function(){
  $('.flexslider').flexslider({
    directionNav: true,
    pauseOnAction: false
  });
});   


