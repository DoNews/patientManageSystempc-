window.onload = function () {
    //分页
    layui.use(['laypage', 'layer'], function () {
        var laypage = layui.laypage,
            layer = layui.layer;

        //自定义样式
        //完整功能
        laypage.render({
            elem: 'pageNum',
            count: $("#count").val(),
            layout: ['count', 'prev', 'page', 'next', 'skip'],
            limit: 10,
            jump: function (obj, first) {
                //obj包含了当前分页的所有参数，比如：
                // console.log(obj.curr); //得到当前页，以便向服务端请求对应页的数据。
                // console.log(obj.limit); //得到每页显示的条数
                if (!first) {
                    reloadData(obj.curr)
                }

            }
        });

    });

}

function reloadData(page) {
    $.ajax({
        url: "/api/apoint/orderall/",
        data: {"page": page},
        type: "GET",
        dataType: "json",
        success: function (data) {
            // console.log(data)
            $("#data").html(data.data);
        }
    })
}