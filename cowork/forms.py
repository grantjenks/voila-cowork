from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document'].widget = forms.HiddenInput()
        self.fields['topic'].widget = forms.HiddenInput()
        self.fields['author'].widget = forms.HiddenInput()

    class Meta:
        model = Comment
        fields = ['document', 'topic', 'author', 'message']
