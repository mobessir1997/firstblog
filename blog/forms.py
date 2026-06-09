from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    
    tag_input = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Enter post tag'}))
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tag_input']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder':'আপনার মন্তব্য লিখুন..'})
        }