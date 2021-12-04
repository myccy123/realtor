

var mls = $("body").attr("mls")
var token = $("body").attr("token")

var name
var cardid
var yyyy
var mm
var cvs

var editable = false


$(document).on('click','#edit',function(){

	if(editable){
		newname = $("#cardname").val()
		newcardid = $("#cardno").val()
		newyyyy = $("#cardy").val()
		newmm = $("#cardm").val()
		newcvs = $("#cardcvs").val()

		if(newname==name && newcardid==cardid && newyyyy==yyyy && newmm==mm && newcvs==cvs){
			$('#edit').text("Edit")
			$("input").attr("readonly","readonly")
			$("#cancle").hide()
			editable = false
			return
		}else{
			$('#edit').text("Posting")
			$('#edit').css({'background':'#ff0036','border':'1px solid #ff0036'})
			$("#cancle").hide()
			$.post('http://127.0.0.1:8000/sp/postcard/',{mls:mls,token:token,name:newname,cardid:newcardid,yyyy:newyyyy,mm:newmm,cvs:newcvs},function(data){
				if(data == 'ok'){
					$('#edit').text("Edit")
					$('#edit').css({'background':'#4080ff','border':'1px solid #4b7bdb'})
					$("input").attr("readonly","readonly")
					editable = false
				}else{
					$(this).text("Post")
					$("#cancle").show()
					editable = true
				}
			})
		}
	}else{

		$(this).text("Post")
		$("input").removeAttr("readonly")
		$("#cancle").show()

		name = $("#cardname").val()
		cardid = $("#cardno").val()
		yyyy = $("#cardy").val()
		mm = $("#cardm").val()
		cvs = $("#cardcvs").val()
		editable = true
	}

})

$(document).on('click','#cancle',function(){

	$('#edit').text("Edit")
	$("input").attr("readonly","readonly")
	$("#cancle").hide()
	$("#cardname").val(name)
	$("#cardno").val(cardid)
	$("#cardy").val(yyyy)
	$("#cardm").val(mm)
	$("#cardcvs").val(cvs)
	editable = false

})










