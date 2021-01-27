from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("group", "text")

    def empty_text(self):
        text = self.cleaned_data["text"]
        if not text:
            raise ValidationError("Поле обязательно к заполнению")
        return text
