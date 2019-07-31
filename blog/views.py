from django.shortcuts import render, get_object_or_404, redirect
from.models import Blog, Comment
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    blogs = Blog.objects.all().order_by("-id") #Blog의 객체를 다 가지고 오겠다.
    return render(request,'blog/home.html',{'blogs':blogs})
    #render 제공하다,넘겨주다 - 웹페이지(home.html)을 통해서 제공하겠다.

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog,pk=blog_id)

    user = request.user

    if blog_detail.likes.filter(id = user.id):
        message = "좋아요 취소"
    else: 
        message = "좋아요"

    return render(request, 'blog/detail.html', {'blog': blog_detail, 'message':message})

#c new
def new(request):
    return render(request, 'blog/new.html') #요청이 들어오면 render를 통해서 new.html을 뛰워주어라!

# c create
def create(request):
    blog = Blog() # blog라는 붕어빵 틀을 가지고 온것
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.user = get_object_or_404(User, pk=request.GET['user_id'])
    # 붕어빵 속 틀을 다 채웠다
    blog.save()

    return redirect('/blog/' + str(blog.id))

#u edit
def edit(request,blog_id):
    blog = get_object_or_404(Blog,pk=blog_id)
    return render(request, 'blog/edit.html',{'blog' : blog }) 
    
#u update
def update(request,blog_id):
    blog = get_object_or_404(Blog,pk=blog_id)
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    # 붕어빵 속 틀을 다 채웠다
    blog.save()

    return redirect('/blog/' + str(blog.id))

#d delete
def delete(request, blog_id):
    blog = get_object_or_404(Blog,pk=blog_id)
    blog.delete()

    return redirect('home')

def comment_create(request, blog_id):
    comment = Comment() #댓글을 저장하기 위해서 빈 Comment 객체를 하나 생성
    comment.body =request.GET['content'] #댓글의 내용을 받아옴 
    comment.blog = get_object_or_404(Blog,pk=blog_id) #해당 댓글을 어떤 blog 객체와 연결시켜 줄 것인지에 찾아온다.
    comment.save() #comment를 db에 저장.
    
    return redirect('/blog/' + str(blog_id))

def post_like(request, blog_id):
    user = request.user #로그인된 유저의 객체(정보)를 가져온다.
    blog =get_object_or_404(Blog, pk = blog_id) #좋아요 버튼을 누를 글을 가져온다.

    #이미 좋아요를 눌렀다면 좋아요를 취소, 아직 안눌렀으면 좋아요를 누른다.
    if blog.likes.filter(id =user.id):
        blog.likes.remove(user)
    else: #아직 좋아요를 누르지 않았다면
        blog.likes.add(user) #좋아요를 추가하여 준다.
    
    return redirect('/blog/' + str(blog_id)) # 좋아요 처리를 하고 detail 페이지로 간다.