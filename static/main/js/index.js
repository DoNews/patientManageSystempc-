$(function() {

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