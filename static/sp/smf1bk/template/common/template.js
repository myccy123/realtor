// document.documentElement.style.fontSize = document.documentElement.clientWidth / 100 + 'px';

const baseUrl = "http://www.realtoraccess.com/"
var url = window.location.href;
//var url = "http://www.realtoraccess.com/";
var strs = url.split("/"), str, userId
str = strs[strs.length - 1]
if (!str) {
    userId = strs[strs.length - 2]
} else {
    userId = strs[strs.length - 1]
}
let menuData = {
    menu: [
        { label: '首页', pageId: 0 },
        { label: '特色房源', pageId: 1 },
        { label: '关于我们', pageId: 2 },
        { label: '联系我们', pageId: 3 }],
    tel: ''
}
let menuData2 = {
    menu: [
        { label: '首页',pageId: 0 },
        { label: '特色房源', pageId: 1 },
        { label: '关于我们',pageId: 2 },
        { label: '联系我们',pageId: 3 }
    ]
}
let list = (data) => {
    let str = ''
    for (let i = 0; i < data.length; i++) {
        str += ` <li class="menu-item" id="${data[i].pageId}">${data[i].label}</li>`
    }
    return str
}
let list2 = (data) => {
    let str = ''
    for (let i = 0; i < data.length; i++) {
        str += ` <a  href=""><li class="menu-item ${i == 1 ? 'select' : ''}" id="${data[i].pageId}">${data[i].label}</li></a>`
    }
    return str
}
// 菜单栏
let svgSize=window.screen.width>=1080?'18px':'36px'
Vue.component('headmenu', {
    template: `
    <header>
        <div class="menu">
        <div class="show_box_header">
    		<img src="http://www.webmainland.com/static/web/agent4/src/img/wphone@3x.png"/>
    		<a :href="'tel:' + tel">{{tel}}</a>
    		<img src="http://www.webmainland.com/static/web/agent4/src/img/del.png"  @click="homehide($event)" class="showimg"/>
    	</div>
            <div class="container clear">
                <ul class="left">
                    <a :hre="gourl" @click="homehide($event)" ><li class="menu-item" id="0">首页</li></a>
                    <a :href="gourl" @click="homehide($event)" ><li class="menu-item" id="1">特色房源</li></a>
                    <a :href="gourl" @click="homehide($event)" ><li class="menu-item " id="2">关于我们</li></a>
                    <a :href="gourl" @click="homehide($event)" ><li class="menu-item " id="3">联系我们</li></a>
                </ul>
                <div class="right">
                    <svg class="iconfont-tel4"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                        width="${svgSize}" height="${svgSize}">
                    <image  x="0px" y="0px" width="${svgSize}" height="${svgSize}"  xlink:href="data:img/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAxCAMAAACvdQotAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABTVBMVEX////Yt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2v///9nqM62AAAAbXRSTlMAL4ufeBZz/eksd+prJPWzK/7SBvzoFCIwPIgccQP5zI9G4AVkDh77jp0zG9QIepfTXzH6PvA2AbAQ1/Im7W8gpuutJfirEVPkTa8hcHVmUvY359jJOZFMSZs4yL0KT86yjRpywAxEdri/vqBnh+I+/gAAAAFiS0dEAIgFHUgAAAAHdElNRQfjCRwTNBGEIYf2AAABaklEQVRIx5XUaVPCMBAG4AgKUhStULUiKIoi3uKBeIGKiuJ93+J97v//qnQYSWjSZN+PzTyzk3R3CbFS53LXNxBMPF4AaPQhhAZW/OqmCQBpmgOANS0ASNOqA9a4ALCmDbAmGKohYLRLSAfYoklIp524JcS0ky50lZDs/mEb6Za9WCSKvPxfetCC9KIFidGiL6JC+v20iasQti+NARUymKDNkFKZJE0SwypkJECb0TEVM86884QKCU4yZkrFpKZpEp1RMR6mzOycAknP401mgTGLMQWztMzO2Ur1KJszVtfWOcbMs1OwsVk58FlNyN1VWzXrqbBNCYGJ66yBnWJVCMxu7RrIu0xqNLhGA8dwzZ6ON/shvDk4xJujY0dzwlso4VNHc8brneC50yNc8BvusiAUelHQpJkrUaEcEeb6hitu78SEpO8fkKKMYiX2x3ofJaKcp+eX/13qLaXkwMrr23vy4/Pr+ydc+fALBRhs2RJR2CcAAAAASUVORK5CYII=" />
                    </svg>
                    <span class="inner-tel"> {{tel}}</span>
                </div>
                <div class="show_box_bot">
           			<a href="http://www.realtoraccess.com/web/page/signin/">Agent Login</a>
                	<a href="http://www.realtoraccess.com/web/page/signup/">Sign Up</a>
    				<img :src="qrcode"/>
    				<span>扫码添加微信</span>
    			</div>
            </div>
        </div>
    </header>`,
     props: ['tel','gourl','qrcode'],
     methods: {
    homehide: function (str) {
      this.$emit('homehidetap', '')
    }
  }
})
// 菜单栏
Vue.component('indexmenu', {
    template: `
    <header>
        <div class="menu">
        <div class="show_box_header">
    		<img src="http://www.webmainland.com/static/web/agent4/src/img/wphone@3x.png"/>
			<a :href="'tel:' + tel">{{tel}}</a>
    		<img src="http://www.webmainland.com/static/web/agent4/src/img/del.png"  @click="homehide($event)" class="showimg"/>
    	</div>
            <div class="container ">
                    <ul class="">
                    <a :href="gourl+'?pageId=0'"><li class="menu-item" id="0">首页</li></a>
                    <a :href="gourl+'?pageId=1'"><li class="menu-item select" id="1">特色房源</li></a>
                    <a :href="gourl+'?pageId=2'"><li class="menu-item " id="2">关于我们</li></a>
                    <a :href="gourl+'?pageId=3'"><li class="menu-item " id="3">联系我们</li></a>
                </ul>
                <div  v-if="!screesize">
                    <svg class="iconfont-tel4"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                        width="${svgSize}" height="${svgSize}">
                    <image  x="0px" y="0px" width="${svgSize}" height="${svgSize}"  xlink:href="data:img/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAxCAMAAACvdQotAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABTVBMVEX////Yt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2vYt2v///9nqM62AAAAbXRSTlMAL4ufeBZz/eksd+prJPWzK/7SBvzoFCIwPIgccQP5zI9G4AVkDh77jp0zG9QIepfTXzH6PvA2AbAQ1/Im7W8gpuutJfirEVPkTa8hcHVmUvY359jJOZFMSZs4yL0KT86yjRpywAxEdri/vqBnh+I+/gAAAAFiS0dEAIgFHUgAAAAHdElNRQfjCRwTNBGEIYf2AAABaklEQVRIx5XUaVPCMBAG4AgKUhStULUiKIoi3uKBeIGKiuJ93+J97v//qnQYSWjSZN+PzTyzk3R3CbFS53LXNxBMPF4AaPQhhAZW/OqmCQBpmgOANS0ASNOqA9a4ALCmDbAmGKohYLRLSAfYoklIp524JcS0ky50lZDs/mEb6Za9WCSKvPxfetCC9KIFidGiL6JC+v20iasQti+NARUymKDNkFKZJE0SwypkJECb0TEVM86884QKCU4yZkrFpKZpEp1RMR6mzOycAknP401mgTGLMQWztMzO2Ur1KJszVtfWOcbMs1OwsVk58FlNyN1VWzXrqbBNCYGJ66yBnWJVCMxu7RrIu0xqNLhGA8dwzZ6ON/shvDk4xJujY0dzwlso4VNHc8brneC50yNc8BvusiAUelHQpJkrUaEcEeb6hitu78SEpO8fkKKMYiX2x3ofJaKcp+eX/13qLaXkwMrr23vy4/Pr+ydc+fALBRhs2RJR2CcAAAAASUVORK5CYII=" />
                    </svg>
                    <span class="inner-tel"> {{tel}}</span>
                </div>
                <div class="show_box_bot">
                	<a href="http://www.realtoraccess.com/web/page/signin/">Agent Login</a>
                	<a href="http://www.realtoraccess.com/web/page/signup/">Sign Up</a>
					<img :src="qrcode"/>
					<span>扫码添加微信1</span>
    		</div>
            </div>
        </div>
    </header>`,
    props: ['tel','gourl','qrcode','screesize'],
    methods: {
    homehide: function (str) {
      this.$emit('homehidetap', '')
    }
  }
})

