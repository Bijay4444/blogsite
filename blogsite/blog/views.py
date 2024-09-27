
from django.shortcuts import render, redirect, get_object_or_404
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from .models import Post, Comment, Interactions
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from .forms import CommentForm, EmailPostForm
from django.core.paginator import Paginator
from django.core.mail import send_mail


class PostListView(OwnerListView):
    model = Post
    template_name = "blog/post_list.html"

    def get(self, request):
        post_list = Post.objects.all()
        comment_list = Comment.objects.all()
        paginator = Paginator(post_list, 3)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.get_page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
            
        ctx = {'post_list': post_list,
               'comment_list': comment_list, 'posts': posts}
        return render(request, self.template_name, ctx)


class PostDetailView(OwnerDetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get(self, request, year, month, day, slug):
        post = get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=slug,
        )

        comments = Comment.objects.filter(post=post).order_by('-created_at')
        comment_form = CommentForm()
        ctx = {'post': post, 'comments': comments,
               'comment_form': comment_form}
        return render(request, self.template_name, ctx)


class PostCreateView(OwnerCreateView):
    model = Post
    fields = ['title', 'content', 'tags', 'picture']
    success_url = reverse_lazy('blogs:all')


class PostUpdateView(OwnerUpdateView):
    model = Post
    fields = ['title', 'content', 'tags', 'picture']
    success_url = reverse_lazy('blogs:all')


class PostDeleteView(OwnerDeleteView):
    model = Post
    success_url = reverse_lazy('blogs:all')
    
class PostShareView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        sent = False
        if request.method == 'POST':
            form = EmailPostForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                post_url = request.build_absolute_uri(post.get_absolute_url())
                subject = (f"{cd['name']} ({cd['email']})" 
                           f"recommends you read {post.title}")
                message = (f"Read {post.title} at {post_url}\n\n"
                           f"{cd['name']}\'s comments: {cd['comments']}")
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=[cd['to']]
                )
                sent = True
        else:
            form = EmailPostForm()
            
        return render(request, 'blog/post_share.html', {'post': post, 
                                                        'form': form, 
                                                        'sent': sent}
                      )


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        comment = Comment(
            comment=request.POST['comment'], owner=request.user, post=post)
        comment.save()
        messages.success(request, 'Comment added successfully!')
        return redirect(reverse('blogs:post_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "blog/comment_delete.html"

    def get_success_url(self):
        post = self.object.post
        messages.success(self.request, 'Comment deleted successfully!')
        return reverse('blogs:post_detail', args=[post.id])
