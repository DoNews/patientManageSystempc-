/**
 * Created by wp on 2/5/2018.
 */
var userinfo = {}
var postData = {}
$(".img_boxUl").on('click','.x',function () {
    $(this).parent().remove();
    imgSrcList.remove($(this).attr("data"))
});
$(".img_boxUl").on('click','.p',function () {
        layer.photos({
        photos: '.img_boxUl'
        , anim: 5 //0-6的选择，指定弹出图片动画类型，默认随机（请注意，3.0之前的版本用shift参数）
    });

});
layui.use(['form', 'laydate', 'upload', 'layer'], function () {
    var form = layui.form,
        upload = layui.upload,
        laydate = layui.laydate,
        date=new Date();

    laydate.render({
        elem: '#yyDate',
        min:'date'
    });
    // layer.photos({
    //         photos: '.img_boxUl',
    //         area: ['700px','500px'],
    //         anim: 5,//0-6的选择，指定弹出图片动画类型，默认随机（请注意，3.0之前的版本用shift参数）,
    //         closeBtn: 1,
    //     full:true
    //
    // });
    laydate.render({
        elem: '#birthDay',
        max:'date'
    });
    laydate.render({
        elem: "#yyDateNext ",
        min:'date'
    });

    layer = layui.layer;
    var uploadInst = upload.render({
        elem: '#addupload'
        ,
        url: '/upload'
        ,
        done: function (res) {
            var url = res.imgurl
            //上传完毕回调
            imgSrcList.push(url)
            $("#addupload").before("<li class=\"img_boxLi\"><div data=\"" + url + "\"  style=\"  width: 20px;height:20px\" class=\"x\"></div><a href=\"" + url + "\" target='_blank'><img class=\"p\" layer-pid=\"图片id，可以不写\" 					layer-src=\"" + url + "\"  src=\"" + url + "\" /></a></li>");
        },
        error: function () {
            //请求异常回调
        }
    });

});

$("#sureAdd").click(function () {
    submitCreateData();
});

$(".action").click(function () {
    var val=$('#yyDateNext').val();
    var type = $(this).attr("type");
    var date=new Date(Date.parse(val));
    var now =new Date();
    if(type!=12)
    {
        if(type!=15){
                    if(val==""){
                        layer.msg('下次跟进回访时间不能为空', {
                          time: 5000, //2s后自动关闭
                             btn: ['去填写']
                         });
                         return false
                    }
                     else if(now>date){
                         layer.msg('下次跟进回访时间不能小于当前时间', {
                          time: 5000, //2s后自动关闭
                             btn: ['去填写']
                         });
                         return false
                  }
        }

    }
    if(type=3){
        $('.addBtn2').attr('disabled','true')
    }
    submitUpdateData(type);
});

function submitCreateData() {
    var surl = "/ordersubmit";
    initUserData();
    submit(surl)
}

function initUserData() {
    userinfo.name = $("#name").val();
    userinfo.birthday = $("#birthDay").val()
    userinfo.phone = $("#phone").val()
    userinfo.sex = $("#sex").val()
    userinfo.area = $("#area").val()
    userinfo.wantTime = $("#yyDate").val()
    userinfo.wanthospital = $("#hosp").val()
    userinfo.description = $(".info_text").val()
    userinfo.number=$("#number").val()
    postData["userinfo"] = JSON.stringify(userinfo);
    postData["photo"] = JSON.stringify(imgSrcList);
}

function initFolowData(stype) {
    var remark = $("#textarea").val();
    var nextcall = $("#yyDateNext").val();
    var now =Date.now()

    var folowdata = {}
    folowdata.remark = remark;
    folowdata.nextcalldate = nextcall;
    folowdata.status = stype
    userinfo.nextcalldate = nextcall;
    userinfo.number=$("#number").val()
    userinfo.oid = getParam("id");
    userinfo.status = stype;
    postData["folow"] = JSON.stringify(folowdata);
}

function submit(surl) {
var mask = parent.layer.load(1,{shade:[0.3, '#393D49']})
        $.ajax({
            url: surl,
            type: "POST",
            dataType: "json",
            data: postData,
            success: function (data) {
                // console.log(data)
                // window.parent.location.reload();
                parent.layer.close(mask);
                parent.layer.closeAll();
                parent.layer.msg('操作成功');
                parent.parent.isneedreload = true
            }
        })
}

function submitUpdateData(stype) {
    initFolowData(stype)
    initUserData()
    submit("/orderupdate")
}

Array.prototype.indexOf = function (val) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == val) return i;
    }
    return -1;
};
Array.prototype.remove = function (val) {
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};