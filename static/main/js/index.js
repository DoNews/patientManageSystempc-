$(function() {
	//切换状态
	$('.kf_power li').click(function() {
		$(this).addClass("li_active").siblings().removeClass()
	});
	//echart图标
	var myChart1 = echarts.init(document.getElementById('chart1'));
	// 指定图表的配置项和数据
	var chart1 = {

		tooltip: {
			enterable: true,
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			},
		},
		xAxis: [{
			data: ["本月累计跟进人数", "本月分配患者数", "本月认领患者数"],
			axisLabel: {
				rotate: 45,
				textStyle: {
					color: "red",
					fontSize: 13
				}
			}
		}],

		yAxis: {

		},
		series: [{
				name: '销量',
				type: 'bar',
				barWidth: 15,
				data: [5, 20, 36],
				itemStyle: {
					normal: {
						color: function(params) {
							var colorList = ['rgb(110,217,181)', 'rgb(248,134,94)', 'rgb(175,216,255)'];
							return colorList[params.dataIndex];
						}
					}
				},
			}

		]

	};
	myChart1.setOption(chart1);

	var myChart2 = echarts.init(document.getElementById('chart2'));
	var chart2 = {
		title: {
			text: '本月数据'
		},
		tooltip: {
			enterable: true,
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			},
		},
		xAxis: [{
			data: ["安排治疗", "预约转院治疗", "转院"],
			axisLabel: {
				rotate: 45,
				textStyle: {
					color: "red",
					fontSize: 13
				}
			}
		}],

		yAxis: {

		},
		series: [{
				name: '销量',
				type: 'bar',
				barWidth: 15,
				data: [5, 20, 36],
				itemStyle: {
					normal: {
						color: function(params) {
							var colorList = ['rgb(87,126,250)', 'rgb(110,217,181)', 'rgb(248,134,94)'];
							return colorList[params.dataIndex];
						}
					}
				},
			}

		]
	};
	myChart2.setOption(chart2);
	//	患者认领弹框	
	layui.use(['layer'], function() {
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
		});
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
//	点击查看更多跳转
	$(".chart2_btn").click(function(){
		window.location.href="formManage.html"
	})
})