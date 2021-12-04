$(document).on("dragstart", ".dragable-img", function(e) {
    chartid = e.target.getAttribute('chartid')
    dragsrc = 'render'
})

$(document).on("dragover", ".chartdiv", function(e) {
    e.preventDefault();
})

$(document).on("drop", ".chartdiv", function(e) {
    e.preventDefault()
    if (dragsrc == 'render') {
        vm.canPublish = false
        vm.tempChart = []
        vm.tempChart.push({chartid: chartid, intro: ''})
        makeChart(this.getAttribute('id'), chartid)
        vm.canPublish = true
    }
    dragsrc = ''
})

$(document).on("drop", "body", function(e) {
    dragsrc = ''
})