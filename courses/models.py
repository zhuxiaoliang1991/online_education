from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from django.contrib.contenttypes.models import  ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200,verbose_name='专业名称')
    slug = models.SlugField(max_length=200,blank=True,unique=True,verbose_name='简短url')

    class Meta:
        db_table = 'subject'
        ordering = ['title']
        verbose_name = '专业'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Subject,self).save(*args,**kwargs)

class Course(models.Model):
    owner = models.ForeignKey(User,related_name='course_created',on_delete=models.CASCADE,verbose_name='主讲老师')
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE,verbose_name='所属专业')
    title = models.CharField(max_length=200,verbose_name='课程名称')
    slug = models.SlugField(max_length=200,blank=True,verbose_name='短url')
    overview = models.TextField(verbose_name='课程概括')
    created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        db_table = 'course'
        ordering = ['-created']
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course,self).save(*args,**kwargs)

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE,verbose_name='所属课程')
    title = models.CharField(max_length=200,verbose_name='章节标题')
    description = models.TextField(blank=True,verbose_name='章节概述')
    order = OrderField(for_fields=['course'],blank=True,verbose_name='序号')

    class Meta:
        ordering = ['order']
        db_table = 'module'
        verbose_name = '章节'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{}.{}'.format(self.order,self.title)

class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE,verbose_name='内容')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':('text','file','image','video')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    order = OrderField(blank=True,for_fields=['module'],verbose_name='序号')

    class Meta:
        ordering = ['order']
        db_table = 'content'
        verbose_name = '内容'
        verbose_name_plural = verbose_name


class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE,verbose_name='编写者')
    title = models.CharField(max_length=250,verbose_name='标题')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField(verbose_name='教学文本')
    class Meta:
        db_table = 'text'

class File(ItemBase):
    file = models.FileField(upload_to='files',verbose_name='教学文件')
    class Meta:
        db_table = 'file'

class Image(ItemBase):
    file = models.FileField(upload_to='images',verbose_name='教学图片')
    class Meta:
        db_table = 'image'

class Video(ItemBase):
    url = models.URLField(verbose_name='教学视频url')
    class Meta:
        db_table = 'video'
