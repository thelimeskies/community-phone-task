from django.db import models


class AreaCodes(models.Model):
    code = models.CharField(max_length=3)
    region = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    class Meta:
        db_table = 'area_codes'
        verbose_name = 'Area Code'
        verbose_name_plural = 'Area Codes'

    def __str__(self):
        return self.code


class PhoneNumbers(models.Model):
    number = models.CharField(max_length=10)
    # area_code = models.ForeignKey(AreaCodes, on_delete=models.CASCADE)
    is_avaliable = models.BooleanField(default=True)

    class Meta:
        db_table = 'phone_numbers'
        verbose_name = 'Phone Number'
        verbose_name_plural = 'Phone Numbers'

    def __str__(self):
        return self.number
