from django import forms
from django.forms.models import inlineformset_factory
from .models import Course,Module


#使用内置的inlineformset_factory()方法构建了表单集ModelFormSet,内联表单工厂函数是在
#普通的表单集之上的一个抽象，这个函数允许我们动态的通过与Course模型关联的Module模型创建表单集
#fields:表示表单集中每个表单的字段
#extra:设置每次显示表单集时候的表单数量
#can_delete:该项如果设置为True,Django会在每个表单内包含一个布尔字段(被渲染成为一个checkbox类型的input元素）
#供用户选中需要删除的表单

ModuleFormset = inlineformset_factory(Course,Module,fields=['title','description'],extra=2,can_delete=True)

