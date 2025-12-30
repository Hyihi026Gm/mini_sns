from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content", "image")
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "いま何してる？",
                    "maxlength": 300,
            }),
        }
    def clean_content(self):
        content = self.cleaned_data["content"]

        if content and len(content) > 300:
            raise forms.ValidationError("300文字以内で入力してください")
        return content

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "コメントを書く..."
                }
            )
        }