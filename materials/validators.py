from rest_framework import serializers
import re

class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value:
            return attrs 
        allowed_domains = ['youtube.com']

        # Если это просто ссылка, то проверим напрямую
        if isinstance(value, str) and value.startswith('http'):
            if not any(domain in value for domain in allowed_domains):
                raise serializers.ValidationError({
                    self.field: "Разрешены только ссылки на YouTube (youtube.com или youtu.be)."
                })

        # Если это текст, то ищем в нём все ссылки
        urls = re.findall(r'https?://[^\s]+', value)
        for url in urls:
            if not any(domain in url for domain in allowed_domains):
                raise serializers.ValidationError({
                    self.field: f"В тексте найдена запрещённая ссылка: {url}. Разрешены только ссылки на YouTube."
                })

        return attrs