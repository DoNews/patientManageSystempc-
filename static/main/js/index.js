$(function() {
	//切换状态
	$('.kf_power li').click(function() {
		$(this).addClass("li_active").siblings().removeClass()
	});

	//echart图标
	var myChart1 = echarts.init(document.getElementById('chart1'));
	// 指定图表的配置项和数据
	var option1 = {
		title: {
			text: '本月数据'
		},
		tooltip: {
			enterable: true,
			trigger: 'axis',
			axisPointer: { // 坐标轴指示器，坐标轴触发有效
				type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
			},
		},
		xAxis: [{
			data: ["衬衫", "羊毛衫", "雪纺衫", "裤子"],
			axisLabel: {
				rotate: 45, //刻度旋转45度角
				textStyle: {
					color: "red",
					fontSize: 13
				}
			}
		}],
//		grid: { // 控制图的大小，调整下面这些值就可以，
//			x: 40,
//			x2: 100,
//			y2: 50, // y2可以控制 X轴跟Zoom控件之间的间隔，避免以为倾斜后造成 label重叠到zoom上
//		},
		yAxis: {},
		series: [{
				name: '销量',
				type: 'bar',
				barWidth: 15, //柱图宽度
				data: [5, 20, 36, 53],
				itemStyle: {
					//通常情况下：
					normal: {
						color: function(params) {
							var colorList = ['rgb(87,126,250)', 'rgb(110,217,181)', 'rgb(248,134,94)', 'rgb(175,216,255)'];
							return colorList[params.dataIndex];
						}
					}
				},
			}

		]
	};
	myChart1.setOption(option1);

	var myChart2 = echarts.init(document.getElementById('chart2'));
	// 指定图表的配置项和数据
	var option2 = {
		title: {
			text: '数据组展示'
		},
		tooltip: {},
		legend: {
			data: ['销量']
		},
		xAxis: [{
			data: ["衬衫", "羊毛衫", "雪纺衫", "裤子"],
			axisLabel: {
				rotate: 90, //刻度旋转45度角
				textStyle: {
					color: "red",
					fontSize: 16
				}
			}
		}],
//		grid: { // 控制图的大小，调整下面这些值就可以，
//			x: 40,
//			x2: 100,
//			y2: 50, // y2可以控制 X轴跟Zoom控件之间的间隔，避免以为倾斜后造成 label重叠到zoom上
//		},
		yAxis: {},
		series: [{
				name: '销量',
				type: 'bar',
				barWidth: 15, //柱图宽度
				data: [5, 20, 36, 10],
				itemStyle: {
					//通常情况下：
					normal: {
						color: function(params) {
							var colorList = ['rgb(87,126,250)', 'rgb(110,217,181)', 'rgb(248,134,94)', 'rgb(175,216,255)'];
							return colorList[params.dataIndex];
						}
					},
					//鼠标悬停时：
					emphasis: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.5)'
					}
				},
			}

		]
	};
	myChart2.setOption(option2);

	//	患者认领弹框	
	$('.hzrl_list_btn').click(function() {

		layer.open({
			type: 2,
			title: false,
			closeBtn: 1, //不显示关闭按钮
			shade: [0.4],
			area: ['800px', '550px'],
			offset: '40px',
			scrollbar: false, //禁止浏览器滚动
			anim: 2,
			content: ['./hzrlpop.html', 'yes'], //iframe的url，no代表不显示滚动条
			end: function() { //此处用于演示
					
			}
		});
	})

	$('.jrrw_list_btn').click(function() {

		layer.open({
			type: 2,
			title: false,
			closeBtn: 1, //不显示关闭按钮
			shade: [0.4],
			area: ['800px', '550px'],
			offset: '40px',
			scrollbar: false, //禁止浏览器滚动
			anim: 2,
			content: ['./addPatient.html', 'yes'], //iframe的url，no代表不显示滚动条
			end: function() { //此处用于演示

			}
		});

	})

	$('.xttx_list_btn').click(function() {

		layer.open({
			type: 2,
			title: false,
			closeBtn: 1, //不显示关闭按钮
			shade: [0.4],
			area: ['800px', '550px'],
			offset: '40px',
			scrollbar: false, //禁止浏览器滚动
			anim: 2,
			content: ['./addPatient.html', 'yes'], //iframe的url，no代表不显示滚动条
			end: function() { //此处用于演示

			}
		});
	})

})