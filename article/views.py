from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from article.forms import ArticleForm, CommentForm
from article.models import Article, Comment
from blog_site.views import BaseView


class ArticleAddView(BaseView):
    template_name = 'article_add.html'

    def get(self, request, *args, **kwargs):
        form = ArticleForm
        return render(request, self.template_name, {'form': form})

    def post(self,request, *args, **kwargs):
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            messages.add_message(request, messages.SUCCESS, "Article has been added successfully")
        else:
            messages.add_message(request, messages.ERROR, "Form is not valid")
            return render(request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('articles'))

class ArticleListView(View):
    template_name = 'articles.html'

    def get(self, request, *args, **kwargs):
        context = {
            'articles': Article.objects.all().order_by('-updated_at'),
        }

        return render(request, self.template_name, context)


class ArticleDetailsView(View):
    template_name = 'article_details.html'

    def get(self,request, *args, **kwargs):
        article = Article.objects.get(id=kwargs.get('article_id'))
        comments = article.comments.filter(parent__isnull=True).order_by('-created_at')

        context = {
            'article': article,
            'comments': comments,
        }

        return render(request, self.template_name, context)



class CommentAddAPIView(APIView):

    def post(self, request, *args, **kwargs):
        article_id = request.data.get('article_id', None)
        parent_id = request.data.get('parent_id', None)

        form = CommentForm(request.data, author=request.user, article_id=article_id, parent_id=parent_id)

        if form.is_valid():
            data = form.cleaned_data
            comment = Comment.objects.create(**data)

            response_data = {
                'id': comment.id,
                'avatar': comment.author.info.image.url,
                'author': comment.author.full_name,
                'text': comment.text,
                'created_at': comment.created_datetime,
            }

            if parent_id:
                response_data['parent_id'] = parent_id

            return Response(response_data)

        return Response(HTTP_401_UNAUTHORIZED)


class CommentDeleteAPIView(APIView):

    def post(self, request, *args, **kwargs):
        comment_id = request.data.get('comment_id')

        try:
            Comment.objects.get(id=comment_id).delete()
            return Response(HTTP_202_ACCEPTED)

        except:
            return Response(HTTP_204_NO_CONTENT)


class CommentUpdateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        comment_id = request.data.get('comment_id', None)
        comment_text = request.data.get('text', None)

        print(comment_id, comment_text)

        if comment_id and comment_text:
            try:
                Comment.objects.filter(id=comment_id).update(text=comment_text)
                return Response(HTTP_202_ACCEPTED)

            except: pass

        return Response(HTTP_204_NO_CONTENT)
