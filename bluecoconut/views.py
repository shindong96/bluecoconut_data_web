import os, sys
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib import messages
from django.views.generic import CreateView
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from table_view.models import Argo_User

#requset.user : 현재 로그인한 user 정보 불러오기

@login_required()
def post_main(request):
    return render(request, 'main.html', {})

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return render(request, 'main.html', {})
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        return render(request, 'login.html', {})

def user_logout(request):
    auth.logout(request)
    return redirect('user_login')

@csrf_exempt
def user_signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if request.POST['password'] != request.POST['password2']:
                messages.info(request, '비밀번호가 일치하지 않습니다.')
                return redirect('user_signup')
            user_info = form.save(commit=False)
            user = User.objects.create_user(username=request.POST['userID'], password=request.POST['password'], email=request.POST['email'])
            user_info.userID_id = user.id
            user_info.save()
            messages.info(request, '회원가입을 완료했습니다. 로그인 해주세요.')
            return redirect('user_login')
        else:
            print(form.errors)
            messages.info(request, '정보를 올바르게 입력해주세요.')
            return redirect('user_signup')
    else:
        form = RegisterForm()
        return render(request, 'signup.html',{'form': form})





# class UserCreateView(CreateView):
# @csrf_exempt
# def user_create(request):
#     print("@@@@@@@")
#     form = RegisterForm(request.POST)
#     if form.is_valid():
#         print('!!!!!!!!')
#         print(form['name'])
#         response = {'status': 1, 'message': '등록이 완료되었습니다.'}
#         return HttpResponse(json.dumps(response), content_type='application/json')
#     else:
#         print("?????")
#         print(form.errors)
#         response = {'status': 0, 'message': '저장이 실패하였습니다.'}
#         return HttpResponse(json.dumps(response), content_type='application/json')