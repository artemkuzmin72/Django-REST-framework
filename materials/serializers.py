from rest_framework import serializers
from materials.models import Course, Lesson
from .validators import LinkValidator
from user.models import Subscription
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson 
        fields = '__all__'
        validators = [LinkValidator(field='description')]

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  
    lessons_count = serializers.SerializerMethodField()    
    is_subscribed = serializers.SerializerMethodField()   

    class Meta:
        model = Course
        fields = '__all__' 
        validators = [LinkValidator(field='description')]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
    
    def get_is_subscribed(self, obj):
        """
        Проверяет, подписан ли текущий пользователь на курс.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=request.user, course=obj).exists()
