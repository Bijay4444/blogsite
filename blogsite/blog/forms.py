from django import forms
from .models import Post, Comment, Interactions

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']