from django.core.mail import send_mail
import random
import ghasedak_sms

sms_api = ghasedak_sms.Ghasedak(api_key='773c50149197530bfafa31363c45965b1f743d15dc4aa61b487db6fe2dac7f3dimrGkVoVyRykik5T')


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
محصول : {product}
نام : {name}
شماره تماس : {phone}
مقدار : {gain}
هزینه : {price}"""
    print(msg)

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