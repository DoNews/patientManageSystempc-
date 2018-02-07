window.onload = function() {
	//切换状态
	$('.kf_power li').click(function() {
		$(this).addClass("li_active").siblings().removeClass()
	})

	//	患者认领弹框	
	$('.hzrl_list_btn').click(function() {

		layer.open({
			type: 2,
			title: false,
			closeBtn: 1, 
			shade: [0.4],
			area: ['800px', '550px'],
			offset: '40px', 
			scrollbar: false,
			anim: 2,
			content: ['./hzrlpop.html', 'yes'],
			end: function() { 

			}
		});
	})
	

}