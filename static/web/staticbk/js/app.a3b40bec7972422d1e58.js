webpackJsonp([1],{Hzne:function(t,e){},IBoS:function(t,e,s){t.exports=s.p+"static/img/logo_main_new.e8729e4.png"},JETS:function(t,e,s){t.exports=s.p+"static/img/logo_wechat.fd3a831.png"},MrDw:function(t,e,s){t.exports=s.p+"static/img/no_data.a68cc7f.jpg"},NHnr:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=s("7+uW"),i=s("/ocq"),o=s("mtWM"),n=s.n(o),r=s("f+Au"),l={name:"el-sl-panel",props:{color:{required:!0}},computed:{colorValue:function(){return{hue:this.color.get("hue"),value:this.color.get("value")}}},watch:{colorValue:function(){this.update()}},methods:{update:function(){var t=this.color.get("saturation"),e=this.color.get("value"),s=this.$el.getBoundingClientRect(),a=s.width,i=s.height;i||(i=3*a/4),this.cursorLeft=t*a/100,this.cursorTop=(100-e)*i/100,this.background="hsl("+this.color.get("hue")+", 100%, 50%)"},handleDrag:function(t){var e=this.$el.getBoundingClientRect(),s=t.clientX-e.left,a=t.clientY-e.top;s=Math.max(0,s),s=Math.min(s,e.width),a=Math.max(0,a),a=Math.min(a,e.height),this.cursorLeft=s,this.cursorTop=a,this.color.set({saturation:s/e.width*100,value:100-a/e.height*100})}},mounted:function(){var t=this;Object(r.a)(this.$el,{drag:function(e){t.handleDrag(e)},end:function(e){t.handleDrag(e)}}),this.update()},data:function(){return{cursorTop:0,cursorLeft:0,background:"hsl(0, 100%, 50%)"}}},c={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"el-color-svpanel",style:{backgroundColor:this.background}},[e("div",{staticClass:"el-color-svpanel__white"}),this._v(" "),e("div",{staticClass:"el-color-svpanel__black"}),this._v(" "),e("div",{staticClass:"el-color-svpanel__cursor",style:{top:this.cursorTop+"px",left:this.cursorLeft+"px"}},[e("div")])])},staticRenderFns:[]},p=s("VU/8")(l,c,!1,null,null,null).exports,u=s("Au9i"),d=s.n(u),h={components:{ElSlPanel:p},data:function(){return{popugroup:!1,popupVisible:!0,popupShowNecessery:!0,filterPopupVisible:!1,baiduurl:"",houses:[],countries:[],provs:[],groups:[],cities:[],types:[{name:"二手(MLS)房源",value:"saling"},{name:"楼花房源",value:"presale"},{name:"出租房源",value:"rent"}],country:"Canada",prov:"BC",group:"REBGV",city:"Vancouver",opendate:"",housetypeValue:"二手(MLS)房源",housetype:"saling",endtime:"2018年05月18日",countryname:"选择国家",provname:"选择省份",groupname:"大温地区",cityname:"温哥华",map:{},marker:{},center:{lat:49.2827291,lng:-123.1207375},zoom:12,loading:!0,markers:[],eventType:"map",currentIndex:0,lastIndex:0,clickLastIndex:0,buttonBottom:0,wechat:!1,wechatUrl:"../../static/logo_wechat.png",no_data_default:!1,isClickMarker:!1,pickerStarttime:new Date,startDate:new Date("2018"),STime:"公众开放日开始时间",ETime:"公众开放日结束时间",pickerEndStarttime:new Date}},created:function(){var t=this;n.a.get("http://www.realtoraccess.com/web/get/groups/",{params:{provid:this.prov}}).then(function(e){t.groups=e.data}),n.a.get("http://www.realtoraccess.com/web/get/cities/",{params:{groupid:this.group}}).then(function(e){t.cities=e.data})},mounted:function(){var t=this,e=document.getElementById("map");this.map=new google.maps.Map(e,{zoom:this.zoom,center:this.center});n.a.get("http://www.realtoraccess.com/web/zone/listings/",{params:{country:this.country,prov:this.prov,group:this.group,city:this.city,opendate:this.opendate,housetype:this.housetype}}).then(function(e){t.houses=e.data,null!=t.houses&&0!==t.houses.length||(t.no_data_default=!0),e.data.forEach(t.generateMarker),t.loading=!1}),document.getElementById("list").addEventListener("scroll",this.handleScroll)},methods:{formatDate:function(t){var e=t.getFullYear(),s=t.getMonth()+1;s=s<10?"0"+s:s;var a=t.getDate();return e+"年"+s+"月"+(a=a<10?"0"+a:a)+"日"},openPicker:function(t){this.$refs[t].open()},popuWchat:function(){this.wechat=!0},generateMarker:function(t,e){var s=t.lat,a=t.lng;""!==s&&""!==a&&this.createdMarker(t.lat,t.lng,t.price,e)},createdMarker:function(t,e,s,a){var i=this,o=new google.maps.Marker({icon:"http://maps.google.cn/mapfiles/ms/icons/red-dot.png",position:{lat:Number(t),lng:Number(e)},map:this.map,ent_type:"marker"});0===a&&(this.currentIndex=a,this.map.setCenter(o.getPosition()),o.setIcon("http://maps.google.cn/mapfiles/ms/icons/blue-dot.png")),this.markers.push(o),google.maps.event.addListener(o,"click",function(s){i.markerClick(a,o,t,e)})},handleClick:function(){this.popupVisible=!0},toggle:function(){"marker"===this.eventType?(this.popupShowNecessery&&(this.popupVisible=!0,this.popupShowNecessery=!1),this.eventType="map"):this.popupVisible?this.popupVisible=!1:this.popupVisible=!0},showfilter:function(){this.filterPopupVisible?this.filterPopupVisible=!1:this.filterPopupVisible=!0,this.popupVisible=!0},selectCompleted:function(){this.filterPopupVisible=!1,this.opendate=this.startTime+"-"+this.endTime,this.getFilterHouse(),this.loading=!0},close:function(){this.filterPopupVisible=!1},handleGroup:function(t){this.groupname=this.groups[t].groupname,this.group=this.groups[t].groupid,this.getcity(this.groups[t].groupid)},handleCity:function(t){this.cityname=this.cities[t].cityname,this.city=this.cities[t].cityid},handleHouseType:function(t){this.housetypeValue=this.types[t].name,this.housetype=this.types[t].value},getprov:function(t){var e=this;n.a.get("http://www.realtoraccess.com/web/get/provs/",{params:{countryid:t}}).then(function(t){e.provs=t.data})},getgroup:function(t){var e=this;n.a.get("http://www.realtoraccess.com/web/get/groups/",{params:{provid:t}}).then(function(t){e.groups=t.data})},getcity:function(t){var e=this;n.a.get("http://www.realtoraccess.com/web/get/cities/",{params:{groupid:t}}).then(function(t){e.cities=t.data})},getFilterHouse:function(){var t=this;console.log(this.country+"----"+this.prov+"----"+this.group+"----"+this.city+"----"+this.housetype),n.a.get("http://www.realtoraccess.com/web/zone/listings/",{params:{country:this.country,prov:this.prov,group:this.group,city:this.city,opendate:this.opendate,housetype:this.housetype}}).then(function(e){t.houses=e.data,null==t.houses||0===t.houses.length?t.no_data_default=!0:t.no_data_default=!1;for(var s=0;s<t.markers.length;s++)t.markers[s].setMap(null);console.log(t.houses),t.markers=[],t.houses.forEach(t.generateMarker),t.loading=!1}).catch(function(t){console.log(t)})},changeStartTime:function(t){this.startTime=new Date(t).getTime(),this.STime=this.formatDate(t)},changeEndTime:function(t){this.endTime=new Date(t).getTime(),this.endTime<this.startTime&&Object(u.Toast)({message:"结束日期不能早于开始日期",position:"bottom"}),this.ETime=this.formatDate(t)},markerClick:function(t,e,s,a){this.eventType="marker",this.popupVisible?this.popupShowNecessery=!1:this.popupShowNecessery=!0,console.log("click-------lastIndex :"+this.lastIndex+"currentIndex : "+this.currentIndex+"index : "+t),this.handleList(t,s,a)},handleList:function(t,e,s){var a=this;if(a.isClickMarker=!0,this.markers[this.lastIndex].setIcon("http://maps.google.cn/mapfiles/ms/icons/red-dot.png"),this.map.setCenter({lat:Number(e),lng:Number(s)}),this.markers[t].setIcon("http://maps.google.cn/mapfiles/ms/icons/blue-dot.png"),this.lastIndex=t,this.currentIndex!==t){this.currentIndex=t;var i=document.getElementById("listitem").offsetWidth,o=(i+12)*t,n=document.getElementById("list"),r=0,l=0,c=setInterval(function(){l=(i+12)*r,r>=t?(n.scrollTo(o,0),a.isClickMarker=!1,clearInterval(c)):n.scrollTo(l,0),r++},5)}},handleScroll:function(){var t=document.getElementById("list").scrollLeft,e=document.getElementById("listitem").offsetWidth+12,s=Math.ceil(t/e);(parseFloat(t)/parseFloat(e)).toFixed(2)>s-.05&&(this.currentIndex=s),s>=this.houses.length&&(this.currentIndex=this.houses.length-1);var a=this.markers[this.currentIndex];(this.currentIndex!==s||this.lastIndex>this.currentIndex)&&!this.isClickMarker&&(this.map.setCenter(a.getPosition()),-1!==this.lastIndex&&(this.markers[this.lastIndex].setIcon("http://maps.google.cn/mapfiles/ms/icons/red-dot.png"),a.setIcon("http://maps.google.cn/mapfiles/ms/icons/blue-dot.png")),this.lastIndex=this.currentIndex),console.log("lastIndex : "+this.lastIndex+"----\x3ecurrentIndex :  "+this.currentIndex+"-----—>index :  "+s)}}},m={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"container"},[a("div",{staticClass:"page-popup-wrapper",staticStyle:{position:"absolute",width:"100%","z-index":"999"}},[a("mt-header",{staticClass:"header"},[a("router-link",{attrs:{slot:"left",to:"/"},slot:"left"},[a("mt-button",{staticClass:"header-left"},[a("img",{staticClass:"icon",attrs:{slot:"icon",src:s("IBoS"),width:"35",height:"35"},slot:"icon"}),t._v(" "),a("span",{staticClass:"header-left"},[t._v("99%的大温地产投资精英都在关注")])])],1),t._v(" "),a("span",{staticClass:"header-right",attrs:{slot:"right"},on:{click:t.popuWchat},slot:"right"},[t._v("关注")])],1)],1),t._v(" "),a("mt-popup",{staticClass:"mint-popup-wechat",style:{top:t.buttonBottom+10+"px"},attrs:{"popup-transition":"popup-fade"},model:{value:t.wechat,callback:function(e){t.wechat=e},expression:"wechat"}},[a("img",{staticClass:"wechatimg",attrs:{src:s("JETS"),alt:"公众号二维码"}}),t._v(" "),a("span",{staticClass:"wetchat_text"},[t._v("长按识别二维码")])]),t._v(" "),a("div",{staticClass:"map",attrs:{id:"map"},on:{click:t.toggle}}),t._v(" "),a("mt-button",{staticClass:"mapfilter",attrs:{size:"small"},on:{click:t.showfilter}},[t._v("筛选条件")]),t._v(" "),a("div",{staticClass:"gallery",attrs:{id:"gallery"}},[a("mt-popup",{staticClass:"mint-popup",attrs:{position:"bottom",modal:!1},model:{value:t.popupVisible,callback:function(e){t.popupVisible=e},expression:"popupVisible"}},[a("img",{directives:[{name:"show",rawName:"v-show",value:t.no_data_default,expression:"no_data_default"}],staticClass:"gallery_img",attrs:{src:s("MrDw")}}),t._v(" "),a("mt-button",{staticClass:"filter",attrs:{size:"small",id:"btnfilter"},on:{click:t.showfilter}},[t._v("筛选条件")]),t._v(" "),a("transition",{attrs:{name:"bounce"}},[a("ul",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],staticClass:"list-house",attrs:{"element-loading-text":"加载中...","element-loading-spinner":"el-icon-loading",id:"list"}},[t._l(t.houses,function(e,s){return a("li",{key:s,staticClass:"item-houe",class:{active:t.currentIndex==s},attrs:{id:"listitem"}},[a("div",{staticClass:"selectstatus"}),t._v(" "),a("a",{staticStyle:{"text-decoration":"none"},attrs:{href:e.url}},[a("img",{staticClass:"img-house",attrs:{src:e.img,alt:"房源图片"}}),t._v(" "),a("div",{staticClass:"desc-house"},[a("p",{staticClass:"address"},[t._v(t._s(e.address))]),t._v(" "),a("p",{staticClass:"configure"},[t._v(t._s(e.bedroom)+"室"+t._s(e.toilet)+"卫  "+t._s(e.areas))]),t._v(" "),a("p",{staticClass:"type"},[t._v(t._s(e.housetype))]),t._v(" "),a("p",{staticClass:"price"},[t._v(t._s(e.price))])])])])}),t._v(" "),a("li",{staticStyle:{width:"50%"}})],2)])],1)],1),t._v(" "),a("div",[a("mt-popup",{staticClass:"filter-popup",attrs:{position:"top",modal:!1},model:{value:t.filterPopupVisible,callback:function(e){t.filterPopupVisible=e},expression:"filterPopupVisible"}},[a("div",[a("mt-header",{attrs:{title:"筛选条件"}},[a("router-link",{attrs:{slot:"right",to:"/"},slot:"right"},[a("mt-button",{on:{click:t.close}},[t._v("关闭")])],1)],1),t._v(" "),a("div",{staticClass:"select"},[a("span",{staticClass:"selectdec"},[t._v("选择大区：")]),t._v(" "),a("el-dropdown",{staticClass:"selectgroup",attrs:{placement:"bottom-start",trigger:"click"},on:{command:t.handleGroup}},[a("el-button",{staticClass:"selectdecin",attrs:{type:"default"}},[t._v("\n             "+t._s(t.groupname)+"\n           ")]),t._v(" "),a("el-dropdown-menu",{staticClass:"selectgroup",attrs:{slot:"dropdown"},slot:"dropdown"},t._l(t.groups,function(e,s){return a("el-dropdown-item",{key:s,attrs:{command:s}},[t._v(t._s(e.groupname))])}))],1)],1),t._v(" "),a("div",{staticClass:"select"},[a("span",{staticClass:"selectdec"},[t._v("选择城市：")]),t._v(" "),a("el-dropdown",{staticClass:"selectgroup",attrs:{placement:"bottom-start",trigger:"click"},on:{command:t.handleCity}},[a("el-button",{staticClass:"selectdecin",attrs:{type:"default"}},[t._v("\n             "+t._s(t.cityname)+"\n           ")]),t._v(" "),a("el-dropdown-menu",{staticClass:"selectgroup",attrs:{slot:"dropdown"},slot:"dropdown"},t._l(t.cities,function(e,s){return a("el-dropdown-item",{key:s,attrs:{command:s}},[t._v(t._s(e.cityname))])}))],1)],1),t._v(" "),a("div",{staticClass:"select"},[a("span",{staticClass:"selectdec"},[t._v("房源类型：")]),t._v(" "),a("el-dropdown",{staticClass:"selectgroup",attrs:{placement:"bottom-start",trigger:"click"},on:{command:t.handleHouseType}},[a("el-button",{staticClass:"selectdecin",attrs:{type:"default"}},[t._v("\n             "+t._s(t.housetypeValue)+"\n           ")]),t._v(" "),a("el-dropdown-menu",{staticClass:"selectgroup",attrs:{slot:"dropdown"},slot:"dropdown"},t._l(t.types,function(e,s){return a("el-dropdown-item",{key:s,attrs:{command:s}},[t._v(t._s(e.name))])}))],1)],1)],1),t._v(" "),a("div",{staticClass:"select"},[a("div",[a("span",{staticClass:"selectdec"},[t._v("开始时间：")]),t._v(" "),a("el-button",{staticClass:"selectgroup",attrs:{type:"default"},nativeOn:{click:function(e){t.openPicker("start")}}},[t._v("\n           "+t._s(t.STime)+"\n         ")])],1),t._v(" "),a("mt-datetime-picker",{ref:"start",attrs:{type:"date","year-format":"{value} 年","month-format":"{value} 月","date-format":"{value} 日",startDate:t.startDate},on:{confirm:function(e){return t.changeStartTime(e)}},model:{value:t.pickerStarttime,callback:function(e){t.pickerStarttime=e},expression:"pickerStarttime"}})],1),t._v(" "),a("div",{staticClass:"select"},[a("div",[a("span",{staticClass:"selectdec"},[t._v("结束时间：")]),t._v(" "),a("el-button",{staticClass:"selectgroup",attrs:{type:"default"},nativeOn:{click:function(e){t.openPicker("end")}}},[t._v("\n           "+t._s(t.ETime)+"\n         ")])],1),t._v(" "),a("mt-datetime-picker",{ref:"end",attrs:{type:"date","year-format":"{value} 年","month-format":"{value} 月","date-format":"{value} 日",startDate:t.startDate},on:{confirm:function(e){return t.changeEndTime(e)}},model:{value:t.pickerEndStarttime,callback:function(e){t.pickerEndStarttime=e},expression:"pickerEndStarttime"}})],1),t._v(" "),a("mt-button",{staticClass:"btnconfirm",attrs:{type:"primary",size:"large"},on:{click:t.selectCompleted}},[t._v("确定")])],1)],1)],1)},staticRenderFns:[]};var g=s("VU/8")(h,m,!1,function(t){s("enGN")},"data-v-3a29689b",null).exports;a.default.use(i.a);var v=new i.a({routes:[{path:"/",name:"newmap",component:g}]}),f=(s("d8/S"),{render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("router-view")],1)},staticRenderFns:[]});var _=s("VU/8")({name:"App"},f,!1,function(t){s("Hzne")},null,null).exports,w=s("zL8q"),y=s.n(w);s("tvR6");a.default.use(d.a),a.default.use(y.a),new a.default({el:"#app",router:v,components:{App:_},template:"<App/>"})},"d8/S":function(t,e){},enGN:function(t,e){},tvR6:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.a3b40bec7972422d1e58.js.map