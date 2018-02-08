window.onload = function() {
	//切换状态

	layui.use([ 'layer'], function() {
		var layer = layui.layer;

		//去管理
		$('.remindTableBtn,.remindTableBtn2').click(function() {
			var sid =$(this).attr("id");
			layer.open({
				type: 2,
				title: false,
				closeBtn: 1, //不显示关闭按钮
				shade: [0.4],
				area: ['800px', '550px'],
				offset: '40px',
				scrollbar: false, //禁止浏览器滚动
				anim: 2,
			content: ['/orderdetail?id='+sid, 'yes'],
				end: function() { //此处用于演示

				}
			});

		});
		
	});
}