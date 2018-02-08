/**
 * Created by wp on 2/1/2018.
 */

$(".require_allInfo").click(function () {

    var index = parent.layer.getFrameIndex(window.name); //获取窗口索引
    $.ajax({
    url:"/renlingAction",
    type:"POST",
    dataType:"json",
    data:{"sid":getParam("id")},
    success:function (data) {
        //关闭iframe

        if(data.result==1)
        {
             parent.layer.msg('认领成功');
             parent.isrenling=true;
             parent.layer.close(index);

        }
       else
        {
             parent.layer.msg("失败："+data.msg);
            parent.layer.close(index);
        }

    }
})
});
