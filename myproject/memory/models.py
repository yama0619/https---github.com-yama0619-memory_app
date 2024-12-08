from django.db import models
import datetime

class Memory(models.Model):
    title = models.CharField(max_length=200)  # タイトル
    description = models.TextField()  # 文章
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)  # 写真（画像）保存用
    video = models.FileField(upload_to='videos/', null=True, blank=True)  # 動画保存用（オプション）
    created_at = models.DateField()  # 日付のみ
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title