// 左侧
let asideData = {
    bg: '',
    website: '',
    logo: ''
}
Vue.component('asideCommon', {
    template: `<aside >
    <img class="inner-aside-bg" :src="myimg" alt="">
    <a class="inner-aside-jumpUrl" :href="website">
        <div class="house-footer">
            <span>
                <img class="inner-aside-log" :src="logo" alt="">
            </span>
        </div>
    </a>
    </aside>`,
    props: ['myimg','website','logo']
})
// 左侧logo
Vue.component('asideLogo', {
    template: ` <div class="house-footer">
    <a :href="gourl+'?pageId=0'"">
         <img class="inner-aside-log" :src="logo" alt="">
    </a>
</div>`,
props: ['logo','gourl']
})
if(url.indexOf('smart/flyer1')== -1){
    $.ajax({
        url: url + "/portal/agent/" + userId,
        type: "get",
        success: function (res) {
            document.querySelectorAll(".inner-tel")[0].innerHTML = JSON.parse(res).data.tel;
            document.querySelectorAll(".inner-aside-log")[0].setAttribute('src', JSON.parse(res).data.logo)
            if (document.querySelectorAll(".inner-aside-bg")[0]) {
                document.querySelectorAll(".inner-aside-bg")[0].setAttribute('src', JSON.parse(res).data.head)
                document.querySelectorAll(".inner-aside-jumpUrl")[0].setAttribute('href', JSON.parse(res).data.website)
            }
            sessionStorage.setItem('userObj', res)
        },
        error: function (res) {

        }
    })
}
function getParam(paramName) {
    paramValue = "", isFound = !1;
    if (this.location.search.indexOf("?") == 0 && this.location.search.indexOf("=") > 1) {
        arrSource = decodeURIComponent(this.location.search).substring(1, this.location.search.length).split("&"), i = 0;
        while (i < arrSource.length && !isFound) arrSource[i].indexOf("=") > 0 && arrSource[i].split("=")[0].toLowerCase() == paramName.toLowerCase() && (paramValue = arrSource[i].split("=")[1], isFound = !0), i++;
    }
    return paramValue == "" && (paramValue = null), paramValue;
}

