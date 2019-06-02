from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error':'username or password is incorrect.'})
    else:
         return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST': #post일경우에if문 아니면 회원가입창으로
        if request.POST['password1'] == request.POST['password2']: #비밀번호가 같은지
            user = User.objects.create_user( #필요한객체:name,pw
                    request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return redirect('/')
    return render(request, 'accounts/signup.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    return render(request, 'accounts/signup.html')