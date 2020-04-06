var ec_left1=echarts.init(document.getElementById('l1'),'dark');

var ec_left1_Option= {
    //title
    title: {
        text: "全国累计趋势",
        textStyle: {},
        left: 'left',
    },
    tooltip: {
        trigger: 'axis',
        //指示器
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#7171C6'
            }
        },
    },
    legend: {
        data: ['累计确诊', '现有疑似', '累计治愈', '累计死亡'],
        left: "right"
    },

    //图形位置
    grid: {
        left: '4%',
        right: '6%',
        bottom: '4%',
        top: 50,
        containLabel: true
    },
    xAxis: [{
        type: 'category',
        //X轴坐标点开始与结束位置都不在最边缘
        //boundaryGap：true
        data: []
    },],
    yAxis: [{
        type: 'value',
        //y轴字体
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function (value) {
                if (value >= 1000) {
                    value = value / 1000 + 'k';
                }
                return value;
            }
        },
        //y轴线设置显示
        axisLine: {
            show: true
        },
        //与X轴平行的线样式
        splitLine: {
            show: true,
            lineStyle: {
                color: '#17273B',
                width: 1,
                type: 'solid',
            }
        }
    }],
    series: [{
        name: "累计确诊",
        type: 'line',
        smooth: true,
        data: []
    }, {
        name: "现有疑似",
        type: 'line',
        smooth: true,
        data: []
    }, {
        name: "累计治愈",
        type: 'line',
        smooth: true,
        data: []
    }, {
        name: "累计死亡",
        type: 'line',
        smooth: true,
        data: []
    }]
};

ec_left1.setOption(ec_left1_Option);