from django.contrib import admin
from .models import customer, Employee, menu, order, reservation, seat
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy

# Register your models here.


@admin.register(menu)
class menuadmin(admin.ModelAdmin):
    list_display = ("menu_number", "name", "category", "price", "start_date")

@admin.register(order)
class orderadmin(admin.ModelAdmin):
    list_display = ("order_number", "order_customer_number", "order_menu_number", "order_zahl")

@admin.register(reservation)
class reservationadmin(admin.ModelAdmin):
    list_display = ("reservation_number", "reservation_customer_number", "reservation_seat_number", "reservation_seat_number", "reservation_taketime", "reservation_staytime", "preorder", "details")

@admin.register(seat)
class seatadmin(admin.ModelAdmin):
    list_display = ("seat_number", "reservation_number", "taketime", "staytime", "preorder")

@admin.register(Employee)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_superuser')

@admin.register(customer)

class customeradmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (gettext_lazy("personal info"), {"fields": ("family_name", "personal_name", "telephone_number", "mail_address")}),
        (gettext_lazy("permissions"), {"fields": ("is_active", "is_staff", "is_admin", "groups", "user_permissions")}),
        )
    
    list_display = ("customer_number", "family_name", "personal_name", "telephone_number", "mail_address")



