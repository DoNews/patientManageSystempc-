 $(function(){
 //切换状态
	$('.kf_power li').click(function() {
		$(this).addClass("li_active").siblings().removeClass()
	});

	//echart图标
	var myChart1 = echarts.init(document.getElementById('chart1'));
	// 指定图表的配置项和数据
        var option1 = {
            title: {
                text: 'ECharts 入门示例'
            },
            tooltip: {},
            legend: {
                data:['销量']
            },
            xAxis:[
            {
                data: ["衬衫","羊毛衫","雪纺衫","裤子"]
                ,
            axisLabel:{
              rotate:45, //刻度旋转45度角
              textStyle:{
                 color:"red",
                 fontSize:16
            }
            }}
            ] ,
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                barWidth :15,//柱图宽度
                data: [5, 20, 36, 10],
                itemStyle: {   
                //通常情况下：
                normal:{  
                    color: function (params){
                        var colorList = ['rgb(87,126,250)','rgb(110,217,181)','rgb(248,134,94)','rgb(175,216,255)'];
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
        myChart1.setOption(option1);
        
        
        var myChart2 = echarts.init(document.getElementById('chart2'));
	// 指定图表的配置项和数据
        var option2 = {
            title: {
                text: 'ECharts 入门示例'
            },
            tooltip: {},
            legend: {
                data:['销量']
            },
            xAxis:[
            {
                data: ["衬衫","羊毛衫","雪纺衫","裤子"]
                ,
            axisLabel:{
              rotate:45, //刻度旋转45度角
              textStyle:{
                 color:"red",
                 fontSize:16
            }
            }}
            ] ,
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                barWidth :15,//柱图宽度
                data: [5, 20, 36, 10],
                itemStyle: {   
                //通常情况下：
                normal:{  
                    color: function (params){
                        var colorList = ['rgb(87,126,250)','rgb(110,217,181)','rgb(248,134,94)','rgb(175,216,255)'];
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
			scrollbar: false,//禁止浏览器滚动
			anim: 2,
			content: ['./hzrlpop.html', 'yes'], //iframe的url，no代表不显示滚动条
			end: function() { //此处用于演示
//				layer.open({
//					type: 2,
//					title: '很多时候，我们想最大化看，比如像这个页面。',
//					shadeClose: true,
//					shade: false,
//					maxmin: true, //开启最大化最小化按钮
//					area: ['893px', '600px'],
//					content: '//fly.layui.com/'
//				});
			}
		});
	})
 })
 
 
