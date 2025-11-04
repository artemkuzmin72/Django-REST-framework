from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video = models.FileField(upload_to='lesson_videos/')
    сourse = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
        
    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.title
    
class LessonQuantity(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name='Кол-во уроков')

    class Meta:
        verbose_name = "Quantity"
        verbose_name_plural = "Quantity"