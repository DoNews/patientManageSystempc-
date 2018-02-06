window.onload = function() {
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