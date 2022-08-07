from django.shortcuts import redirect,render
from supershop import definitions
from django.db import connection,IntegrityError
from django.http import JsonResponse
from asyncio.windows_events import NULL
from django.contrib import messages
from datetime import datetime
import hashlib

# Create your views here.

def is_username_unique(username):
    cursor = connection.cursor()
    query = """SELECT USERNAME 
            FROM USERS WHERE USERNAME=%s"""
    cursor.execute(query, [username])
    result = cursor.fetchone()
    cursor.close()

    if result is not None:
        return False
    
    return True

def IsSignUpInputsValid(request, firstname, lastname, phonenumber, email, username):
    if username==NULL or username=="":
        messages.error(request,'Please input your username!!')
        return False
    elif email==NULL or email=="":
        messages.error(request,'Please input your email!!')
        return False
    elif firstname==NULL or firstname=="":
        messages.error(request,'Please input your first name!!')
        return False
    elif lastname==NULL or lastname=="":
        messages.error(request,'Please input your last name!!')
        return False
    elif phonenumber==NULL or phonenumber=="":
        messages.error(request,'Please give your phone number!!')
        return False

def signup(request):
    data = {
        'firstname': None,
        'lastname' : None,
        'username' : None,
        'email' : None,
        'phone' : None,
        'bankacc' : None,
        'creditcard' : None,
    }

    if request.method == 'GET':
        return render(request, "accounts/signup.html", data)

    elif request.method == 'POST':
        firstname = request.POST.get('firstname'),
        lastname = request.POST.get('lastname'),
        username = request.POST.get('username'),
        email = request.POST.get('email'),
        phone = request.POST.get('phonenumber'),
        data.update({
            'firstname': firstname[0],
            'lastname': lastname[0],
            'username': username[0],
            'email': email[0],
            'phone': phone[0],
            'bankacc': request.POST.get('bankaccount'),
            'creditcard': request.POST.get('creditcard'),
        })
        
        if IsSignUpInputsValid(request, firstname, lastname, phone, email, username) == False:
            return render(request, "accounts/signup.html", data)
        
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirmpassword')

        if password1 != password2:
            messages.error(request, "Passwords did not match")
            return render(request, "accounts/signup.html", data)

        if is_username_unique(data['username'])== False:
            messages.error(request, 'Username already exists')
            data.update({'username' : None})
            return render(request, "accounts/signup.html", data)
        else:
            dateFormat = '%d-%b-%Y'
            joiningDate= datetime.strftime(datetime.now(), dateFormat)
            data.update({'joindate': joiningDate})
            try:
                hashed_password = hashlib.sha256(password1.encode()).hexdigest()
                cursor = connection.cursor()
                query = """INSERT INTO USERS(USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, PASSWORD, BANK_ACC_NO, CREDIT_CARD_NO, JOIN_DATE) 
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, STR_TO_DATE(%s, \'%d-%b-%Y\'))"""
                cursor.execute( query,
                                [data['username'], data['firstname'], data['lastname'], data['email'], 
                                data['phone'], hashed_password, data['bankacc'], data['creditcard'], data['joindate']])
                request.session['username'] = data['username']
                cursor.close()
            except IntegrityError:
                messages.error(request, 'This email already has an account')
                data.update({'email' : None})
                return render(request, "accounts/signup.html", data)

            if request.GET.get('next') is None:
                return redirect('home')
            else:
                return redirect(request.GET['next'])

