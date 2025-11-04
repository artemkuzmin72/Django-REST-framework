from rest_framework import serializers
from materials.models import Course, Lesson, LessonQuantity


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson 
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class SerializerMethodField(serializers.ModelSerializer):
    class Meta:
        model = LessonQuantity
        fields = '__all__'
