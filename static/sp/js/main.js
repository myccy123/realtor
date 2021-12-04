  var floor;
  var initnum = 0;

  document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {        
    // 通过下面这个API显示右上角按钮         
    WeixinJSBridge.call('showOptionMenu');  });
  //share to wechat
  



  var timestamp = new Date().getTime();
  timestamp = timestamp.toString().substring(0, 10);
  var url = window.location.href;
  url = encodeURIComponent(url.split('#')[0]);

  var signature;
  var imgurl;
  var notes;
  var tt;
  var openhouse1 = ''
  tt = $("body").attr("wechattitle")
  notes = $("body").attr("wechatnote")
  imgurl = $("#gethead").attr('src');
  presell = $("body").attr("presell")


  $.get('http://www.realtoraccess.com/weixin/jsapi/?timestamp=' + timestamp + '&url=' + url, function(data) {
    signature = data;
    wx.config({
      debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
      appId: 'wxcd1c7e6e724cc101', // 必填，公众号的唯一标识
      timestamp: timestamp, // 必填，生成签名的时间戳
      nonceStr: 'realter', // 必填，生成签名的随机串
      signature: signature, // 必填，签名，见附录1
      jsApiList: ['onMenuShareAppMessage', 'onMenuShareTimeline'] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
    });

    wx.ready(function() {
      wx.onMenuShareAppMessage({
        title: tt, // 分享标题
        desc: openhouse1==''?notes: presell == '1' ? openhouse1+' | '+notes : '公众开放日 | '+openhouse1+' | '+notes, // 分享描述
        link: '', // 分享链接
        imgUrl: imgurl, // 分享图标
        type: '', // 分享类型,music、video或link，不填默认为link
        dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
        success: function() {
          // 用户确认分享后执行的回调函数
        },
        cancel: function() {
          // 用户取消分享后执行的回调函数
        }
      });
      wx.onMenuShareTimeline({
        title: tt, // 分享标题
        link: '', // 分享链接
        imgUrl: imgurl, // 分享图标
        success: function() {
          // 用户确认分享后执行的回调函数
        },
        cancel: function() {
          // 用户取消分享后执行的回调函数
        }
      });
    });
  })

  //initial the type picture's pagination
  //$('.type-pagination').find('#1').addClass('showing-page');
  var mls = $('body').attr('mls');
  /*
  测试用。
  var opendays = [{
      opentime: "01:00-19:00",
      opendate: "2016， 12月17日， 星期1"
    },
    {
      opentime: "11:00-18:00",
      opendate: "2017， 2月1日， 星期一"
    }, {
      opentime: "5:00-9:00",
      opendate: "2017， 8月17日， 星期六"
    }
  ]
  for (var i in opendays) {
    $('.add-on-' + i).text(opendays[i].opendate);
    $('.add-time-' + i).text(opendays[i].opentime);
  }
  */

  //公众开放日ajax
  //  $.ajax({
  //    type: 'GET',
  //    url: 'http://www.realtoraccess.com/sp/get/openhouse/?mls='+mls,
  //    dataType: 'json/application',
  //    success: function(res) {
  //      console.log(res.data)
  //      var opendays = res.data;
  //      for (var i in opendays) {
  //        $('.add-on-' + i).text(opendays[i].opendate);
  //        $('.add-time-' + i).text(opendays[i].opentime);
  //      }
  //    },
  //    error: function(err) {
  //      console.log(err)
  //      console.error('get info failed')
  //    }
  //  });

  $.get('http://www.realtoraccess.com/sp/get/openhouse/?mls=' + mls, function(res) {
    var opendays = $.parseJSON(res);
    if (opendays.length > 0) {
      $('.openday-li-3').css('display', 'block');
      $(".year").text('');
      switch (opendays.length) {
        case 1:
          $('.openday-li-2').css('display', 'none');
          $('.openday-li-3').css('display', 'none');
          $('#opendays').find('.data-wrap').css('top', '36%');
          break;
        case 2:
          $('.openday-li-3').css('display', 'none');
          $('#opendays').find('.data-wrap').css('top', '25%');
          break;
        case 3:
          $('#opendays').find('.data-wrap').css('top', '14%');
          break;
        default:

      }
      openhouse1 = opendays[0].opendate
    }
    for (var i in opendays) {
      j = parseInt(i) + 1;
      $('.add-on-' + j).text(opendays[i].opendate);
      $('.add-time-' + j).text(opendays[i].opentime);
    }
  })

  $.get('http://www.realtoraccess.com/sp/get/imgs/?mls=' + mls, function(res) {
    var assetpic = $.parseJSON(res);
    $("#listingimgs").empty();
    for (var i in assetpic) {
      div = '<div class="col-md-4 col-xs-6 col-lg-4 col-sm-6 target">\
			     <img id="house-pic-' + i + '" src="' + assetpic[i].img + '" data-info="' + assetpic[i].desc + '" data-toggle="modal" data-target="#myModal" onclick="showPicInfo(this);" />\
				</div>';
      $("#listingimgs").append(div);
    }
  })
  //户型图片的ajax
  //  $.ajax({
  //    type: 'GET',
  //    url: 'http://www.realtoraccess.com/sp/get/floorplan/',
  //    dataType: 'json/application',
  //    data: {
  //      mls: ''
  //    },
  //    success: function(res) {
  //      var floor = res.data;
  //      var j = 0;
  //      for (var i = 1 in floor) {
  //        j = parseInt(i) + 1;
  //        $('.type-' + j).find('img').attr('src', floor[i]);
  //     }
  //   },
  //   error: function(err) {
  //     console.error('get info failed')
  //   }
  // })



  $("#pcBtn").click(function() {
    agentid = $("#agentid").text();
    name = $("#name1").val();
    email = $("#email1").val();
    tel = $("#tel1").val();
    comm = $("#comm1").val();
    $.post('http://www.realtoraccess.com/sp/call/agent/', {
      mls: mls,
      agentid: agentid,
      name: name,
      tel: tel,
      email: email,
      desc: comm
    }, function(data, textStatus) {
      if (textStatus == 'success')
        alert('您的信息提交成功');
      else
        alert('信息提交失败');
      return false;
    })
  })

  $("#mobileBtn").click(function() {
    agentid = $("#agentid").text();
    name = $("#mobileName").val();
    email = $("#mobileEmail").val();
    tel = $("#mobilePhone").val();
    comm = $("#comm2").val();
    $.post('http://www.realtoraccess.com/sp/call/agent/', {
      mls: mls,
      agentid: agentid,
      name: name,
      tel: tel,
      email: email,
      desc: comm
    }, function(data, textStatus) {
      console.log(textStatus);
      if (textStatus == 'success')
        alert('您的信息提交成功');
      else
        alert('信息提交失败');
      return false;
    })
  })


  $.get('http://www.realtoraccess.com/sp/get/floorplan/?mls=' + mls, function(res) {
    floor = $.parseJSON(res);
    var j = 0;
    if (floor.length > 0) {
      $('.page-left').text('〈');
      $('.page-right').text('〉');
      $('.house-type-pic-container').attr('data-info', floor.length - 1);
      for (var i in floor) {
        $('#pagination-ul').append('<li class="page-mid" id="pagi-' + i + '" onclick="changePage(' + i + ')" data-info="' + floor[i] + '">·</li>');
      }
      $('.type-pic').find('img').attr({'src': floor[initnum]});
      $('.type-pic').attr({'align' : 'center'})
      $('.type-words').find('.type-num').text('01');
      $('#pagi-0').addClass('showing-page');
      
      console.log($('.type-pic').find('img').width());
      console.log($('.type-pic').find('img').height());
      // if($('.type-pic').find('img').width > $('.type-pic').find('img').height){
      //   $('.type-pic').find('img').css('width','100%')
      // }else{
      //   $('.type-pic').find('img').css('height','100%')
      // }

    }


  })


  //   //debug
  //   floor = ["http://www.realtoraccess.com/data/listings/r2177295_1.jpg"]
  //   if (floor.length > 0) {
  //     console.log('test floor');
  //     $('.page-left').text('<');
  //     $('.page-right').text('>');
  //     $('.house-type-pic-container').attr('data-info', floor.length - 1);
  //     for (var i in floor) {
  //       $('#pagination-ul').append('<li class="page-mid" id="pagi-' + i + '" onclick="changePage(' + i + ')" data-info="' + floor[i] + '">—</li>');
  //     }
  //     $('.type-pic').find('img').attr('src', floor[initnum]);
  //     $('.type-words').find('.type-num').text('01');
  //     $('#pagi-0').addClass('showing-page');
  //   }

  // })

  function changePage(pagenum) {
    var timer = 0;
    var typenum;
    //console.log($('.house-type-pic-container').attr('data-info'));
    //var initLeft = $('.showing').offset().left;
    if (pagenum != initnum) {
      var interval = setInterval(function() {
        if (pagenum > initnum || pagenum == 'r')
          $('.house-type-pic-container').css('left', $('.house-type-pic-container').offset().left + 100 + 'px');
        if (pagenum < initnum || pagenum == 'l')
          $('.house-type-pic-container').css('left', $('.house-type-pic-container').position().left - 100 + 'px');
        $('.house-type-pic-container').css('opacity', $('.house-type-pic-container').css('opacity') / 1.5);
        timer++;
        if (timer > 6) {
          clearInterval(interval);
          reloadPagination(pagenum);
        }

      }, 30);

    }
  }

  function reloadPagination(num) {
    if (num == 'r') {
      if (initnum != $('.house-type-pic-container').attr('data-info'))
        initnum++;
    } else {
      if (num == 'l') {
        if (initnum != 0)
          initnum--;
      } else
        initnum = num;
    }
    $('.showing-page').removeClass('showing-page');
    $('#pagi-' + initnum).addClass('showing-page');
    typenum = initnum + 1;
    $('.type-pic').find('img').attr('src', $('#pagi-' + initnum).attr('data-info'));
    $('.type-words').find('.type-num').text('0' + typenum);
    $('.house-type-pic-container').css('left', 0);
    $('.house-type-pic-container').css('opacity', 1);
  }

  // show Pic information
  var presentPic;

  function showPicInfo(target) {
    presentPic = $(target).attr('id');
    var imgsrc = $(target).attr('src');
    var imgdesc = $(target).attr('data-info');
    $('#modal-img').attr('src', imgsrc);
    $('#modal-desc').text(imgdesc);
  }

  function toLeftPic() {
    var presrc = $('#' + presentPic).parent('.target').prev().find('img').attr('src');
    var predesc = $('#' + presentPic).parent('.target').prev().find('img').attr('data-info');
    $('#modal-img').attr('src', presrc);
    $('#modal-desc').text(predesc);
    presentPic = $('#' + presentPic).parent('.target').prev().find('img').attr('id');

  }

  function toRightPic() {
    var presrc = $('#' + presentPic).parent('.target').next().find('img').attr('src');
    var predesc = $('#' + presentPic).parent('.target').next().find('img').attr('data-info');
    $('#modal-img').attr('src', presrc);
    $('#modal-desc').text(predesc);
    presentPic = $('#' + presentPic).parent('.target').next().find('img').attr('id');

  }

  $(document).on("mousewheel DOMMouseScroll", function(e) {
    if (document.body.scrollTop > 100) {
      $('.nav-top-black').css('display', 'none');
    } else {
      $('.nav-top-black').css('display', 'block');

    }
  });
  $("#todescrption").click(function() {
    if (document.body.clientWidth > 768) {
      $("html,body").animate({
        scrollTop: $("#descrption").offset().top - 120
      }, 300);
    } else {
      console.log('test');
      $("html,body").animate({
        scrollTop: $("#descrption").offset().top - 85
      }, 300);
    }
  });

  $("#todetail").click(function() {
    if (document.body.clientWidth > 768) {
      $("html,body").animate({
        scrollTop: $("#detail").offset().top - 120
      }, 300);
    } else {
      $("html,body").animate({
        scrollTop: $("#detail").offset().top - 50
      }, 300);
    }

  });
  $("#toopendays").click(function() {
    if (document.body.clientWidth > 768) {

      $("html,body").animate({
        scrollTop: $("#opendays").offset().top - 60
      }, 300);
    } else {
      $("html,body").animate({
        scrollTop: $("#opendays").offset().top - 40
      }, 300);

    }
  });

  $("#topicture").click(function() {
    if (document.body.clientWidth > 768) {

      $("html,body").animate({
        scrollTop: $("#picture").offset().top - 100
      }, 300);
    } else {
      $("html,body").animate({
        scrollTop: $("#picture").offset().top - 40
      }, 300);

    }
  });

  $("#totype").click(function() {
    if (document.body.clientWidth > 768) {

      $("html,body").animate({
        scrollTop: $("#type").offset().top - 80
      }, 300);

    } else {
      $("html,body").animate({
        scrollTop: $("#type").offset().top - 40
      }, 300);

    }
  });
  $("#tovideos").click(function() {
    if (document.body.clientWidth > 768) {

      $("html,body").animate({
        scrollTop: $("#videos").offset().top - 100
      }, 300);
    } else {
      $("html,body").animate({
        scrollTop: $("#videos").offset().top - 40
      }, 300);

    }
  });

  $("body").on('click', '#toreal', function() {
    if (document.body.clientWidth > 768) {

      $("html,body").animate({
        scrollTop: $("#real").offset().top - 100
      }, 300);
    } else {
      $("html,body").animate({
        scrollTop: $("#real").offset().top - 40
      }, 300);

    }
  });

  $("#tolocation").click(function() {
    if (document.body.clientWidth > 768) {

      $("html,body").animate({
        scrollTop: $("#location").offset().top - 100
      }, 300);
    } else {
      $("html,body").animate({
        scrollTop: $("#location").offset().top - 40
      }, 300);

    }
  });

  $("#tocontact").click(function() {
    if (document.body.clientWidth > 768) {
      $("html,body").animate({
        scrollTop: $("#contact").offset().top - 100
      }, 300);
    } else {
      $("html,body").animate({
        scrollTop: $(".xs-contact").offset().top - 40
      }, 300);
    }
  });
  $("#index").click(function() {
    $("html,body").animate({
      scrollTop: 0
    }, 200);
  });
  $('.menu-container').find('.navbar-color').on('click', function() {
    $('.navbar-ex1-collapse ').removeClass('in');
  });
  $('.return-top').on('click', function() {
    console.log('hhh')
    $("html,body").animate({
      scrollTop: 0
    }, 200);
  });

  
