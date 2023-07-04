from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from  .forms import registerForm,loginForm, PasswordChangingForm
from  django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.views import PasswordChangeView
from .models import CreateUserForm
from  django.contrib import messages


def register(request):
    rF = CreateUserForm()
    if request.method == "POST":
        rF = CreateUserForm(request.POST)
        if rF.is_valid():
            rF.save()
            return redirect('userMember:loginUser')
    return render(request, 'userMember/register.html', {'rF': rF})

# class loginUser(View):
#     def get(self,request):
#         lU = loginForm
#         return render(request, 'userMember/login.html',{'lU':lU})
#     def post(self,request):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # Redirect to a success page.
#             return render(request,'userMember/private.html')
#         else:
#             # Return an 'invalid login' error message.
#            return  HttpResponse('fail')
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('realcam:index')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('realcam:index')

        else: messages.error(request,'your username or password is not correct')
    return render(request,'userMember/login.html')

@login_required(login_url="/login/")
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password1']

        if not user.check_password(password):
            messages.error(request, 'Incorrect current password.')
            return redirect('userMember:edit_profile')

        # Cập nhật thông tin người dùng
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()


        return redirect('userMember:edit_profile')  # Đổi 'profile' thành tên view hiển thị thông tin người dùng

    return render(request, 'userMember/edit_profile.html', {'user': user})

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('userMember:change_success')
def password_success(request):
    messages.success(request,'You have been updated successful')
    return  render(request,'userMember/change_password.html')

def logoutUser(request):
    logout(request)
    # return render(request, 'polls/base.html')
    return redirect('polls:home')

#
# @login_required(login_url="/login/")
# def privateWeb(request):
#     return render(request, 'realcam/video.html')