****
    作用:发送验证码
    请求方式:POST
    url:http://127.0.0.1:8000/api/apoint/scrfcode/
    字段:phone #手机号
    return JsonResutResponse({'ret': 0,'msg':'success' })

****
    作用:员工认证
    请求方式:POST
    url:
    字段:
        openid
        name
        email
        phone
        vercode # 验证码
     return JsonResutResponse({"ret": -1, "msg": u"你已经认证过"})
     return JsonResutResponse({"ret": 0,'msg':'success'})
     return JsonResutResponse({'ret':1,'msg':u'手机号或姓名不匹配'})


****
    作用:查询我的患者
    请求方式:GET
    Url:http://127.0.0.1:8000/api/apoint/mypatien/?openid=o_MHBjuPu3dDh2-1z5rPfmXNfsAQ
    字段：openid,
    "lister": [{
        "wantTime": "2018-01-31",
        "hospital": "上海医院",
        "sex": "男",
        "id": 1,
        "name": "患者姓名"
    }],
    返回：return JsonResutResponse({'ret':0,'msg':'success','lister':lister})

****
    作用:查看患者详情
    请求方式:GET
    Url:http://127.0.0.1:8000/api/apoint/patientsdetail/?id=1
    请求字段:id，#患者订单id
    "data": {
            "wanthospital": "上海医院",
            "phone": "18765489065",#电话
            "birthday": "2018-01-16", #出生日期
            "name": "患者姓名",
            "area": "上海",
            "photo": [],
            "description": "这病很好治 三天几号",
            "customer": [{
                "remark": "这个患者可以被治疗 很快", #客服的描述
                "name": "", #客服姓名
                "time": "2018-01-30 11:39" # 客服操作时间
            }],
            "wantTime": "2018-01-31", #预约时间
            "sex": "男",
            "id": "1",

        },
    返回:return JsonResutResponse({'ret':0,'msg':'success','data':data})

****
    作用:患者提交预约单
    请求方式：POST
    url:http://127.0.0.1:8000/api/apoint/ordersubmit/
    字段1：name,[{"key":"name","value":"这是新患者",}]
    字段2：openid,[{"key":"openid","value":"o_MHBjlLNNi2JzTQWiC-P223dbc0",}]
    字段3：birthday，[{"key":"birthday","value":"2017-08-20","description":"生日"}]
    字段4：sex，[{"key":"sex","value":"男","description":"性别"}]
    字段5：phone，[{"key":"phone","value":"16253478956","description":""}]
    字段6：area，[{"key":"area","value":"1","description":"省，给我省的id"}]
    字段7：wantTime，[{"key":"wantTime","value":"2018-02-10","description":"预约时间"}]
    字段8：hospital，[{"key":"hospital","value":"1","description":"医院的id"}]
    字段9：description，[{"key":"description","value":"这个天使之吻只有一毫米，但我就是不想要","description":"胎记描述"}]
    字段10：photo，[{"key":"photo","value":"[]","description":"图片地址"}]
    成功时：
        return JsonResutResponse({'ret':0,'msg':'success'})
    已有预约时：
        return JsonResutResponse({'ret':1,'msg':'已有预约正在进行中'})

****
    作用: 图片上传
    请求方式：POST
    url：http://127.0.0.1:8000/api/apoint/upload/
    return HttpResponse(simplejson.dumps({"result": 0, "imgurl": img_url}))

****
    作用: 查看所有省
    请求方式：get
    url：http://127.0.0.1:8000/api/apoint/province/
    "lister": [{
		"id": 1,
		"area": "上海"
	}],
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister})

****
    作用:查看所有医院
    请求方式:get
    url：http://127.0.0.1:8000/api/apoint/hospital/
    "lister": [{
		"id": 1,
		"hospits": "上海医院"
	}],
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister})

****
    作用:销售提交
    请求方式:POST
    url:http://127.0.0.1:8000/api/apoint/thememo/
    字段1：id，[{"key":"id","value":"1","description":"orderid"}]
    字段2：openid，[{"key":"openid","value":"o_MHBjuPu3dDh2-1z5rPfmXNfsAQ","description":"销售openid"}]
    字段3：describe，[{"key":"describe","value":"这个患者 可以治","description":"描述"}]
    字段4：types，[{"key":"types","value":"6","description":"状态"}]#已安排治疗6，预约延后治疗11，转院13，患者未到诊14，暂停跟进12
    return JsonResutResponse({'ret':0,'msg':'success'})