
let BASE_URL = 'http://119.3.241.33:9000';
let chartMap = {};
let timers = new Set();

function getParam(name) {
    const reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    const r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return unescape(r[2]);
    }
    return null;
}


function initMap(map) {
    return new Promise((resolve, reject) => {
        if (!map) {
            resolve();
        } else {
            axios.get(BASE_URL + '/ccb/map/', {params: {mapfile: map}}).then((res) => {
                echarts.registerMap(map, res.data);
                console.log(`地图（${map}）初始化成功！`);
                resolve();

            }).catch((err) => {
                console.log(err);
                reject();
            })
        }
    })
}

function appendChart(domId, chartObj) {
    if(chartMap.hasOwnProperty(domId)) {
        chartMap[domId].dispose()
    }
    chartMap[domId] = chartObj
}

function genChart(domId, chartId, options = {}, commonTheme) {

    let dom = document.getElementById(domId);

    if (!chartId) {
        return
    }
    axios.post(BASE_URL + '/ccb/get/chart/', {id: chartId, ...options}).then((res) => {
        if (res.data.code === '00') {
            initMap(res.data.data.formOptions.moreConfig.map).then(() => {
                echarts.dispose(dom);
                if (res.data.data.formOptions.chartType === 'tableBasic') {
                    let tableExtend = Vue.extend(TableExtend);
                    let tableComponent = new tableExtend({
                        propsData: {
                            chartId: chartId,
                            domId: domId,
                            tableConfig: res.data.data.formOptions.tableConfig,
                            srcid: res.data.data.formOptions.srcid
                        }
                    });
                    tableComponent.$mount(`#${domId}`);

                } else if (res.data.data.formOptions.chartType === 'htmlBasic') {
                    let htmlExtend = Vue.extend(HtmlExtend);
                    let htmlComponent = new htmlExtend({
                        propsData: {
                            chartId: chartId,
                            domId: domId,
                            htmlCode: res.data.data.diyCode
                        }
                    });
                    htmlComponent.$mount(`#${domId}`);
                } else {
                    let theme = commonTheme ? commonTheme : res.data.data.theme;
                    if (res.data.data.chartType === 'diy') {
                        let jsCode = `
                            var ${domId} = echarts.init(document.getElementById('${domId}'), '${theme}', {renderer: 'canvas'})
                            ${res.data.data.diyCode};
                            ${domId}.setOption(option);
                            return ${domId}`.replace(/chartObj/g, domId);
                        let jsFun = new Function(jsCode);
                        let myChart = jsFun();
                        appendChart(domId, myChart)

                    } else {
                        let myChart = echarts.init(dom, theme);
                        myChart.setOption(res.data.data.chartOptions);
                        appendChart(domId, myChart)
                    }
                }

            })

        } else {
            dom.innerText = JSON.stringify(res.data, null, 4)
        }
    }).catch((err) => {
        console.log(err);
    })
}




function disposeAll() {
    for (let c in chartMap) {
        chartMap[c].dispose();
        delete chartMap[c]
    }
    for (let tm of timers) {
        window.clearInterval(tm)
    }
    timers.clear()
}
