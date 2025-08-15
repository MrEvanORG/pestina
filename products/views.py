from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.shortcuts import render ,get_object_or_404 , redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import Group
#----------------------------------------------------------#
from .models import Product , Ticket ,BuyTicket , User ,Resume
from .forms import *
from .addons import *
from .blogviews import *

from time import sleep
# these are imports 
# <------------------- Simple Pages -------------------
def homepage(request):
    return render(request,'index.html')

def view_products(request):
    prd = Product.objects.all()
    pagin = Paginator(prd,6)
    page_number = request.GET.get('page')
    page_obj = pagin.get_page(page_number)
    context = {'prd': page_obj}
    return render(request,'products.html',context)

def about_us(request):
    # تمام رزومه‌ها را از دیتابیس بگیرید
    all_resumes = Resume.objects.filter(is_confirmed=True)

    # برای هر رزومه، لیست مهارت‌ها را پردازش و به آن اضافه کنید
    for resume in all_resumes:
        skill_list = []
        if resume.skills_category_1:
            skills = resume.skills_category_1.strip().split(';')
            for skill_pair in skills:
                if skill_pair and ',' in skill_pair:
                    skill_list.append(skill_pair.split(','))
        
        # یک ویژگی جدید به نام skill_list به هر آبجکت رزومه اضافه می‌کنیم
        resume.processed_skills = skill_list # type: ignore

    context = {
        'rss': all_resumes,
    }
    return render(request, 'about_us.html', context)

def resume_detail_view(request, slug):
    # ۱. رزومه مورد نظر را پیدا می‌کنیم
    resume_object = get_object_or_404(Resume,slug=slug, is_confirmed=True)

    # ۲. پردازش مهارت‌های دسته اول
    skills_1_list = []
    if resume_object.skills_category_1:
        # با strip(';') مطمئن می‌شویم سمی‌کالن اضافه در ابتدا یا انتها حذف شود
        skills = resume_object.skills_category_1.strip().strip(';').split(';')
        for skill_pair in skills:
            if skill_pair and ',' in skill_pair:
                skills_1_list.append(skill_pair.split(','))
    
    # یک ویژگی جدید به آبجکت اضافه می‌کنیم
    resume_object.processed_skills_1 = skills_1_list

    # ۳. پردازش مهارت‌های دسته دوم
    skills_2_list = []
    if resume_object.skills_category_2:
        skills = resume_object.skills_category_2.strip().strip(';').split(';')
        for skill_pair in skills:
            if skill_pair and ',' in skill_pair:
                skills_2_list.append(skill_pair.split(','))

    resume_object.processed_skills_2 = skills_2_list
    
    # ۴. آبجکت کامل شده را به تمپلیت ارسال می‌کنیم
    context = {
        'resume': resume_object,
    }
    return render(request, 'resum.html', context)
# <------------------- Simple Pages ------------------->
########################################################
# <------------------- Login Pages ---------------------
# from django.contrib.auth.models import Group

# # ... پس از اینکه کاربر جدید ساخته شد (مثلا user = User.objects.create_user(...))
# user.is_staff = True  # این خط به کاربر اجازه ورود به پنل ادمین را می‌دهد
# farmer_group = Group.objects.get(name='کشاورزان')
# user.groups.add(farmer_group)
# user.save()



@csrf_protect
def login_page(request):
    # return render(request,"soon_page.html",{'text':'پستینایی عزیز به زودی میتوانید حساب کاربری ایجاد کنید ومحصولات خود را در پستینا به فروش برسانید'})
    if request.user.is_authenticated : 
        return redirect(dashboard)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['phone_number'],
                                password=form.cleaned_data['password'])
            if user:
                login(request,user)
                request.session.set_expiry(2*60*60)
                return redirect(dashboard)
            else:
                context = {'form':form,'auth_error':True}
        
        return render(request,'l-pages/login.html',context)
            
    
    if request.method == 'GET':
        return render(request,'l-pages/login.html')

@csrf_protect
def signup(request):
    # return render(request,"soon_page.html",{'text':'پستینایی عزیز به زودی میتوانید حساب کاربری ایجاد کنید ومحصولات خود را در پستینا به فروش برسانید'})
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            request.session['signup-form-data'] = {
                "form-data":form.cleaned_data,
                "is_verified":False,
                "phone_number":form.cleaned_data['phone_number'],
            }
            return redirect(number_verify)
        else:
            context = {'form':form}
            return render(request,'l-pages/signup.html',context)

    if request.method == 'GET':
        return render(request,'l-pages/signup.html')

