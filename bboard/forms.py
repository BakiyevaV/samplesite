from django.forms import ModelForm

from .models import Bb,Comments
class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'feature')

class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('comment_creator', 'comment')
