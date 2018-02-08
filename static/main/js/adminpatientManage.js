window.onload = function() {
	//分页
	layui.use(['laypage', 'layer'], function() {
		var laypage = layui.laypage,
			layer = layui.layer;

		//自定义样式
		//完整功能
		laypage.render({
			elem: 'pageNum',
			count: $("#count").val(),
			layout: ['count', 'prev', 'page', 'next',  'skip'],
			limit:10,
			jump: function(obj,first) {
				 //obj包含了当前分页的所有参数，比如：
					console.log(obj.curr); //得到当前页，以便向服务端请求对应页的数据。
					console.log(obj.limit); //得到每页显示的条数
					if(!first)
					{
						$.ajax({
						url:"/api/apoint/service/",
						data:{"page":obj.curr},
						type:"GET",
						dataType:"json",
						success:function (data) {
						$("#count").val(data.all);
						$("#data").html(data.lister);

							$(".pmTbaleBtn").click(function () {
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
							})
							$(".newgd").click(function () {
								parent.layer.open({
												type: 2,
												title: false,
												closeBtn: 1, //不显示关闭按钮
												shade: [0.4],
												area: ['800px', '600px'],
												offset: '40px',
												scrollbar: false, //禁止浏览器滚动
												anim: 2,
												content: ['/addpation', 'yes'], //iframe的url，no代表不显示滚动条
												end: function() {}
											});
							});

						console.log(data)
                        }
					})
					}
			}
		});
	});

}