@csrf_protect
def number_verify(request):
    main_session = request.session.get('signup-form-data')
    if not main_session or 'phone_number' not in main_session:
        return redirect(signup)

    if request.method == "GET":
        phone = main_session.get('form-data', {}).get('phone_number')

        send_otp(request, phone,mode='signup')

        otp_last_send = request.session.get('otp-last-send',0)
        last_send = int(otp_last_send)
        now_time = int(time.time())
        retry_seconds = max(0, 90 - (now_time - last_send))

        return render(
            request,
            'l-pages/verify-sms.html',
            {'number': phone, 'retry_seconds': retry_seconds}
        )

    if request.method == "POST":
        form = VerifyNumberForm(request.POST)
        if form.is_valid():
            form_code = form.cleaned_data['code']
            otp_code = main_session.get('otp-code')

            if str(form_code) == str(otp_code):
                main_session['is-verified'] = True
                request.session['signup-form-data'] = main_session
                return redirect(set_password)
            else:
                phone = main_session.get('form-data', {}).get('phone_number')
                now_time = int(time.time())
                last_send = int(request.session.get('otp-last-send'))
                retry_seconds = max(0, 90 - (now_time - last_send))
                return render(
                    request,
                    'l-pages/verify-sms.html',
                    {'number': phone, 'retry_seconds': retry_seconds, 'form': {'code': {'errors': 'کد وارد شده اشتباه است'}}}
                )

