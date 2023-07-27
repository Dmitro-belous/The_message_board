from django import forms
from django.core.exceptions import ValidationError

from .models import Response, Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['categoryType', 'head', 'body', 'image', 'file']

    def clean(self):
        cleaned_data = super().clean()
        head = cleaned_data.get('head')
        body = cleaned_data.get('body')
        if head == body:
            raise ValidationError(
                'Основной текст не должен быть идентичен заголовку'
            )

        return cleaned_data


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
