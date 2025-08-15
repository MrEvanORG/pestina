from django.core.mail import send_mail
import random
import ghasedak_sms
import re
from django.http import JsonResponse
import time
from products.templatetags.custom_filters import format_weight , format_toman , to_jalali , to_jalali_persian

sms_api = ghasedak_sms.Ghasedak(api_key='773c50149197530bfafa31363c45965b1f743d15dc4aa61b487db6fe2dac7f3dimrGkVoVyRykik5T')



def persian_slugify(value):
    value = re.sub(r'[\u200c\u200b\u200d\uFEFF]', '',value)
    
    value = str(value).strip()

    value = re.sub(r'[^\w\s\-ا-ی]', '', value)

    value = re.sub(r'[\s‌]+', ' ', value)

    value = re.sub(r'\s+', '-', value)

    return value.strip('-')

def get_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        ip = forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def calculate_price(product,gain):
    if product.free_shipping :
        product_price = float(gain) * float(product.price)
        all_price = product_price
    else :
        product_price = float(gain) * float(product.price)
        all_price = float(gain) * float(product.price) + float(product.shipping_cost)

    return  product_price , all_price
#------------- otp secton 
otp_waited_phones = {}
WAIT_TIME = 90  
CLEANUP_INTERVAL = 300 

def is_in_waited_phones(phone):
    now = int(time.time())
    if phone in otp_waited_phones:
        if now - otp_waited_phones[phone] < WAIT_TIME:
            return True
        else:
            del otp_waited_phones[phone]
    return False

def cleanup_waited_phones():
    print("Clean up waited phones runed ")
    while True:
        time.sleep(CLEANUP_INTERVAL)
        now = int(time.time())
        expired = [phone for phone, t in otp_waited_phones.items() if now - t >= WAIT_TIME]
        for phone in expired:
            print("cleared")
            del otp_waited_phones[phone]

def send_otp(request, phone=None, name=None, mode='signup'):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "روش درخواست معتبر نیست"}, status=405)

    if not phone:
        phone = request.POST.get("phone")

    if not phone:
        return JsonResponse({"status": 400, "message": "شماره تلفن یافت نشد"}, status=400)


    if is_in_waited_phones(phone):
        request.session['otp-last-send'] = otp_waited_phones[phone]
        otp_last_send = otp_waited_phones[phone]
    else:
        otp_last_send = 0

    now_time = int(time.time())

    if now_time - otp_last_send < 90:
        remaining = 90 - (now_time - otp_last_send)
        return JsonResponse({"status": 429, "message": f"لطفاً {remaining} ثانیه صبر کنید"}, status=429)

    if mode == 'signup':
        otp_code = random.randint(100000, 999999)
        main_session = request.session.get('signup-form-data', {})
        main_session['otp-code'] = otp_code
        request.session['signup-form-data'] = main_session #save otp code in session
        newotpcommand = ghasedak_sms.SendOtpInput(
            send_date=None,
            receptors=[
                ghasedak_sms.SendOtpReceptorDto(
                    mobile=str(phone),
                )
            ],
            template_name='conf',
            inputs=[
                ghasedak_sms.SendOtpInput.OtpInput(param='Code', value=str(otp_code)),
            ],
            udh=False
        )
        response = sms_api.send_otp_sms(newotpcommand) #send otpcode to phone

        sms_status = response['statusCode']

        otp_waited_phones[phone] = now_time 
        request.session['otp-last-send'] = otp_waited_phones[phone] #save limits for sending
        if not sms_status == 200:
            return JsonResponse({"status": sms_status, "message": "ارسال پیامک با خطا مواجه شد"}, status=sms_status)
        else:
            return JsonResponse({"status": 200, "message": "کد تأیید با موفقیت ارسال شد"})


def send_ticket_message(name,phone,title,type):
    msg = f"""تیکت جدید از نوع {type}\nعنوان : {title}\nنام : {name}\nشماره تماس : {phone}"""


    response = sms_api.send_single_sms(
        ghasedak_sms.SendSingleSmsInput(
            message=msg,
            receptor='09302366684',
            line_number='30006707215215',
            send_date='',
            client_reference_id=''
        )
    )
    response = sms_api.send_single_sms(
        ghasedak_sms.SendSingleSmsInput(
            message=msg,
            receptor='09134871227',
            line_number='30006707215215',
            send_date='',
            client_reference_id=''
        )
    )
    return response

def send_order_message(name,phone,product,gain,price):
    msg = f"""سفارش محصول جدید
محصول : {product.get_kind_display()}
نام : {name}
شماره تماس : {phone}
مقدار : {format_weight(gain)}
هزینه : {format_toman(price)}"""
    print(msg)

    response = sms_api.send_single_sms(
        ghasedak_sms.SendSingleSmsInput(
            message=msg,
            receptor=product.user.phone_number,
            line_number='30006707215215',
            send_date='',
            client_reference_id=''
        )
    )

    return response