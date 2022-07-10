from smtplib import SMTPException
from rest_framework import views
from .models import AreaCodes, PhoneNumbers
from django.core.mail import send_mail
from rest_framework.response import Response


class GetNumbers(views.APIView):
    """
    note: User Must be Logged in to use this Endpoint
    params:
        area_code: 3 digit area code
    returns:     Response object with phone number
    description: This takes in a 3 digit area code and returns a phone number
                Provided that the area code exists in the database and is
                available exclusively in US.
    errors:     If the area code does not exist in the database, an error is
                returned.
                If the area code is not exclusively US, an error is returned.
                If the area code exists but there are no more numbers
                available, an error is returned.
                If the email cannot be sent, an error is returned.
    """

    def post(self, request):
        email = request.user.email
        print(email)
        area_code = request.data.get('area_code')
        if AreaCodes.objects.filter(code=area_code, country='US').exists():
            try:
                if PhoneNumbers.objects.filter(number__startswith=area_code,
                                               is_avaliable=True).exists():
                    phone_number = PhoneNumbers.objects.filter(
                        number__startswith=area_code, is_avaliable=True).first()
                    send_mail('Phone Number',
                              phone_number.number,
                              'test@example.com',
                              [email],
                              fail_silently=False
                              )
                    phone_number.is_avaliable = False
                    phone_number.save()
                    return Response({'Phone Number': phone_number.number})
                else:
                    phone_number = PhoneNumbers.objects.filter(
                        is_avaliable=True).first()
                    send_mail('Phone Number',
                              phone_number.number + 'Area Code: ' + area_code +
                              'not available',
                              'test@example.com',
                              [email],
                              fail_silently=False
                              )
                    phone_number.is_avaliable = False
                    phone_number.save()
                    return Response({'Phone Number': phone_number.number})
                    # return Response({'message': 'No more numbers available'})
            except SMTPException:
                return Response({'error': 'Email not sent Server Error'})
        else:
            return Response({'error': 'Area Code not found'})
