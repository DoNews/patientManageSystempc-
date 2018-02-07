window.onload = function() {
	//切换状态
	$('.kf_power li').click(function() {
		$(this).addClass("li_active").siblings().removeClass()
	});
	//分页
 
	layui.use(['laypage', 'layer'], function() {
		var laypage = layui.laypage,
			layer = layui.layer;

		//自定义样式
		//完整功能
		laypage.render({
			elem: 'pageNum',
			count: 100,
			layout: ['count', 'prev', 'page', 'next', 'limit', 'skip'],
			jump: function(obj) {
				console.log(obj)
			}
		});
		$('.pmTbaleBtn').click(function() {
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

		});
		
	});

}