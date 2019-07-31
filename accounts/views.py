from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def signup(request):
    if request.method == 'POST': #POST 방식으로 요청을 받았는지 확인하여주는 역할
        if request.POST['password1'] == request.POST['password2']: #비밀번호 input 값과 확인 값이 같은지에 대해서 확인을 하여준다.
            try: #오류가 나지 않으면 계속해서 try안에 있는 것을 실행 시켜 줌.
                user = User.objects.get(username=request.POST['username'])
                #회원가입할 때 같은 이름의 회원 불러오기, 없으면 에러
                return render(request, 'signup.html',{'error':'이미 사용하고 있는 이름입니다!'})
            except User.DoesNotExist : #try안에서 User,DoesNotExist 에러가 났을 경우 실행
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1']
                )
                auth.login(request, user) #접속 상태를 로그인 상태로 변경
                return redirect('/')
    return render(request, 'signup.html') #회원가입 페이지 보여주기


def login(request):
    if request.method == 'POST': # POST 요청을 받은 경우
        username = request.POST['username']
        password = request.POST['password']
        #로그인에서 받은정보를 가진 회원이 있는지 확인하기
        user = auth.authenticate(request, username=username, password=password)
        if user is not None: #User가 존재할 경우
            auth.login(request,user) #로그인 상태로 변경하여 주기
            return redirect('home')
        else:
            return render(request,'login.html',{'error':'아이디 혹은 비번을 확인해주세요!'})
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')