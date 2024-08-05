from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog, Category
from .forms import BlogForm
from users.models import CustomUser

def blog_page(request):
    categories = Category.objects.all()
    category_blogs = {category: Blog.objects.filter(category=category, is_draft=False).order_by('-created_at') for category in categories}
    form = BlogForm()
    return render(request, 'blog/blog_page.html', {'category_blogs': category_blogs, 'form': form})

@login_required
def create_blog(request):
    if not request.user.is_doctor:
        messages.warning(request, 'Only doctors can add blogs')
        return redirect('Blog_Page')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            if blog.is_draft:
                messages.success(request, 'Blog saved as draft')
            else:
                messages.success(request, 'Blog posted successfully')
            return redirect('Blog_Page')
        else:
            messages.error(request, 'Blog not posted. Please try again.')
            return redirect('Blog_Page')
    return redirect('Blog_Page')

    