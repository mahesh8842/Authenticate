from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
import random
import re
import http.client
# Create your views here.

def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')


def validate_email_address(email_address):
  
   return re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address)
#    r'^\+?1?\d{9,15}$
def validate_mobile(mobile):
    return re.search(r'^\+?1?\d{9,12}$',mobile)

def send_otp(mobile,otp):
    conn = http.client.HTTPSConnection("api.msgp1.com")
    authkey = settings.AUTH_KEY
    headers = { 'content-type': "application/json" }
    url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Hey! your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data,'---------------')
    return None

#     import http.client

# conn = http.client.HTTPSConnection("api.msg91.com")

# payload = "{\n  \"flow_id\": \"EnterflowID\",\n  \"sender\": \"EnterSenderID\",\n  \"recipients\": [\n    {\n      \"mobiles\": \"919XXXXXXXXX\",\n      \"VAR1\": \"VALUE 1\",\n      \"VAR2\": \"VALUE 2\"\n    },\n    {\n      \"mobiles\": \"9198XXXXXXX\",\n      \"VAR1\": \"VALUE 1\",\n      \"VAR3\": \"VALUE 3\"\n    }\n  ]\n}"

# headers = {
#     'authkey': "",
#     'content-type': "application/json"
#     }

# conn.request("POST", "/api/v5/flow/", payload, headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

# def return_register()

def register(request):
    message=''
    class_message=''
    if request.method=='POST':
        print(request.POST)
        email=request.POST.get('email','')
        name=request.POST.get('name','')
        mobile=request.POST.get('mobile','')
        # print(validate_email_address(email),name,mobile)
        if validate_email_address(email)==None:
            return render(request,'register.html',{'mail':'danger','class':'danger','message':'Please enter a valid email id!','name_p':name,'mobile_p':mobile})
        if validate_mobile(mobile)==None:
            return render(request,'register.html',{'mobile':'danger','class':'danger','message':'Please enter a valid mobile number!','mail_p':email,'name_p':name})
        check_user = Profile.objects.filter(mobile=mobile)

        if len(check_user)!=0:
            message = 'mobile number already exists!'
            class_message='danger'
        else:
            user_exist = User.objects.filter(first_name=request.user.first_name).first()
            print(user_exist)
            if user_exist:
                user = request.user
            else:
                user = User(email=email,first_name= name)
                user.save()
            otp = str(random.randint(100000,999999))
            profile=Profile(user=user,mobile=mobile,otp=otp)
            profile.save()
            send_otp(mobile,otp)

            # add otp and mobile to the session
            request.session['mobile']=mobile
            request.session['otp']=otp
            return redirect('otp')




    return render(request,'register.html',{'message':message,'class':class_message})


def otp(request):
    mobile=request.session['mobile']
    context={'mobile':mobile}

    return render(request,'otp.html',context)