from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.shortcuts import render ,get_object_or_404 , redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
#----------------------------------------------------------#
from .models import Product , Ticket ,BuyTicket , User 
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
    pagin = Paginator(prd,2)
    page_number = request.GET.get('page')
    page_obj = pagin.get_page(page_number)
    context = {'prd': page_obj}
    return render(request,'products.html',context)

def about_us(request):
    return render(request,"about_us.html")
# <------------------- Simple Pages ------------------->
########################################################
# <------------------- Login Pages ---------------------
@csrf_protect
def login_page(request):
    return render(request,"soon_page.html",{'text':'پستینایی عزیز به زودی میتوانید حساب کاربری ایجاد کنید ومحصولات خود را در پستینا به فروش برسانید'})
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
    return render(request,"soon_page.html",{'text':'پستینایی عزیز به زودی میتوانید حساب کاربری ایجاد کنید ومحصولات خود را در پستینا به فروش برسانید'})
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            otp = random.randint(10000,99999)
            print(">> otp" + str(otp))
            request.session['form-data'] = form.cleaned_data
            request.session['phone-number'] = form.cleaned_data['phone_number']
            request.session['otp-code'] = otp
            request.session['is-verified'] = False

            # send code with function
            # send_otp(form.cleaned_data['first_name'],form.cleaned_data['phone_number'],otp)
            return redirect(number_verify)

        else:
            context = {'form':form}
            return render(request,'l-pages/signup.html',context)




    if request.method == 'GET':
        return render(request,'l-pages/signup.html')

@csrf_protect
def number_verify(request):
    if not 'phone-number' in request.session : #if session has destroid
        return redirect(signup)
    
    if request.method == 'POST': #for submit form
        form = VerifyNumberForm(request.POST)

        if form.is_valid(): #if format of code be correct

            form_code = form.cleaned_data['code']
            otp_code = request.session.get('otp-code')
            if str(form_code) == str(otp_code) :
                request.session['is-verified'] = True
                print('phone veified save in session check for correction : '+str(request.session['is-verified']))
                return redirect(set_password)
            else:
                context = {'form':{'code':{'errors':'کد وارد شده اشتباه است'}}}
                return render(request,'l-pages/verify-sms.html',context)


        else:
            context = {'form':form}
            return render(request,'l-pages/verify-sms.html',context)


    

    if request.method == "GET": #for comming to this page from signup
        form_phone = request.session.get('phone-number')
        return render(request,'l-pages/verify-sms.html',{'number':form_phone})

@csrf_protect
def set_password(request):
    if not request.session.get('is-verified'):
        return redirect(signup)
    
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            data = request.session.get('form-data',{})
            # form = SignUpForm(data=data)
            user = User.objects.create_user(
                phone_number = data.get('phone_number'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                is_verified = True,
                username = data.get('phone_number'),
                password = form.cleaned_data['new_password1'],
                ip_address = get_ip(request),
            )
            user.save()
            del request.session['form-data'] 
            del request.session['phone-number'] 
            del request.session['otp-code'] 
            del request.session['is-verified'] 
            login(request,user)
            # login(request,user)
            request.session.set_expiry(2*60*60)
            return redirect(dashboard)

        else:
            return render(request,'l-pages/set-password.html',{'form':form})

    if request.method == 'GET':
        return render(request,'l-pages/set-password.html')

@csrf_protect
def forgotpass(request):
    return render(request,"soon_page.html",{'text':'پستینایی عزیز به زودی میتوانید حساب کاربری ایجاد کنید ومحصولات خود را در پستینا به فروش برسانید'})
    return render(request,'l-pages/forgot-pass.html')    

@csrf_protect
def dashboard(request):
    if not request.user.is_authenticated : 
        return redirect(login_page)
    return render(request,'l-pages/dashboard.html')

def user_logout(request):
    logout(request)
    return redirect(homepage)
# ------------------- Login Pages ------------------->
########################################################
# <------------------- Order-Buy Pages -----------------
@csrf_protect
def send_ticket(request,ticket_type):
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
            #send message
            # try:
            #     rs = send_order_message(ticket.buyer_namelastname,ticket.buyer_phone,ticket.request_title,form_type.label)
            # except Exception as e:
            #     print(rs,e)
            # print(rs)

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
def buy_product1(request,pid):
    # in the first check gain and calculate price and redirect to buy_product2
    order_data = request.session.get("form-data")
    if order_data:
        del request.session["form-data"]
    

    prd = Product.objects.get(id=pid)
    if request.method == 'POST':
        
        form = CheckGainBuyForm(data=request.POST,max=prd.max_order,min=prd.min_order)
        if not form.errors and form.is_valid():
            pprice , aprice = calculate_price(prd,form.cleaned_data['quantity'])
            request.session['form-data'] = {
                'product' : str(pid) ,
                'pprice' : str(pprice) ,
                'aprice' : str(aprice),
                'gain' : str(form.cleaned_data['quantity']) ,
            }
            return redirect(buy_product2)
        else:
            context = {'form':form,'p':prd} 
            return render(request,"buy_product.html",context)

    elif request.method == 'GET':
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
    'p' : Product.objects.get(id=form_data.get('product')),
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
                product = Product.objects.get(id=form_data.get('product')),
                gain = float(form_data.get('gain')),
                price = float(form_data.get('aprice')),
                post_code = int(form.cleaned_data['post_code']),
                address = form.cleaned_data['address'],
                ip_address = get_ip(request),
            )
            order.save()
            #send message
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
        'p' : Product.objects.get(id=data.get('product')),
        'gain':  float(data.get('gain')),
    }
    # try:
    #     del request.session["form-data"]
    # except:
    #     pass
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