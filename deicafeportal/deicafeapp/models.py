from django.db import models
from django.urls import reverse
import datetime as dt
import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission 
from django.core.validators import MinLengthValidator, RegexValidator

# Create your models here.


class seat(models.Model):
    seat_number = models.CharField(max_length=20, primary_key = True, default = "")
    reservation_number = models.TextField(max_length=20, blank = True, null = True)
    taketime = models.DateTimeField(blank = True, null = True)
    staytime = models.DurationField(blank = True, null = True)
    preorder = models.BooleanField(blank = True, null = True)

    def is_inuse(self):
        try:
            if self.objects.get(self.seat_number).taketime <= dt.datetime.now() <= self.objects.get(self.seat_number).taketime + self.objects.get(self.seat_number).staytime:
                return True
            else:
                return False
        except:
            return None


class menu(models.Model):
    menu_number = models.CharField(max_length=20, primary_key = True)
    name = models.CharField(max_length=50, default = "")
    category = models.CharField(max_length=20, default = "")
    price = models.PositiveIntegerField()
    start_date = models.DateField()

    def  __str__(self):
        return self.name
    

class customermanager(BaseUserManager):
    def create_user(self, username, email, password = None):
        if not username:
            raise ValueError("Users must have an username")
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(username = username, email = self.normalize_email(email),)

        user.set_password(password)
        user.save(using=self._db)
        return user

    #def create_superuser(self, username, email, password):
        #user = self.create_user(
            #username=username,
            #email=self.normalize_email(email),
            #password=password,
        #)
        #user.is_admin=True
        #user.is_staff=True
        #user.is_superuser=True
        #user.save(using=self._db)
        #return user

    def create_superuser(self, email, password=None, **extra_fields):
        raise NotImplementedError('Superuser is not allowed for Customer')


class customer(AbstractBaseUser, PermissionsMixin):
    customer_number = models.CharField(verbose_name = "顧客番号", unique=True, max_length=20, default = "", editable = False)
    username = models.CharField(verbose_name = "アカウント名", max_length=20, default = "", unique = True) #垢名。登録時はメールアドレス
    family_name = models.CharField(verbose_name = "苗字", max_length=20, default = "")
    personal_name = models.CharField(verbose_name = "名前", max_length=20, default = "")
    #password = models.CharField(verbose_name = "パスワード", max_length=20, default = "")
    telephone_number = models.CharField(verbose_name = "電話番号", max_length=20, default = "")
    mail_address = models.CharField(verbose_name = "メールアドレス", max_length=100, default = "")

    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,  # 'to'引数にGroupモデルを指定
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="crud_user_groups",  # related_nameを追加
        related_query_name="user",
        # through='UserGroups'  # 中間モデルの指定が必要な場合にはコメントを解除してください
    )
    user_permissions = models.ManyToManyField(
        Permission,  # 'to'引数にPermissionモデルを指定
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="crud_user_permissions",  # related_nameを追加
        related_query_name="user",
        # through='UserUserPermissions'  # 中間モデルの指定が必要な場合にはコメントを解除してください
    )



    objects = customermanager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        print("saving process")
        #customer_numberの登録
        if not self.customer_number:
            def sixnum():
                f = "C-"
                for m in range(6):
                    f += str(random.randint(0, 9))
                if "C-" + f not in list(customer.objects.values("customer_number")):
                    return f
                else:
                    sixnum()
            
            self.customer_number = sixnum()

        #usernameの登録
        if not self.username:
            self.username = self.mail_address
        if not self.password:
            print(f"Before set_password: {self.password}")
            super(customer,self).save(*args, **kwargs)
            print(f"After set_password: {self.password}")


class EmployeeManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class order(models.Model):
    order_number = models.CharField(primary_key = True, max_length=20, default = "")
    order_customer_number = models.ForeignKey(to = customer, on_delete = models.DO_NOTHING)
    order_menu_number = models.ForeignKey(to = menu, on_delete = models.DO_NOTHING)
    order_zahl = models.PositiveSmallIntegerField()

class reservation(models.Model):
    reservation_number = models.CharField(primary_key=True, max_length=20, default = "")
    reservation_customer_number = models.ForeignKey(to = customer, on_delete = models.DO_NOTHING)
    reservation_seat_number = models.ForeignKey(to = seat, on_delete= models.DO_NOTHING)
    reservation_taketime = models.DateTimeField()
    reservation_staytime = models.DurationField()
    preorder = models.BooleanField()
    details = models.TextField()

class cafecalendar(models.Model):
    date_field = models.DateField()
