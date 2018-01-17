from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
import markdown

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=70)
    author = models.CharField(max_length=16)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    excerpt = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)



