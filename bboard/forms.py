from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet
from django.core import validators
from django import forms
from .models import Bb,Comments
# class BbForm(BaseInlineFormSet):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric', 'feature')


class BbForm(ModelForm):
    title = forms.CharField(
        label='Название товара',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Слишком короткое название товара'})
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'feature')

    def clean_title(self):
        val = self.cleaned_data.get('title')
        if val == 'Прошлогодний снег':
            print('к продаже не допускается')
            raise ValidationError('к продаже не допускается')
        print('хрень какая-то')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data.get('content'):
            errors['content'] = ValidationError('Нет описания')
        if self.cleaned_data.get('price') < 0:
            errors['price'] = ValidationError('Что с ценой?')
        if errors:
            raise ValidationError(errors)
class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('comment_creator', 'comment')
