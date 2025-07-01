from django.core.mail import send_mail
import random
# import ghasedak_sms

# sms_api = ghasedak_sms.Ghasedak(api_key='e7998db0c3b83b8930dab5e7f0b5585f7b269527405112e04daa3d5b3dac7be07JDnwtTAE2JR2Kzy')

# #salehih1227@gmail.com
# # def Generate_email(type,name,phone,title,discription,pistachio,gain,price):
# #     if type == 'order':
# #         text = f"""نام درخواست دهنده : {name}
# # شماره تماس : {phone}
# # عنوان درخواست : {title}
# # شرح درخواست : {discription}
# # محصول سفارش داده شده : {pistachio}
# # """
# #         send_mail('درخواست خرید جدید',text,'pestina.ir@gmail.com',['ehsan66845@gmail.com'],fail_silently=True)
# #     if type == 'buy':
# #         text = f"""نام خریدار : {name}
# # شماره تماس : {phone}
# # توضیحات : {discription}
# # مقدار سفارش داده شده : {gain} کیلوگرم
# # هزینه نهایی : {price} تومان """
# #         send_mail('سفارش خرید جدید',text,'pestina.ir@gmail.com',['ehsan66845@gmail.com'],fail_silently=True)
# #         send_mail('test1','salam',['pestina.ir@gmail.com'],['ehsan66845@gmail.com',],fail_silently=False)

# def send_otp(name,number,otp):
#     text = f'{name} عزیز به پستینا خوش آمدید '+f'\n کد ورود شما {otp} می باشد'+'\n لغو ۱۱'
#     response = sms_api.send_single_sms(
#         ghasedak_sms.SendSingleSmsInput(
#             message=text,
#             receptor=number,
#             line_number='10008642',
#             send_date='',
#             client_reference_id=''
#         )
#     )
#     print(response)




def get_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        ip = forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def calculate_price(product,gain):
    if product.free_shipping :
        product_price = int(gain) * int(product.price)
        all_price = product_price
    else :
        product_price = int(gain) * int(product.price)
        all_price = int(gain) * int(product.price) + int (product.shipping_cost)
    return  product_price , all_price
