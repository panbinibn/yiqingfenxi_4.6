var ec_right2=echarts.init(document.getElementById('r2'),'dark');

var ec_right2_Option= {
    title: {
        text: '国外地区确诊TOP5',
        //subtext: '纯属虚构',
        textStyle: {
            color:'white'
        },
        left: 'left'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        top: 'top',
        left: 'right',
        data: ['累计确诊', '累计死亡']
    },
    grid: {

        left: '3%',
        right: '4%',
        bottom: '5%',
        containLabel: true
    },
    xAxis: {
        type: 'value'
    },
    yAxis: [{
        type: 'category',
        inverse:true,
        data: []
    }],

    series: [
        {
            name: '累计确诊',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: []
        },
        {
            name: '累计死亡',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: []
        },

    ]
};

ec_right2.setOption(ec_right2_Option);