from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView,DeleteView

from .models import Post,Like,Comment
from .forms import PostForm,CommentForm


class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"] # 新しい順
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        liked_posts = Like.objects.filter(
            user=self.request.user
        ).values_list("post_id", flat=True)

        context["liked_posts"] = liked_posts
        return context


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()

        return redirect("post_detail", pk=self.object.pk)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # いいねしたユーザーが、いいねした投稿にすでにいいねしているか探す
    # 存在しなければ作成、存在すれば削除
    # True→新しく作成、False→すでに存在している
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()  # 既にいいねしてたら解除

    return redirect("post_list")

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user  # 本人だけ削除可能