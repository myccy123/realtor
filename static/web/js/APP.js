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