@csrf_protect
def set_password(request):
    temp_session = request.session.get('signup-form-data',{})
    if not temp_session.get('is-verified'):
        return redirect(signup)
    
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            data = request.session['signup-form-data'].get('form-data',{})
            user = User.objects.create_user(
                phone_number = data.get('phone_number'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                is_verified = True,
                username = data.get('phone_number'),
                password = form.cleaned_data['new_password1'],
                ip_address = get_ip(request),
            )
            user.is_staff = True
            farmer_group = Group.objects.get(name='کشاورزان')
            user.groups.add(farmer_group)
            user.save()
            del request.session['signup-form-data']
            login(request,user)
            request.session.set_expiry(2*60*60)
            return redirect(dashboard)

        else:
            return render(request,'l-pages/set-password.html',{'form':form})

    if request.method == 'GET':
        return render(request,'l-pages/set-password.html')

@csrf_protect
def forgotpass(request):
    # return render(request,"soon_page.html",{'text':'پستینایی عزیز به زودی میتوانید حساب کاربری ایجاد کنید ومحصولات خود را در پستینا به فروش برسانید'})
    return render(request,'l-pages/forgot-pass.html')    


def dashboard(request):
    if request.user.is_authenticated : 
        return redirect(reverse('farmer-dashboard'))
    else:
        redirect(login_page)

def user_logout(request):
    logout(request)
    return redirect(homepage)
# ------------------- Login Pages ------------------->
########################################################
# <------------------- Order-Buy Pages -----------------
@csrf_protect
def send_ticket(request,ticket_type):
    context = None
    if str(ticket_type) == 'technical':
        context = {'title':'ارتباط با پشتیبانی/گزارش نقص فنی',
                    'text':'لطفا جهت گزارش نقص فنی فرم زیر را تکمیل کنید',
                    'form_type':'technical'}
        form_type = Ticket.TicketType.TECHNICAL
    elif str(ticket_type) == 'feedback':
        context = {'title':'ارتباط با پشتیبانی/انتقادات و پیشنهادات',
                    'text':'لطفا جهت تبادل نظراتتان فرم زیر را کامل کنید',
                    'form_type':'feedback'}
        form_type = Ticket.TicketType.FEEDBACK
    elif str(ticket_type) == 'purchase':
        context = {'title':'فرم درخواست خرید پسته',
                    'text':'لطفا جهت سفارش محصول ناموجود فرم زیر را کامل کنید',
                    'form_type':'purchase'}
        form_type = Ticket.TicketType.PURCHASE
    if not context:
        return redirect(homepage)
    
    if request.method == 'POST':
        form = OrderForm(data=request.POST, request=request)
            # ticket.save()
        if not form.errors and form.is_valid():
            if request.user.is_authenticated:
                user = request.user
            else:
                user = None       
            ticket = Ticket.objects.create(
            user = user,
            buyer_namelastname = form.cleaned_data['buyer_namelastname'],
            buyer_phone = form.cleaned_data['buyer_phonenumber'],
            request_title = form.cleaned_data['request_title'],
            request_discription = form.cleaned_data['request_text'],
            ticket_type = form_type,
            ip_address = get_ip(request))
            ticket.save()
            # send message
            try:
                rs = send_ticket_message(ticket.buyer_namelastname,ticket.buyer_phone,ticket.request_title,form_type.label)
            except Exception as e:
                print(rs,e)
            print(rs)

            request.session['buyer-phone'] = form.cleaned_data['buyer_phonenumber']
            request.session['buyer-name'] = form.cleaned_data['buyer_namelastname']
            request.session['form-type'] = ticket_type
            return redirect(registered_ticket)
        else:
            form_context = {'form':form}
            context.update(form_context)
            return render(request,"send_ticket.html",context,)

    if request.method == 'GET':
        return render(request,"send_ticket.html",context)

@csrf_protect
def buy_product1(request,slug):
    # in the first check gain and calculate price and redirect to buy_product2
    order_data = request.session.get("form-data")
    if order_data:
        del request.session["form-data"]
    
    prd = get_object_or_404(Product,slug=slug)

    if request.method == 'POST':
        
        form = CheckGainBuyForm(data=request.POST,max=prd.max_order,min=prd.min_order)
        if not form.errors and form.is_valid():
            pprice , aprice = calculate_price(prd,form.cleaned_data['quantity'])
            request.session['form-data'] = {
                'product' : str(slug) ,
                'pprice' : str(pprice) ,
                'aprice' : str(aprice),
                'gain' : str(form.cleaned_data['quantity']) ,
            }
            return redirect(buy_product2)
        else:
            context = {'form':form,'p':prd} 
            return render(request,"buy_product.html",context)

    elif request.method == 'GET':
        session_key = f"viewed_product_{prd.id}" #calcualte views
        if not request.session.get(session_key,False):
            prd.views += 1
            prd.save()
            request.session[session_key] = True
        context = {'p':prd}
        return render(request, "buy_product.html", context)

@csrf_protect
def buy_product2(request):
    form_data = request.session.get("form-data")
    if not form_data:
        return HttpResponse('sorry something happend in backend process and your order does not save\nThis is an Error !')
    context = {
    'pprice' : float(form_data.get('pprice')),
    'free_shipping' :bool(form_data.get('free_shipping')),
    'aprice' : float(form_data.get('aprice')),
    'p' : Product.objects.get(slug=form_data.get('product')),
    'gain':  float(form_data.get('gain')),
    }
    if request.method == 'GET' :
        return render(request,"send_order.html",context)
    
    elif request.method == 'POST':
        form = CheckPersonalBuyForm(data=request.POST)
        if not form.errors and form.is_valid():
            order = BuyTicket.objects.create(
                name = form.cleaned_data['buyer_namelastname'],
                phone = form.cleaned_data['buyer_phone'],
                product = Product.objects.get(slug=form_data.get('product')),
                gain = float(form_data.get('gain')),
                price = float(form_data.get('aprice')),
                post_code = int(form.cleaned_data['post_code']),
                address = form.cleaned_data['address'],
                ip_address = get_ip(request),
            )
            order.save()
            try:
                rs = send_order_message(order.name,order.phone,order.product.get_kind_display(),order.gain,order.price)
            except Exception as e:
                print(e)
            form_data['order_number'] = str(order.id).zfill(4)
            form_data['name'] = form.cleaned_data['buyer_namelastname']
            form_data['phone'] = form.cleaned_data['buyer_phone']
            form_data['post_code'] = form.cleaned_data['post_code']
            form_data['address'] = form.cleaned_data['address']

            request.session['form-data'] = form_data

            return redirect(registered_order)
        else:
            post_context = {**context,'form':form} 
            return render(request,"send_order.html",post_context)

def registered_ticket(request):
    phone = request.session.get("buyer-phone")
    name = request.session.get("buyer-name")
    form_type = request.session.get("form-type")
    if not phone or not name or not form_type:
        return redirect(send_ticket,'purchase')
    try:
        del request.session["form-type"]
        del request.session["buyer-phone"]
        del request.session["buyer-name"]
    except:
        print("error while get session")
        return redirect(send_ticket,'purchase')

    context = {"buyer_name":name,"buyer_phone":phone,"form_type":form_type}
    return render(request,'registered_ticket.html',context)

def registered_order(request):
    data = request.session.get("form-data")
    if not data :
        return redirect(view_products)
    
    context = {
        "order_number":(data.get('order_number')),
        "name":str(data.get('name')),
        "phone":int(data.get('phone')),
        "post_code":int(data.get('post_code')),
        "address":str(data.get('address')),
        'aprice' : float(data.get('aprice')),
        'p' : Product.objects.get(slug=data.get('product')),
        'gain':  float(data.get('gain')),
    }
    try:
        del request.session["form-data"]
    except:
        pass
    return render(request,'registered_order.html',context)
# ------------------- Order-Buy Pages --------------------->
############################################################
# <------------------- Error Pages -------------------------
def custom_404(request, exception):
    context = {
        'type':'404',
        'error':'404',
               }
    return render(request, 'error_page.html', status=404,context=context)

def unknown_error(request, exception=None, status_code=500):
    context = {
        'type':'other',
        'error' : status_code,
                }
    return render(request, 'error_page.html',status=status_code ,context=context)
# ------------------- Error Pages ------------------------->