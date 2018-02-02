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
	});

}