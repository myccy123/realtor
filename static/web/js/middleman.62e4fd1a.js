(function(t){function e(e){for(var s,o,c=e[0],r=e[1],l=e[2],v=0,m=[];v<c.length;v++)o=c[v],n[o]&&m.push(n[o][0]),n[o]=0;for(s in r)Object.prototype.hasOwnProperty.call(r,s)&&(t[s]=r[s]);d&&d(e);while(m.length)m.shift()();return i.push.apply(i,l||[]),a()}function a(){for(var t,e=0;e<i.length;e++){for(var a=i[e],s=!0,c=1;c<a.length;c++){var r=a[c];0!==n[r]&&(s=!1)}s&&(i.splice(e--,1),t=o(o.s=a[0]))}return t}var s={},n={middleman:0},i=[];function o(e){if(s[e])return s[e].exports;var a=s[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,o),a.l=!0,a.exports}o.m=t,o.c=s,o.d=function(t,e,a){o.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},o.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},o.t=function(t,e){if(1&e&&(t=o(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(o.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var s in t)o.d(a,s,function(e){return t[e]}.bind(null,s));return a},o.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return o.d(e,"a",e),e},o.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},o.p="http://www.realtoraccess.com/";var c=window["webpackJsonp"]=window["webpackJsonp"]||[],r=c.push.bind(c);c.push=e,c=c.slice();for(var l=0;l<c.length;l++)e(c[l]);var d=r;i.push([2,"chunk-vendors","chunk-common"]),a()})({"0d39":function(t,e,a){t.exports=a.p+"static/web/img/icon-pause.c40c886f.svg"},"0ff9":function(t,e,a){t.exports=a.p+"static/web/img/default-poster.704014b1.png"},"109c":function(t,e,a){t.exports=a.p+"static/web/img/icon-play.feca55d3.svg"},1304:function(t,e,a){t.exports=a.p+"static/web/img/default-house5.0e7ba83c.jpeg"},1631:function(t,e,a){t.exports=a.p+"static/web/img/icon-www.85bb18c9.svg"},2:function(t,e,a){t.exports=a("e69d")},"400e":function(t,e,a){t.exports=a.p+"static/web/img/icon-facebook-white.17f615de.svg"},"501c":function(t,e,a){},7127:function(t,e,a){"use strict";var s=a("501c"),n=a.n(s);n.a},"7c81":function(t,e,a){t.exports=a.p+"static/web/img/default-house3.1201f5ea.jpg"},"7d4a":function(t,e,a){t.exports=a.p+"static/web/img/default-house.1f681474.jpg"},"9d78":function(t,e,a){t.exports=a.p+"static/web/img/icon-weibo-white.dc3f63b8.svg"},e1e4:function(t,e,a){t.exports=a.p+"static/web/img/default-house2.aef2b42e.jpg"},e321:function(t,e,a){t.exports=a.p+"static/web/img/icon-email.75ae9dcf.svg"},e69d:function(t,e,a){"use strict";a.r(e);a("0fb7"),a("450d");var s=a("f529"),n=a.n(s),i=(a("7f7f"),a("cadf"),a("551c"),a("f751"),a("097d"),a("2b0e")),o=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"middleman"}},[s("div",{staticClass:"middleman-header"},[s("common-header",{attrs:{"nav-index":2}})],1),s("div",{staticClass:"middleman-banner"},[s("img",{attrs:{src:t.bannerUrl}}),s("div",{staticClass:"banner-masker"},[s("div",{staticClass:"agent-name"},[t._v(t._s(t.agentInfo.username))]),s("div",{staticClass:"agent-corp"},[t._v("\n        "+t._s(t.agentInfo.note||"海外房产投资估价")+"\n        "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n        "+t._s(t.agentInfo.corp||"大温专业房产经纪人")+"\n      ")]),s("div",{staticClass:"agent-visit"},[t._v("访问量："+t._s(t.visitNum))]),s("div",{staticClass:"agent-contact"},[s("div",{staticClass:"contact-type",on:{click:function(e){t.showCTDialog=!0}}},[s("span",{staticClass:"icon-contact banner-icon"}),t._v("联系方式\n        ")]),s("div",{staticClass:"chinese-service",on:{click:function(e){t.showCSDialog=!0}}},[s("span",{staticClass:"icon-service banner-icon"}),t._v("中文服务\n        ")])])]),s("div",{staticClass:"banner-share bdsharebuttonbox"},[s("a",{attrs:{href:"javascript:window.open('http://www.facebook.com/sharer.php?u='+encodeURIComponent(document.location.href)+'&t='+encodeURIComponent(document.title),'_blank','toolbar=yes, location=yes, directories=no, status=no, menubar=yes, scrollbars=yes, resizable=no, copyhistory=yes, width=600, height=450,top=100,left=350');void(0)"}},[s("img",{attrs:{src:a("400e"),alt:""}})]),s("a",{attrs:{href:"#"}},[s("img",{attrs:{"data-cmd":"tsina",src:a("9d78"),alt:""}})]),s("a",{attrs:{href:"#"}},[s("img",{attrs:{"data-cmd":"weixin",src:a("e7c0"),alt:""}})])])]),s("div",{staticClass:"middleman-detail"},[s("div",{staticClass:"agent-head"},[s("img",{staticClass:"agent-photo",attrs:{src:t.agentInfo.head,alt:""}}),t.agentInfo.auth?s("span",{staticClass:"agent-auth"},[t._v("认证经纪")]):t._e()]),s("div",{staticClass:"detail-descript"},[t._m(0),s("div",{staticStyle:{"margin-top":"2.4vw"}},[s("el-collapse-transition",[t.showAgentMore?s("span",[t._v(t._s(t.agentInfo.selfintro||t.normalAgentDesc))]):s("span",{staticClass:"descript-text"},[t._v(t._s(t.agentInfo.selfintro||t.normalAgentDesc))])])],1),s("span",{staticClass:"more",on:{click:function(e){t.showAgentMore=!t.showAgentMore}}},[t._v(t._s(t.showAgentMore?"收起":"详情")+">>")])])]),s("div",{staticClass:"middleman-recommend"},[s("div",{staticClass:"recommend-title font-title",attrs:{span:24}},[t._v("推荐房源")]),t.recommendData.length>0?s("div",{staticClass:"recommend-list"},t._l(t.recommendData,function(e,a){return s("div",{key:a,staticClass:"recommend-item",style:{backgroundImage:"url('"+e.img+"')"},on:{mouseover:function(e){t.recommendHoverIndex=a},mouseout:function(e){t.recommendHoverIndex=-1}}},[s("div",{directives:[{name:"show",rawName:"v-show",value:t.recommendHoverIndex!=a,expression:"recommendHoverIndex != index"}],staticClass:"item-agent"},[e.listingtype?s("span",[t._v(t._s(e.listingtype))]):t._e()]),s("transition",{attrs:{name:"el-fade-in-linear"}},[s("div",{directives:[{name:"show",rawName:"v-show",value:t.recommendHoverIndex==a,expression:"recommendHoverIndex == index"}],staticClass:"item-detail"},[s("div",{staticClass:"item-detail-price"},[t._v(t._s(e.price))]),s("div",{staticClass:"item-detail-addr"},[t._v(t._s(e.address))]),s("div",{staticClass:"item-detail-cityname"},[t._v(t._s(e.cityname))]),s("div",{staticClass:"item-detail-housetype"},[t._v("\n              "+t._s(e.housetype)+"\n              "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n              "+t._s(e.areas)+"\n            ")]),s("div",{staticClass:"item-detail-roomcount"},[s("span",{staticClass:"icon-furniture"},[t._v(" "+t._s(parseInt(e.toilet)||0))]),s("span",{staticClass:"icon-bed",staticStyle:{"margin-left":"12px"}},[t._v(" "+t._s(e.bedroom||0))])]),s("div",{staticClass:"item-detail-viewcount",staticStyle:{"margin-top":"8px"}},[s("span",{staticStyle:{"margin-right":"12px","line-height":"24px"}},[t._v(t._s(e.date))]),s("span",{staticClass:"icon-eye",staticStyle:{"margin-right":"12px","line-height":"24px"}},[t._v(t._s(e.visit))]),s("a",{attrs:{href:e.htmlid}},[t._v("查看房源")])])])])],1)}),0):s("div",{staticClass:"recommend-list"},[s("div",{staticClass:"recommend-item",style:{backgroundImage:"url("+a("2da5")}},[t._m(1)]),s("div",{staticClass:"recommend-item",style:{backgroundImage:"url("+a("1304")}},[t._m(2)])]),s("div",{staticStyle:{"text-align":"center"}},[s("span",{staticClass:"recommend-button",on:{click:t.handleCheckMore}},[t._v("查看更多")])])]),s("div",{staticClass:"agent-corp-wrap"},[s("div",{staticClass:"corp-video",on:{mouseover:function(e){t.showPlayButton=!0},mouseout:function(e){t.showPlayButton=!1}}},[s("div",{directives:[{name:"show",rawName:"v-show",value:t.showPlayButton,expression:"showPlayButton"}],staticClass:"button-play",on:{click:t.playVideo}},[s("img",{attrs:{src:t.iconPlayButton,alt:"",width:"100%",height:"100%"}})]),s("div",{staticClass:"video-wrap"},[t.agentInfo.corpVideo?s("video",{staticStyle:{"object-fit":"fill"},attrs:{src:t.agentInfo.corpVideo,width:"100%",height:"100%",poster:a("0ff9")}}):s("img",{attrs:{src:a("7d4a"),alt:"",width:"100%",height:"100%"}})])]),s("div",{staticClass:"corp-desc"},[t._m(3),s("div",{staticStyle:{"margin-top":"2.4vw"}},[t.showCorpMore?s("div",[t._v(t._s(t.agentInfo.corpintro))]):s("div",{staticClass:"desc-text"},[t._v(t._s(t.agentInfo.corpintro))])]),s("span",{staticClass:"more",on:{click:function(e){t.showCorpMore=!t.showCorpMore}}},[t._v(t._s(t.showCorpMore?"收起":"详情")+">>")])])]),s("div",{staticClass:"agent-personal-wrap"},[s("div",{staticClass:"personnal-banner"},[s("el-carousel",{attrs:{interval:3e3,height:"100%",width:"100%","indicator-position":"none"}},t._l(t.agentInfo.agentImgs,function(t){return s("el-carousel-item",{key:t},[s("div",{staticClass:"banner-item",style:{backgroundImage:"url("+t+")"}})])}),1)],1),s("div",{staticClass:"personnal-desc"},[t._m(4),s("div",{staticStyle:{"margin-top":"2.4vw"}},[t.showAboutMore?s("div",{staticClass:"desc-text-more"},[t._v(t._s(t.agentInfo.teamintro))]):s("div",{staticClass:"desc-text"},[t._v(t._s(t.agentInfo.teamintro))])]),s("span",{staticClass:"more",on:{click:function(e){t.showAboutMore=!t.showAboutMore}}},[t._v(t._s(t.showAboutMore?"收起":"详情")+">>")])])]),s("div",{staticClass:"agent-contact-wrap"},[s("div",{staticClass:"corp-logo"},[s("img",{staticStyle:{"object-fit":"contain"},attrs:{src:t.agentInfo.logo,alt:""}})]),s("div",{staticClass:"contact-detail"},[t._m(5),s("div",{staticClass:"detail-name"},[t._v(t._s(t.agentInfo.username))]),s("div",{staticClass:"detail-corp"},[t._v("\n        "+t._s(t.agentInfo.corp||"大温专业房产经纪人")+"\n        "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n        "+t._s(t.agentInfo.cityName)+" 房产经纪\n      ")]),s("div",{staticClass:"detail-phone"},[s("span",[s("img",{staticClass:"detail-icon",attrs:{src:a("f476"),alt:""}})]),s("span",[t._v(t._s(t.agentInfo.tel||"400 877 1896"))])]),s("div",{staticClass:"detail-email"},[s("span",[s("img",{staticClass:"detail-icon",attrs:{src:a("e321"),alt:""}})]),s("span",[t._v(t._s(t.agentInfo.email))])]),s("div",{staticClass:"detail-addr"},[s("span",[s("img",{staticClass:"detail-icon",attrs:{src:a("eafa"),alt:""}})]),s("span",[t._v(t._s(t.agentInfo.address||"Vancouver, BC, Canada"))])]),s("div",{staticClass:"detail-website"},[s("span",[s("img",{staticClass:"detail-icon",attrs:{src:a("1631"),alt:""}})]),s("span",[t._v(t._s(t.agentInfo.website||"www.realtoraccess.com"))])])])]),s("div",{directives:[{name:"show",rawName:"v-show",value:t.showQrcode,expression:"showQrcode"}],staticClass:"fix-qrcode"},[s("span",{staticClass:"el-icon-close qrcode-close",on:{click:function(e){t.showQrcode=!1}}}),s("img",{attrs:{src:t.agentInfo.qrcode,alt:""}}),s("p",{staticStyle:{"text-align":"center"}},[t._v("扫一扫添加好友")])]),s("div",{staticClass:"agent-signin-wrap"},[s("span",{staticClass:"signin-text font-title"},[t._v("海外房产经纪人?")]),s("el-button",{attrs:{type:"primary"}},[s("a",{staticStyle:{color:"#fff"},attrs:{href:"/web/page/signup"}},[t._v("免费注册")])])],1),s("CommonFooter"),s("el-dialog",{attrs:{visible:t.showCTDialog,width:"80%","lock-scroll":!1,center:"","show-close":!1},on:{"update:visible":function(e){t.showCTDialog=e}}},[s("div",{staticClass:"dialog-title",attrs:{slot:"title"},slot:"title"},[s("span",[t._v("经纪人联系方式")]),s("span",{staticClass:"el-icon-close dialog-close",on:{click:t.handleClose}})]),s("el-row",[s("el-col",{staticStyle:{"text-align":"center"},attrs:{span:10}},[s("img",{attrs:{src:t.agentInfo.qrcode,alt:"",width:"80%",height:"auto"}}),s("p",{staticClass:"scan-add"},[t._v("扫一扫添加我为微信好友")])]),s("el-col",{staticClass:"contact-info",attrs:{span:14}},[s("p",{staticClass:"name"},[t._v(t._s(t.agentInfo.username))]),s("p",{staticClass:"company"},[t._v("\n          "+t._s(t.agentInfo.note||"海外房产投资估价")+"\n          "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n          "+t._s(t.agentInfo.cityName)+"\n        ")]),s("p",{staticClass:"contact-method"},[t._v("\n          电话\n          "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n          "+t._s(t.agentInfo.tel||"400 877 1896")+"\n        ")]),s("p",{staticClass:"contact-method"},[t._v("\n          邮箱\n          "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n          "+t._s(t.agentInfo.email)+"\n        ")]),s("p",{staticClass:"contact-method"},[t._v("\n          地址\n          "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n          "+t._s(t.agentInfo.address||"Vancouver, BC, Canada")+"\n        ")]),s("p",{staticClass:"contact-method"},[t._v("\n          网站\n          "),s("span",{staticClass:"vl"},[t._v("|")]),s("a",{attrs:{href:"http://"+t.agentInfo.website,target:"_blank"}},[t._v(t._s(t.agentInfo.website||"www.realtoraccess.com"))])])])],1)],1),s("el-dialog",{attrs:{visible:t.showCSDialog,width:"64vw","lock-scroll":!1,center:"","show-close":!1},on:{"update:visible":function(e){t.showCSDialog=e}}},[s("div",{staticClass:"dialog-title",attrs:{slot:"title"},slot:"title"},[s("span",[t._v("中文服务")]),s("span",{staticClass:"el-icon-close dialog-close",on:{click:t.handleClose}})]),s("div",[s("div",{staticStyle:{width:"26vw",float:"left"}},[s("el-input",{attrs:{placeholder:"您的姓名"},model:{value:t.serviceParams.custname,callback:function(e){t.$set(t.serviceParams,"custname",e)},expression:"serviceParams.custname"}}),s("el-input",{attrs:{placeholder:"您的邮箱"},model:{value:t.serviceParams.custemail,callback:function(e){t.$set(t.serviceParams,"custemail",e)},expression:"serviceParams.custemail"}}),s("el-input",{attrs:{placeholder:"免费注册获取我的独家地产资讯",type:"textarea",rows:3,resize:"none"},model:{value:t.serviceParams.custmsg,callback:function(e){t.$set(t.serviceParams,"custmsg",e)},expression:"serviceParams.custmsg"}}),s("el-button",{attrs:{type:"primary",disabled:!t.canSend},on:{click:t.handleSend}},[t._v("发送")])],1),s("div",{staticStyle:{width:"22vw",float:"right"}},[s("div",{staticClass:"dialog-chinese-service"},[s("div",{staticClass:"qrcode"},[s("p",{staticStyle:{"line-heigt":"1.5em"}},[t._v("扫一扫添加我为微信好友")]),s("img",{attrs:{src:t.agentInfo.qrcode2,alt:""}})]),s("p",{staticClass:"name"},[t._v(t._s(t.agentInfo.username2))]),s("p",{staticClass:"contact-method"},[t._v("\n            电话\n            "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n            "+t._s(t.agentInfo.tel2||"400-877-1896")+"\n          ")]),s("p",{staticClass:"contact-method"},[t._v("\n            邮箱\n            "),s("span",{staticClass:"vl"},[t._v("|")]),t._v("\n            "+t._s(t.agentInfo.email2||"info@realtoraccess.com")+"\n          ")])])]),s("div",{staticStyle:{clear:"both"}})])])],1)},c=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"detail-title font-title"},[a("span",[t._v("个人")]),t._v("介绍\n      ")])},function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"item-agent"},[a("span",[t._v("敬请期待")])])},function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"item-agent"},[a("span",[t._v("敬请期待")])])},function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"desc-title font-title"},[a("span",[t._v("公司")]),t._v("简介\n      ")])},function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"desc-title font-title"},[a("span",[t._v("关于")])])},function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"detail-title font-title"},[a("span",[t._v("联系")]),t._v("方式\n      ")])}],r=a("a1d8"),l=a.n(r),d=a("abde"),v=a.n(d),m=a("f9c1"),u=a.n(m),p=a("d9ca"),g=a.n(p),f=a("5520"),h=a("596d"),_=a("109c"),w=a.n(_),C=a("0d39"),b=a.n(C),y=a("2e20"),I=a("6e55"),x=a("5118"),S={name:"Middleman",components:{CommonHeader:f["a"],CommonFooter:h["a"]},data:function(){return{logoUrl:l.a,bannerUrl:v.a,middlemanUrl:u.a,qrcodeUrl:g.a,showCTDialog:!1,showCSDialog:!1,agentInfo:{},agentId:222,sortMethod:"date",serviceParams:{custname:"",custemail:"",custmsg:""},sr:Object(I["a"])(),allRecommendData:[],recommendData:[],recommendHoverIndex:-1,visitData:{visit:0,totalVist:0},normalAgentDesc:"欢迎您来我的中文网站，我是一名专业的海外房产经纪人。在这里您将看到我的介绍，我所代理的特色房源和我的团队介绍，无论您是首次置业者或者专业的海外房产投资人，或者要售出您的房屋，我都能为您提供全程房屋买售服务与专业的海外房产置业方案。",showPlayButton:!0,iconPlayButton:w.a,video:null,showQrcode:!0,showAgentMore:!1,showCorpMore:!1,showAboutMore:!1,viewMoreIndex:1}},computed:{canSend:function(){return this.serviceParams.custname&&this.serviceParams.custemail&&this.serviceParams.custmsg},visitNum:function(){return this.visitData.visit.toFixed(0)}},methods:{getOptions:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:function(){},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:function(){},a={duration:500,delay:100,reset:!0,desktop:!0,distance:"-100px",viewFactor:.1,beforeReveal:t,afterReveal:e};return a},setScrollReveal:function(){var t=this;this.sr.reveal(".middleman-banner",this.getOptions(function(){t.visitData.visit=0},function(){t.visitData.totalVisit>0&&y["a"].to(t.visitData,2,{visit:t.visitData.totalVisit})})),this.sr.reveal(".middleman-detail",this.getOptions()),this.sr.reveal(".middleman-recommend",this.getOptions(function(){})),this.sr.reveal(".agent-corp-wrap",this.getOptions()),this.sr.reveal(".agent-personal-wrap",this.getOptions()),this.sr.reveal(".agent-contact-wrap",this.getOptions()),this.sr.reveal(".agent-signin-wrap",this.getOptions()),this.sr.reveal(".middleman-recommend .recommend-item",{reset:!0,interval:160})},handleCheckMore:function(){this.allRecommendData.length<=this.recommendData.length||(this.viewMoreIndex++,this.recommendData=this.allRecommendData.slice(0,2*this.viewMoreIndex))},handleClose:function(){this.showCTDialog=!1,this.showCSDialog=!1},getAgentById:function(){var t=this;this.$get(this.$api.AGENT_BYID+"/"+this.agentId).then(function(e){t.agentInfo=e,console.log(t.agentInfo),t.agentInfo.username=t.agentInfo.username.toUpperCase(),0==t.agentInfo.agentImgs.length&&(t.agentInfo.agentImgs.push(a("e1e4")),t.agentInfo.agentImgs.push(a("7c81"))),t.visitData.totalVisit=parseInt(e.visit);try{var s=document.querySelectorAll("meta");s[2].content="".concat(e.username,",").concat(e.username,"房产经纪人,").concat(e.corp).concat(e.username,",").concat(e.note),s[3].content="".concat(e.username,"是").concat(e.corp,"的房产经纪人,").concat(e.note,",").concat(e.username,"是经过瑞安居认证的可信赖的房产经纪人,更多").concat(e.username,"的信誉信息和正在经纪的海外房产信息就来海外瑞安居。");var n=document.querySelector("title");n.innerHTML="【".concat(e.username,"房产经纪人_").concat(e.corp,"_").concat(e.note,"】-海外瑞安居RealtorAccess.com")}catch(i){console.log(i)}wxImgUrl=t.agentInfo.head2,y["a"].to(t.visitData,2,{visit:t.visitData.totalVisit}),t.$nextTick(function(){t.setScrollReveal(),t.agentInfo.corpVideo&&(t.video=document.querySelector("video"),console.log(t.video))})})},getAgentListing:function(){var t=this;this.$get("".concat(this.$api.AGENT_LISTINGS,"/?id=").concat(this.agentId,"&sort=").concat(this.sortMethod)).then(function(e){t.recommendData=e.slice(0,2),t.allRecommendData=e,t.$nextTick(function(){t.setScrollReveal()})})},handleSend:function(){var t=this;agentInfo.userid,serviceParams.custname,serviceParams.custemail,serviceParams.custmsg;this.$post(this.$api.AGENT_CHINESE_SERVICE).then(function(e){t.$message({type:"success",message:"发送成功"})})},playVideo:function(){var t=this;this.agentInfo.corpVideo&&(this.video.addEventListener("play",function(){t.iconPlayButton=b.a}),this.video.addEventListener("ended",function(){t.iconPlayButton=w.a,t.showPlayButton=!0}),this.video.paused?(this.video.play(),this.iconPlayButton=b.a):(this.video.pause(),this.iconPlayButton=w.a))}},mounted:function(){var t=this,e=window.location.href;e.lastIndexOf("/")==e.length-1&&(e=e.substr(0,e.length-1)),this.agentId=e.substring(e.lastIndexOf("/")+1),this.getAgentById(),this.getAgentListing(),Object(x["setTimeout"])(function(){t.showCSDialog=!0},6e3)}},k=S,P=(a("7127"),a("2877")),D=Object(P["a"])(k,o,c,!1,null,null,null),M=D.exports,A=(a("adf6"),a("7378"),a("e05f"),a("bc3a")),$=a.n(A),E="http://www.realtoraccess.com",O={AGENT_BYID:E+"/portal/agent",AGENT_LISTINGS:E+"/portal/agent/listings",AGENT_CHINESE_SERVICE:E+"/portal/chinese/service"},T=(a("d21e"),a("61d8"),a("5488")),j=a.n(T);i["default"].component(j.a.name,j.a),i["default"].prototype.$api=O,i["default"].prototype.$message=n.a,i["default"].prototype.$get=function(t){return new Promise(function(e,a){$.a.get(t).then(function(t){200==t.status&&("00"==t.data.code?e(t.data.data):a("请求失败"))})})},i["default"].prototype.$post=function(t,e){return new Promise(function(a,s){$.a.post(t,e).then(function(t){200==t.status&&("00"==t.data.code?a(t.data.data):s("请求失败"))})})},new i["default"]({render:function(t){return t(M)}}).$mount("#middleman")},e7c0:function(t,e,a){t.exports=a.p+"static/web/img/icon-wechat-white.288a1250.svg"},eafa:function(t,e,a){t.exports=a.p+"static/web/img/icon-location.e6537f38.svg"},f476:function(t,e,a){t.exports=a.p+"static/web/img/icon-phone.7e13a27c.svg"}});