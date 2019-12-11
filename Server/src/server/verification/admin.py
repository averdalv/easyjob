from django.contrib import admin

# Register your models here.
from verification.models import EmailVerification, PerformerVerification, BaseVerification, CustomerVerification, \
    FirmVerification

admin.site.register(EmailVerification)
admin.site.register(PerformerVerification)
admin.site.register(BaseVerification)
admin.site.register(CustomerVerification)
admin.site.register(FirmVerification)
