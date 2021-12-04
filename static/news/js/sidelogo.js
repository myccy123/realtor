    
$('#container_right').load('http://127.0.0.1:8000/static/web/header.html',function(data){
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
    
})


