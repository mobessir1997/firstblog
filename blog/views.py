from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    search_query = request.GET.get('q', '').strip()
    if search_query:
        posts = posts.filter(
        Q(title__icontains=search_query) |
        Q(content__icontains=search_query)
        )

    return render(request, 'blog/home.html', {'posts':posts, 'search_query':search_query})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment.all().order_by('-create_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments, 'form':form})
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            tag_data = str(form.cleaned_data.get('tag_input',''))
            if tag_data and not tag_data.startswith('<built-in'):
                tag_list = [t.strip().lower() for t in tag_data.split(',') if t.strip()]
                for tag_name in tag_list:
                    tag_obj = Tag.objects.filter(name=tag_name).first()
                    if not tag_obj:
                        tag_obj = Tag.objects.create(name=tag_name)
                        print(tag_data)
                    post.tags.add(tag_obj)
                    
        return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'blog/post-form.html', {'form':form})
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("আপনি এই পোস্টটি এডিট করার অনুমতি পাননি।")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)

            post.tags.clear()
            tag_data = str(form.cleaned_data.get('tag_input',''))
            if tag_data and not tag_data.startswith('<built-in method'):
                tag_list = [t.strip().lower() for t in tag_data.split(',') if t.strip()]
                for tag_name in tag_list:
                    tag_obj = Tag.objects.filter(name=tag_name).first()
                    if not tag_obj:
                        tag_obj = Tag.objects.create(name=tag_name)
                    post.tags.add(tag_obj)
                    print(tag_data)
        return redirect('post-detail', pk=post.pk)
    else:
        current_tags = ",".join([tag.name for tag in post.tags.all() if not tag.name.startswith('<built-in')])
        form = PostForm(instance=post, initial={'tag_input':current_tags})
    return render(request, 'blog/post-form.html', {'form':form})
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission")
    if request.method == 'POST':
        post.delete()
        return redirect('blog-home')
    return render(request, 'blog/post-delete.html', {'post':post})

