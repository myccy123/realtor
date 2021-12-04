
$('#formLogin').validate({
    submitHandler: function(form) {
        $('#error-info').hide()
        login()
    },
    invalidHandler: function(event, validator) {}
})

$('#formRegister').validate({
    submitHandler: function(form) {
        $('#error-info').hide()
        register()
    },
    invalidHandler: function(event, validator) {}
})


$(document).ready(function() {


    $('[data-toggle="popover"]').popover()
    $('span.service').popover()
    $('span.service').on('shown.bs.popover', function() {
        $('#formMessage').validate({
            submitHandler: function(form) {
                leaveMessage()
            },
            invalidHandler: function(event, validator) {}
        })
    })
    $('.read-more').popover()
    $('.btn-option.wechat').hover(function() {
        $('#wechat-qrcode').css('display', 'block')
    }, function() {
        $('#wechat-qrcode').css('display', 'none')
    })
    $('.backTop').click(function() {
        $('html,body').animate({ scrollTop: 0 }, 'slow')
    })
    if ($('#selfIntro').length && $('#selfIntro')[0].scrollHeight > 255) {
        $('#selfIntro > .read-more').show()
    }
    if ($('#teamIntro').length && $('#teamIntro')[0].scrollHeight > 255) {
        $('#teamIntro > .read-more').show()
    }
    if ($('#corpIntro').length && $('#corpIntro')[0].scrollHeight > 255) {
        $('#corpIntro > .read-more').show()
    }
    $(document).click(function(event) {
        var clickover = $(event.target)
        var _opened = $('.navbar-collapse').hasClass('in')
        if (_opened === true) {
            $('button.navbar-toggle').click()
        }
    });
})
$(document).mouseup(function(e) {
    var container = $(".popover")
    if (!container.is(e.target) && container.has(e.target).length === 0) {
        container.popover("hide")
    }
})

$(document).on('click','#subscribe',function() {
    var userid = $('body').attr('userid')
    var email = $('#input-email').val()
    $.post('/web/add/email/',{userid: userid, useremail: email}, function(){
      alert("提交成功!")
    })
})


function login() {
    let userid = $('#userid').val()
    let passwd = $('#passwd').val()
    let data = { userid: userid, passwd: passwd }
    let $btn = $('#btn-login').button('loading')
    // business logic...

    $.ajax({
        type: 'POST',
        url: 'http://www.realtoraccess.com/web/signin/',
        data: data,
        dataType: 'JSON',
        success: function(resp) {
            let code = resp.rescode
            if (code != "0") {
                $btn.button('reset')
                $('#error-info').text(resp.resdesc)
                $('#error-info').show()
            } else {
                console.log('登录成功')
                window.location.href = '/web/console/'
            }
        }

    })
}

$(".custom-link").click(function(){
    hrf = $(this).attr('href')
    $.post('http://www.realtoraccess.com/web/update/visit/',{token:$(this).attr('tk')},function(){
        window.open(hrf)
    })
    return false
})

function GetQueryString(name)
{
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null)return  unescape(r[2]); return null;
}

function register() {
    let userid = $('#userid').val()
    let passwd = $('#passwd').val()
    let data = { userid: userid, passwd1: passwd, passwd2: passwd, from: GetQueryString('from') }
    let $btn = $('#btn-register').button('loading')
    $.ajax({
        type: 'POST',
        url: 'http://www.realtoraccess.com/web/signup/',
        data: data,
        dataType: 'JSON',
        success: function(resp) {
            let code = resp.rescode
            if (code != 0) {
                $btn.button('reset')
                $('#error-info').text(resp.resdesc)
                $('#error-info').show()
            } else {
                console.log('注册成功')
                window.location.href = '/web/console/'
            }
        }
    })
}

function leaveMessage() {
    let userid = $('#userid').val()
    let custname = $('#inputName').val()
    let custemail = $('#inputEmail').val()
    let custmsg = $('#inputMessage').val()
    let data = { userid: userid, custname: custname, custemail: custemail, custmsg: custmsg ,
                url: window.location.href}
    $.ajax({
        type: 'POST',
        url: 'http://www.realtoraccess.com/web/cmt/info/',
        data: data,
        dataType: 'JSON',
        success: function(resp) {
            let code = resp.rescode
            if (code != 0) {
                $('#error-info').text(resp.resdesc)
                $('#error-info').show()
            } else {
                alert('留言已成功发送')
            }
        }
    })
}