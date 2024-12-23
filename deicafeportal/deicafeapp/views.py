from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import seat, menu, customer, order, reservation
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import customerform, loginform
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.contrib.auth import login as log_in
from django.http import HttpResponse, HttpResponseRedirect
import calendar

# Create your views here.

c = "./customer/"
d = "./debug/"


def SetCookie(request):

    response = HttpResponse('Visiting for the first time')

    response.set_cookie('bookname','Sherlock Holmes')

    return response
 

def GetCookie(request):

    bookname = request.COOKIES['bookname']

    return HttpResponse(f'The book name is: {bookname}')

    
#顧客用画面

class deicafebasis(TemplateView):
    template_name = "basis.html"

class login(LoginView):
    model = customer
    form_class = AuthenticationForm
    template_name = c + "login.html"
    success_url = reverse_lazy("top")
    redirect_authenticated_user = False
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("POST")

        try:
            
            customer_ = customer.objects.get(username = username)
            if customer_.check_password(password):
                log_in(request, customer_, backend = "deicafeapp.authentication.CustomAuthenticationBackend")
                
                # リダイレクト先のURLを取得
                next_url = self.request.GET.get('next') or self.get_success_url()
                print("NEXT_URL:", next_url)
                return HttpResponseRedirect(next_url)
 
            else:
                print("ELSE: Invalid password")
                return self.form_invalid(self.get_form())
 
        except customer.DoesNotExist:
            print("EXCEPTION: Customer does not exist")
            return self.form_invalid(self.get_form())
        


    def get_form_kwargs(self):
        # フォームにリクエストを渡す
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # リクエストをフォームに渡す
        return kwargs

    def get_success_url(self):
        return reverse_lazy("top")
    
    def form_invalid(self, form):
        print("Invalid!")
        print(form.errors)  # エラー時のデバッグ用
        return super().form_invalid(form)
    
    
class createaccount(CreateView):
    form_class = customerform
    model = customer
    template_name = c + "createaccount.html"
    success_url = "top"

    #fields = ("family_name", "personal_name", "telephone_number", "mail_address","password", )

    def get_success_url(self):
        return reverse_lazy("top")
    
    def form_valid(self, form):
        form.save()
        print("Form is valid!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # エラー時のデバッグ用
        return super().form_invalid(form)
    

class createsuccess(TemplateView):
    template_name = c + "createsuccess.html"

    
class top(LoginRequiredMixin, ListView):
    model = customer
    context_object_name = "customer_list"
    template_name = c + "top.html"
    #field = "__all__"

    def get_context_data(self, **kwargs):
        context = super(top, self).get_context_data(**kwargs)
        context.update({"reservation_list": reservation.objects.all(), })#ここに追加したいデータベースを追加する
        return context
    
    def get_queryset(self):
        return customer.objects.all()
    
class reservationlog(LoginRequiredMixin, FormView):#reservationはmodelの名称に使われているので棲み分けとしてlogを入れている。消さないように
    model = reservation
    template_name = c + "reservation"

class logout(LoginRequiredMixin, LogoutView):
    template_name = c + "logout.html"

#店舗用画面

class deicafedebugbasis(TemplateView):
    template_name = "debugbasis.html"

class debuglogin(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True

    template_name = d + "debuglogin.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("debugtop")



class debugtop(LoginRequiredMixin, ListView):
    model = seat
    context_object_name = "seat_list"
    template_name = d + "top.html"
    #field = "__all__"

    def get_context_data(self, **kwargs):
        context = super(debugtop, self).get_context_data(**kwargs)
        context.update({"reservation_list": reservation.objects.all(), })#ここに追加したいデータベースを追加する
        return context
    
    def get_queryset(self):
        return seat.objects.all()

class nonreservationlog(LoginRequiredMixin, CreateView):
    model = reservation
    fields = "__all__"
    context_object_name = "reservation_list"
    template_name = d + "non-reservation.html"

    



class debuglogout(LoginRequiredMixin, LogoutView):
    template_name = d + "logoutsuccess.html"




