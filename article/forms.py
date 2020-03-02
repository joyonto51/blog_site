from django import forms
from django_summernote.widgets import SummernoteWidget
from rest_framework.exceptions import ValidationError

from article.models import Article, Category, Comment


class ArticleForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ArticleForm, self).__init__(*args, **kwargs)  # populates the post
    #     self.fields['category'].queryset = Category.objects.all()

    class Meta:
        model = Article
        fields = ['category','image', 'title', 'about', 'content']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(),
        }


class CommentForm(forms.Form):
    text = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.article_id = kwargs.pop('article_id')
        self.parent_id = kwargs.pop('parent_id', None)

        super(CommentForm, self).__init__(*args,**kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        if self.author and self.article_id:
            cleaned_data['author'] = self.author
            cleaned_data['article'] = Article.objects.get(id=self.article_id)
        else:
            raise ValidationError("form is not valid")

        if self.parent_id:
            cleaned_data['parent'] = Comment.objects.get(id=self.parent_id)

        return cleaned_data
