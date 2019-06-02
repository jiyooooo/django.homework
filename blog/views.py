from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    blogs = Blog.objects #페이지전체를 blog라는 객체로 받음
    blog_list = Blog.objects.all()
    paginator=Paginator(blog_list, 3)
    page = request.GET.get('page') #변수가page
    posts = paginator.get_page(page) #얻어온page가 뭔지 post로 넣어줌.
    return render(request,'home.html', {'blogs':blogs, 'posts':posts}) #알아낸 페이지를 넣은다음에 key랑 value로 리턴이 되게 넘겨줌

def detail(request, blog_id):
    blog_details = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'details':blog_details})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/' +str(blog.id))

def edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        blog.title = request.POST['title']
        blog.body = request.POST['body']
        blog.pub_date = timezone.datetime.now()
        blog.save()
        return redirect('/blog/' +str(blog.id))
    return render(request, 'edit.html', {'blog':blog})

def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('/')

