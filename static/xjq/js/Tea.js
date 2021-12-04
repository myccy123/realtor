
//运货地址
 



//首页菜单
//乌龙茶

  $(".oolong").mouseover(function(){
    $(this).next().show();
    });  
$(".oolong").mouseleave(function(){
    $(this).next().hide();
    });  

$(".oolong").next().mouseleave(function(){
    $(this).hide();
  });

$(".oolong").next().mouseover(function(){
    $(this).show();
  });
  
  
  $(".news").mouseover(function(){
    $(this).next().show();
    });  
$(".news").mouseleave(function(){
    $(this).next().hide();
    });  

$(".news").next().mouseleave(function(){
    $(this).hide();
  });

$(".news").next().mouseover(function(){
    $(this).show();
  });
  
  



   
//边框
 $(".activity_1").mouseover(function(){
    $(this).css("border","3px solid peru"); 
  });

  $(".activity_1").mouseout(function(){
   $(this).css("border","3px solid white"); 
  });

 $(".product_one").mouseover(function(){
    $(this).css("border","3px solid peru"); 
  });

  $(".product_one").mouseout(function(){
   $(this).css("border","3px solid white"); 
  });



//客服
  $(".divQQbox").animate({right:-162},149);

   $("#kefu").mouseover(function(){
    $(".divQQbox").animate({right:0},149);
  });

  $(".divQQbox").mouseleave(function(){
    $(".divQQbox").animate({right:-162},149);
  });

//返回顶部
$(".top").click(function () {
        $('body,html').animate({ scrollTop: 0 }, 200)
 });



//导航栏背景
 $(function(){
  //当鼠标滑入时将classify_nav_1的class换成k
  $('.classify_nav_1').hover(function(){
    $(this).addClass('k');  
   },function(){
    //鼠标离开时移除k样式
    $(this).removeClass('k'); 
   }
  );
 });


//登录窗口
$("#tel").focus(function(){
  var value= $(this).val();//获取地址文本框的值
  if(value=="请输入手机号码"){
    $(this).val("");
  }

})






 

  $(".log_2").click(function(){
  $(".log_tel").show();
  $(".log_password").hide();
  })

 
  $(".log_1").click(function(){
  $(".log_tel").hide();
  $(".log_password").show();
  })



$(".login_submit").click(function(){
  $.get('http://www.yujiahao.cn/app/get/articles/',{'atype':"[share,advertorials]"},function(data){
      console.log(data)
  })
})


$(".sign_in_submit").click(function(){

  var data = {}
  data['fname'] = $(".log_name input").val()
  data['sname'] = $(".log_password input").val()
  data['city'] = $(".set_password input").val()
  data['userid'] = $(".confirm_password input").val()
  data['passwd1'] = $(".password1 input").val()
  data['passwd2'] = $(".password2 input").val()
  console.log(data)
  $.post("http://www.yujiahao.cn/app/signup1/",data,function(ll){

    var res = $.parseJSON(ll)
    if(res.rescode == 0){alert("恭喜你注册成功！");}
      else if(res.rescode == 1){alert("两次输入的密码不一致！")}
      else if(res.rescode == 2){alert("用户名已存在！")}
      
  });
  
})



$(document).ready(function(){
    $('.demo').hiSlider({
      intervalTime:3000,
      affectTime:700
    });

  $("#header").load('http://www.yujiahao.cn/static/xjq/header.html')
    $("#footer").load('http://www.yujiahao.cn/static/xjq/footer.html')
    

$("#header").find("div").click(function(){
    $("#address2").show();
    console.log("sadgdfh")
  });

});

