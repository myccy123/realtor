$('#header').load('http://www.realtoraccess.com/static/web/header.html',function(data){
		$("#header").html(data);
		 //地理定位
		//   $("#head_location").mouseover(function(){
		//     $(this).next().show();
		//     });  
		// $("#head_location").mouseleave(function(){
		//     $(this).next().hide();
		//     });  

		// $("#head_location").next().mouseleave(function(){
		//     $(this).hide();
		//   });

		// $("#head_location").next().mouseover(function(){
		//     $(this).show();
		//   });

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


		 $("#head_land_img").click(function(){
		   $("#head_land").hide();

		 })
		  $("#head_nav_land").click(function(){
		    $("#head_land").show();
		    return false;
		    
		 })
		 $("#head_login_img").click(function(){
		   $("#head_login").hide();

		 })
		  $("#head_nav_login").click(function(){
		   $("#head_login").show();
		   return false;
		 })

      $("#head_tologin").click(function(){
       $("#head_login").hide();
       $("#head_land").show();
       return false;
     })

      $("#head_tosignup").click(function(){
       $("#head_land").hide();
       $("#head_login").show();
       return false;
     })

	})
$('#footer').load('http://www.realtoraccess.com/static/news/footer.html')
$('#container_box_right').load('http://www.realtoraccess.com/static/news/sidelogo.html',function(data){
        $("#container_box_right").html(data)
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

function GetQueryString(name)
{
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null)return  unescape(r[2]); return null;
}

var c = GetQueryString("cate")
if(c == null){
	c = 'global'
}

$(function(){

	var initpage = GetQueryString("page")
	var maxpage = $("#nextpage").attr("maxpage")
	
	$("."+c).addClass("seled")

	if(initpage== '1' || initpage == null){
		$("#prepage").css("color","#999")
		$("#prepage").removeAttr("href")
	}else{
		var p = parseInt(initpage)-1
		$("#prepage").attr("href","/news/list/?cate="+c+"&page="+p)
	}

	if(maxpage == '1' || parseInt(initpage) == parseInt(maxpage)){
		$("#nextpage").css("color","#999")
		$("#nextpage").removeAttr("href")
	}else{
		var p = parseInt(initpage)+1
		$("#nextpage").attr("href","/news/list/?cate="+c+"&page="+p)
	}
	var para = typeof($("body").attr('id')) != 'undefined'?$("body").attr('id'):''
	$(".ad").append('<a href="/"><img src="/static/news/img/ad3.gif"></a>')
	// $.getJSON('http://www.realtoraccess.com/news/share/cnt?articleid='+para, function(data){
	// 	for(var i=0;i<data.length;i++){
	// 		$(".ad").append('<a href="/web/agent/?userid='+data[i]['userid']+'"><img src="'+data[i]['img']+'"></a>')
	// 		if(i==7){
	// 			break;
	// 		}
	// 	}
	// })
})

$("#prepage").click(function(){
	var p = GetQueryString("page")
	if(p == null || p == '1'){
		return false
	} else{
		p = parseInt(p)-1
	}
	
	$(this).attr("href","/news/list/?cate="+c+"&page="+p)
	return true
})


$("#nextpage").click(function(){
	var p = GetQueryString("page")
	var lastpage = $(this).attr("maxpage")
	if(p == null){
		if(lastpage != "1"){
			p = "2"
		}else{
			return false
		}
	}else if(p == lastpage){
		return false
	}else{
		p = parseInt(p)+1
	}
	$(this).attr("href","/news/list/?cate="+c+"&page="+p)
	return true
})





