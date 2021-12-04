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

//页码
var currpage = parseInt($(".pageclick").attr("currpage"))
var lastpage = parseInt($("#tip").attr('page'))
reset_pages()

$(".page").click(function(){
	currpage = parseInt($(this).text())
	jump()
	//reset_pages()
	//addagents(currpage,currule,currthisorder)
})

$("#nextpage").click(function(){
   if(currpage == lastpage){
       return
   }
   currpage++
   jump()
   //reset_pages()
   //addagents(currpage,currule,currthisorder)
})

$("#prevpage").click(function(){
	if(currpage == 1){
		return
	}
	currpage--
	jump()
	//reset_pages()
	//addagents(currpage,currule,currthisorder)
})

$("#confirm").click(function(){
	var to = parseInt($("#ipt").val())
	currpage = to
	jump()
	//reset_pages()
	//addagents(currpage,currule,currthisorder)
})

function jump(){
	urls = window.location.pathname.split('-')
	urls.pop()

	if(urls.length != 9){
		window.location.href = 'all-all-all-all-all-all-all-all-all-'+currpage
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

//条件筛选
// $(document).on('click','.condi a',function(){
// 	$(this).siblings().removeClass("seledcondi")
// 	$(this).addClass("seledcondi")
// })

// $(".areas a").click(function(){

// 	if($(this).text() != '不限'){
		
// 		$.get('http://www.realtoraccess.com/web/get/cities/?area='+$(this).attr('areaid'),function(data){
// 			cities = $.parseJSON(data)
// 			$(".city").children().remove()
// 			for(var i=0;i<cities.length;i++){
// 				$(".city").append('<a  cityid="'+cities[i].cityid+'">'+cities[i].cityname+'</a>')
// 			}
// 			$(".city").children().eq(0).before('<a class="seledcondi">不限</a>')
// 		})
// 	}else{
// 		$(".city").children().remove()
// 		$(".city").append('<a class="seledcondi">不限</a>')
// 		$(".county").children().remove()
// 		$(".county").append('<a class="seledcondi">不限</a>')
// 	}
// })
// $(document).on('click',".city a",function(){

// 	if($(this).text() != '不限'){
		
// 		$.get('http://www.realtoraccess.com/web/get/counties/?cityid='+$(this).attr('cityid'),function(data){
// 			cities = $.parseJSON(data)
// 			$(".county").children().remove()
// 			for(var i=0;i<cities.length;i++){
// 				$(".county").append('<a  countyid="'+cities[i].countyid+'">'+cities[i].countyname+'</a>')
// 			}
// 			$(".county").children().eq(0).before('<a class="seledcondi">不限</a>')
// 		})
// 	}else{
// 		$(".county").children().remove()
// 		$(".county").append('<a class="seledcondi">不限</a>')
// 	}
// })


//SEO改版删除 2018-03-26
// var canload = true

// function loadlisting(page,type){
// 	canload = false
// 	var gif = '<div id="ldgif"><img src="/static/web/images/loadlisting.gif"></div>'
// 	$(".studentlist").append(gif)
//     para = {page:page,type:type,city:$("#citytype").val(),school:$("#schooltype").val()}
// 	$.getJSON('http://www.realtoraccess.com/web/get/listings/',para, function(data){
// 		for(var i=0; i< data.length; i++){
			
// 			div1 = '<div class="share_box">\
//                 <div class="above">\
//             <div class="housepicture"><a href="/web/listing1/?mls='+data[i].mls+'"><img src="'+data[i].img+'"\
//              alt="瑞安居_海外房产_海外最新房源_海外二手房_mls"></a></div>\
//             <div class="information">\
//                <p class="price">&nbsp&nbsp'+data[i].price+' | '+data[i].areas+'</p>\
//                <p class="adddress">&nbsp&nbsp'+data[i].bedroom+'室'+data[i].toilet+'卫 &nbsp&nbsp<img class="dianwei"src="/static/web/images/_icon.png">&nbsp'+data[i].addr+'</p>\
//             </div>\
//         </div>\
//         <div class="page_view">\
//             <p><img src="/static/web/images/reading.png" alt="海外最新房源_阅读量">'+data[i].visit+'</p>\
//             <p class="date">'+data[i].date+'</p>\
//         </div></div>'
            
//             $(".studentlist").append(div1)
// 		}
// 		$("#ldgif").remove()
// 		canload = true
// 	})
// }

// var datatype = 'newhouse'
// var page = 1

// $(function(){
// 	$(".studentlist").empty()
// 	loadlisting(1,'newhouse')
//     $.getJSON('http://www.realtoraccess.com/app/get/cityinfo/', function(data){
//         for(i in data){
//             $("#citytype").append('<option value="'+data[i]['cityid']+'">'+data[i]['cityname']+'</option>')
//         }
//     })
// })

// $("#citytype").change(function(){
//     $(".studentlist").empty()
//     loadlisting(1,datatype)
//     $("#citytype").children().eq(0).removeAttr('selected')
// })

// $("#schooltype").change(function(){
//     $(".studentlist").empty()
//     loadlisting(1,datatype)
// })

// $(".up").click(function(){
	
// 	var title = $(this).attr('datatt')
// 	$("#part2title").text(title)
	
// 	datatype = $(this).attr('datatype')
	
// 	if(datatype == 'school'){
// 		$("#schooltype").show()
// 	}else{
// 		$("#schooltype").hide()
// 	}
//     $("#citytype").children().eq(0).attr('selected','')
// 	$(".studentlist").empty()
// 	loadlisting(1,datatype)
	
// })

// $(window).on('scroll',function(){
//   if(scrollTop() + windowHeight() >= (documentHeight() - 1000/*滚动响应区域高度取50px*/)){
// 	  page++;
// 	  if(canload){
// 		  loadlisting(page,datatype)
// 	  }
//   }
// });


// //获取页面顶部被卷起来的高度
// function scrollTop(){
//  return Math.max(
//   //chrome
//   document.body.scrollTop,
//   //firefox/IE
//   document.documentElement.scrollTop);
// }
// //获取页面文档的总高度
// function documentHeight(){
//  //现代浏览器（IE9+和其他浏览器）和IE8的document.body.scrollHeight和document.documentElement.scrollHeight都可以
//  return Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);
// }
// //获取页面浏览器视口的高度
// function windowHeight(){
//  //document.compatMode有两个取值。BackCompat：标准兼容模式关闭。CSS1Compat：标准兼容模式开启。
//  return (document.compatMode == "CSS1Compat")?
//  document.documentElement.clientHeight:
//  document.body.clientHeight;
// }












