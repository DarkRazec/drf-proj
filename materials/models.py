from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Lesson(models.Model):
    name = models.CharField(max_length=60, verbose_name="название")
    desc = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to='previews', verbose_name="превью", **NULLABLE)
    url = models.URLField(verbose_name="ссылка", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Course(models.Model):
    name = models.CharField(max_length=60, verbose_name="название")
    desc = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to='previews', verbose_name="превью", **NULLABLE)
    lessons = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Уроки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
