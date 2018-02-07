var nowMouth1 = echarts.init(document.getElementById('nowMouth1'));
		// 指定图表的配置项和数据
		var optionNow1 = {
			
			tooltip: {},
			
			xAxis: [{
				data: ["本月累计测评人数", "本月分配患者数", "本月总患者数"],
				axisLabel: {
					rotate:45, //刻度旋转45度角
					textStyle: {
						color: "red",
						fontSize:10
					}
				}
			}],
			yAxis: {},
			series: [{
					name: '销量',
					type: 'bar',
					barWidth: 15, //柱图宽度
					data: [5, 20, 36],
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
		nowMouth1.setOption(optionNow1);
		
		var nowMouth2 = echarts.init(document.getElementById('nowMouth2'));
		// 指定图表的配置项和数据
		var optionNow2 = {
			
			xAxis: [{
				data: ["本月累计测评人数", "本月分配患者数", "本月总患者数"],
				axisLabel: {
					rotate: 45, //刻度旋转45度角
					textStyle: {
						color: "red",
						fontSize: 16
					}
				}
			}],
			yAxis: {},
			series: [{
					name: '销量',
					type: 'bar',
					barWidth: 15, //柱图宽度
					data: [5, 20, 36],
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
		nowMouth2.setOption(optionNow2);
		
		//
		
		
		var nowMouth3 = echarts.init(document.getElementById('nowMouth3'));
		// 指定图表的配置项和数据
		var optionNow3 = {
			
			tooltip: {},
			
			xAxis: [{
				data: ["本月累计测评人数", "本月分配患者数", "本月总患者数"],
				axisLabel: {
					rotate: 45, //刻度旋转45度角
					textStyle: {
						color: "red",
						fontSize: 16
					}
				}
			}],
			yAxis: {},
			series: [{
				
					type: 'bar',
					barWidth: 15, //柱图宽度
					data: [5, 20, 36],
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
		nowMouth3.setOption(optionNow3);
		
		
		var nowMouth4 = echarts.init(document.getElementById('nowMouth4'));
		// 指定图表的配置项和数据
		var optionNow4 = {
			
			tooltip: {},
			
			xAxis: [{
				data: ["本月累计测评人数", "本月分配患者数", "本月总患者数"],
				axisLabel: {
					rotate: 45, //刻度旋转45度角
					textStyle: {
						color: "red",
						fontSize: 16
					}
				}
			}],
			yAxis: {},
			series: [{
					name: '销量',
					type: 'bar',
					barWidth: 15, //柱图宽度
					data: [5, 20, 36],
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
		nowMouth4.setOption(optionNow4);