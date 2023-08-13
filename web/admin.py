from django.contrib import admin
from . import models
from .utils import sent_mail_to_client
# Register your models here.
# admin.site.register(models.Visitor)
# admin.site.register(models.ProductDetail)
# admin.site.register(models.Cartdetail)
@admin.register(models.Visitor)
class Visitor(admin.ModelAdmin):
    list_display=('eemail','epass','eimage')

@admin.register(models.ProductDetail)
class Productdetail(admin.ModelAdmin):
    list_display=('pid','pimage','pdetail','pprice','ptitle')

@admin.register(models.Cartdetail)
class Cartdetail(admin.ModelAdmin):
    list_display=('pid','pimage','pdetail','pprice','ptitle','pnumber','userid')

@admin.register(models.Order)
class Order(admin.ModelAdmin):
    list_display=('pid','ptitle','pprice','pnumber','ename','eemail','userid')
    actions=['proceed_order']
    def proceed_order(self, request, queryset):
        rows_updated = queryset.update(order_status=True)

        for order in queryset:
            # Extract relevant order information
            user_name = order.ename
            ptitle = order.ptitle
            pprice = order.pprice
            pnumber = order.pnumber
            user_eemail = order.eemail

            # Compose email message
            subject = 'Order Proceeded Successfully'
            user_message = f'Hello {user_name},\n\nYour order for {ptitle} (Price: {pprice} $, Quantity: {pnumber}) has been successfully processed.It will be deliver with in 3 days'

            # Send email
            sent_mail_to_client(user_eemail,user_name,user_message)

        self.message_user(request, 'Emails sent successfully to the customers.')
    
    proceed_order.short_description = 'Proceed selected orders and send email'
        
 