def signin(request):
    if request.method == 'GET':
        return render(request, "accounts/signin.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor = connection.cursor()
        query = """SELECT USERNAME, PROFILE_PIC
                FROM USERS 
                WHERE USERNAME=%s AND PASSWORD=%s"""
        cursor.execute(query, [username, hashed_password])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            messages.error(request,"Invalid login credentials!")
            return render(request, 'accounts/signin.html')
        else:
            request.session['username'] = username
            request.session['profile_pic'] = result[1]
            
            if request.GET.get('next') is None:
                return redirect('home')
            else:
                return redirect(request.GET.get('next'))
            
def logout(request):
    request.session.flush()
    return redirect('home')

def profile(request):
    data = {
        'username': '',
        'firstname': '',
        'lastname': '',
        'email': '',
        'phone': '',
        'bankacc': '',
        'creditcard': ''
    }

    if(request.session.has_key('username')):
        cursor = connection.cursor()
        query = """SELECT *
                    FROM USERS
                    WHERE USERNAME=%s"""

        cursor.execute(query, [request.session['username']])
        result = definitions.dictfetchone(cursor)
        user_id = result['USER_ID']
        cursor.close()

        data.update({
            'username': result['USERNAME'],
            'firstname': result['FIRST_NAME'],
            'lastname': result['LAST_NAME'],
            'email': result['EMAIL'],
            'phone': result['PHONE_NO'],
            'bankacc': result['BANK_ACC_NO'],
            'creditcard': result['CREDIT_CARD_NO'],
            'profile_pic': result['PROFILE_PIC']
        })

        if request.method == 'GET':
            return render(request, 'accounts/profile.html', data)
        elif request.method == 'POST':
            data.update({
                'firstname': request.POST.get('firstname'),
                'lastname': request.POST.get('lastname'),
                'phone': request.POST.get('phonenumber'),
                'bankacc': request.POST.get('bankaccount'),
                'creditcard': request.POST.get('creditcard')
            })

            if data['username'] != request.POST.get('username') and is_username_unique(request.POST.get('username')) is False:
                messages.error(
                    request, 'Can not change to new username because the new username already exists')
                return render(request, "accounts/profile.html", data)
            elif data['username'] != request.POST.get('username'):
                cursor = connection.cursor()
                query = """UPDATE USERS
                        SET USERNAME = %s
                        WHERE USERNAME = %s"""
                cursor.execute(
                    query, [request.POST.get('username'), data['username']])
                
                
                messages.success(request, "Username updated!")
                data.update({
                    'username': request.POST.get('username')
                })
                request.session.update({
                    'username': data['username']
                })

            cursor = connection.cursor()
            query = """UPDATE USERS
                    SET FIRST_NAME = %s, 
                    LAST_NAME = %s,
                    PHONE_NO = %s,
                    BANK_ACC_NO = %s,
                    CREDIT_CARD_NO = %s
                    WHERE USERNAME = %s"""
            cursor.execute(query, [data['firstname'], data['lastname'], 
                data['phone'], data['bankacc'], data['creditcard'], data['username']])
            
            # if request.FILES.get('profilePic',False):
            #     folder = MEDIA_ROOT + '/Users/' + str(request.session['username'])
            #     upload1 = request.FILES['profilePic']
            #     fss = FileSystemStorage(location=folder)
            #     file = fss.save(upload1.name, upload1)
            #     photoPath = '/media/Users/' + str(request.session['username']) + '/'+upload1.name
            #     file_url = fss.url(file)

            #     query = """UPDATE USERS SET PROFILE_PIC=%s WHERE USER_ID=%s"""
            #     request.session.update({
            #         'profile_pic': photoPath
            #     })
            #     cursor.execute(query, [photoPath, str(user_id)])

            #     data.update({
            #         'profile_pic': photoPath
            #     })
            
            query = """SELECT EMAIL 
                    FROM USERS
                    WHERE USERNAME = %s"""
            cursor.execute(query, [data['username']])
            result = cursor.fetchone()
            data.update({
                'email': result[0]
            })
            cursor.close()
            
            return render(request, 'accounts/profile.html', data)
    else:
        messages.error(request, "Session Expired")
        return redirect('signin')
    
def deleteprofile(request):
    cursor = connection.cursor()
    if request.method=='POST' and request.POST.get('YES', False) and request.POST.get('YES',False)=='deluser':
        query="""SELECT USER_ID FROM USERS WHERE USERNAME=%s"""
        cursor.execute(query,[request.session.get('username')])
        result = cursor.fetchone()
        canDelete = cursor.callfunc('GET_LAST_DATE_USER', bool, [result[0]])
        if canDelete==False:
            query="""DELETE FROM USERS WHERE USERNAME=%s"""
            cursor.execute(query,[request.session.get('username')])
            request.session.flush()
            return JsonResponse({'url': ''}) 
        else:
            messages.error(request,'Some users are still staying in some of your houses.Can\'t delete profile!!')
            return JsonResponse({'url': '/accounts/profile'}) 