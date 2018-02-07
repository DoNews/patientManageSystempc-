$(function() {

	$('#searchBtn').click(function() {
		layer.open({
			type: 2,
			title: false,
			closeBtn: 1, //不显示关闭按钮
			shade: [0.4],
			area: ['700px', '580px'],
			offset: '40px',
			scrollbar: false, //禁止浏览器滚动
			anim: 2,
			content: ['/api/apoint/search/?keyword='+$("#serch").val(), 'yes'], //iframe的url，no代表不显示滚动条 #26
			end: function() {}
		});
	})
})