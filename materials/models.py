from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=60, verbose_name="название")
    desc = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to='previews', verbose_name="превью", **NULLABLE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="автор", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=60, verbose_name="название")
    desc = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to='previews', verbose_name="превью", **NULLABLE)
    url = models.URLField(verbose_name="ссылка", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="автор", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
