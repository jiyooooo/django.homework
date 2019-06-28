from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Blog, Comment
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import BlogPost #blogpost import해올것
# Create your views here.

def home(request):
    blogs = Blog.objects #페이지전체를 blog라는 객체로 받음
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page') #변수가page
    posts = paginator.get_page(page) #얻어온page가 뭔지 post로 넣어줌.
    return render(request,'home.html', {'blogs':blogs, 'posts':posts}) #알아낸 페이지를 넣은다음에 key랑 value로 리턴이 되게 넘겨줌

def detail(request, blog_id):
    blog_details = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'details':blog_details})

def new(request):
    return render(request, 'new.html')

@login_required
def create(request):
    if request.method == "POST":
        form = BlogPost(request.POST)#post방식으로 받기
        if form.is_valid():
            post = form.save(commit=False) #아직저장하지말기
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
    return render(request, 'new.html', {'form':form})


@login_required
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

#blog/views
@login_required
def comment_add(request, blog_id):
    if request.method == "POST":
        post = Blog.objects.get(pk=blog_id)

        comment = Comment()
        comment.user = request.user
        comment.body = request.POST['body']
        comment.post = post
        comment.save()
        return redirect('/blog/'+ str(blog_id) )

    else:
        return HttpResponse('잘못된 접근입니다')

@login_required
def comment_edit(request,comment_id):
    
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user: #접속유저=댓글유저
        if request.method == "POST":
            comment.body = request.POST['body']
            comment.save()
            return redirect('/blog/'+ str(comment.post.id)) #댓글에서 게시글로 가서 id를 달라는 뜻

        elif request.method =="GET":
            context = {
                'comment':comment
                }
            return render(request, 'comment_edit.html', context)


@login_required
def comment_delete(request,comment_id):
    
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user: 
        if request.method == "POST":
            post_id = comment.post.id
            comment.delete()
            return redirect('/blog/'+ str(post_id)) 
        return HttpResponse('잘못된 접근입니다')

def blogpost(request):
    if request.method == "POST":
        form = BlogPost(request.POST)#post방식으로 받기
        if form.is_vaild():
            post = form.save(commit=False) #아직저장하지말기
            post.pub_date = timezone.now() #지금시각넣어주기
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request, 'new.html', {'form':form})
