import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from admin.models import *

def mypage(request):
    return render(request, 'mypage/mypage.html', {})

def detail(request):
    if request.method == 'POST':
        id = request.POST['id']
        try:
            update = member_tbl.objects.get(id=request.user.id)
            if request.POST['action'] == '탈퇴':
                request.user.delete()
                member_tbl.objects.get(member_id=id).delete()
            elif request.POST['action'] == '저장':
                if request.POST['password1'] == request.POST['password2']:
                    password = request.POST['password2']
                    phone = request.POST['phone']
                    email = request.POST['email']
                    address = request.POST['address']
                    address_detail = request.POST['address_detail']

                    update = member_tbl.objects.get(id= request.POST['user_id'])
                    update.member_password = password
                    update.member_contact_number = phone
                    update.member_email = email
                    update.member_address = address
                    update.member_address_detail = address_detail
                    update.save()

                    users = User.objects.get(username=id)
                    users.set_password(password)
                    users.save()

                    user = authenticate(request, username=id, password=password)
                    login(request, user)

                    message = '성공적으로 저장되었습니다.'
                    return render(request, 'mypage/detail.html', {'User': update, 'message1':message})
                else:
                    message = '비밀번호를 잘못 입력하셨습니다. 다시 입력해주세요'
                    return render(request, 'mypage/detail.html', {'User': update, 'message': message})
            elif request.POST['action'] == '검색':
                return render(request, 'mypage/detail.html', {'User': update})
            elif request.POST['action'] == '찾기':
                return render(request, 'mypage/detail.html', {'User': update})
        except:
            password = request.POST['password']
            try:
                member = member_tbl.objects.get(member_id=id, member_password=password)
                return render(request, 'mypage/detail.html', {'User': member})
            except:
                return redirect("/honssa/my/detail")

    return render(request, 'mypage/check.html', {})

def order_list(request):
    user = member_tbl.objects.get(member_id = request.user)
    try:
        order_list = order_tbl.objects.filter(member_id = user)
        for i in order_list:
            i.order_date = i.order_date.strftime('%Y-%m-%d')
    except:
        order_list = None
    return render(request, 'mypage/order_list.html', {'orders': order_list})

def delivery_list(request):
    user = member_tbl.objects.get(member_id = request.user)
    order_list = order_tbl.objects.filter(member_id = user)
    for i in order_list:
        i.order_date = i.order_date.strftime('%Y-%m-%d')
    return render(request, 'mypage/delivery_list.html', {'orders': order_list})

def address_list(requset):
    return render(requset, 'mypage/address_list.html', {})
# Create your views here.
