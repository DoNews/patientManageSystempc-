# coding:utf-8
__author__ = 'Dell'
from django import template

register = template.Library()


@register.filter(name='reduce_value')
def reduce_value(values):
    count = 0
    # 这里的values就是你使用该标签时传入的参数，在这个例子里面values就是render的时候传给模板的order_list的值
    # 所以这里可以根据你实际传入的值做处理
    for v in values:
        if v['key']:
            count += int(v['key'])
    return count