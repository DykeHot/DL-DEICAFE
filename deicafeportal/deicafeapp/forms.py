from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.hashers import make_password
#from betterforms.multiform import MultiModelForm
from . import models as DB

class seatform(forms.ModelForm):
    class Meta:
        model = DB.seat
        fields = "__all__"

class reserveform(forms.ModelForm):
    class Meta:
        model = DB.reservation
        fields = "__all__"

#class formfortop(MultiModelForm):
    #form_classes = {"top_seat": seatform, "top_reserve": reserveform, }


class customerform(forms.ModelForm):

    family_name = forms.CharField(max_length=20, required = True)
    personal_name = forms.CharField(max_length=20, required = True)
    telephone_number = forms.CharField(max_length=20, required=True)
    mail_address = forms.EmailField(max_length=100, required=True)
    password1 = forms.CharField(widget = forms.PasswordInput, required = True)
    password2 = forms.CharField(widget = forms.PasswordInput, required = True)

    class Meta:
        model = DB.customer
        fields = ("family_name", "personal_name", "telephone_number", "mail_address", "password1", "password2")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # パスワードが一致するかを確認
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")

        return cleaned_data


    def save(self, commit=True):
        print("form progress")
        user = super().save(commit=False)
        user.family_name = self.cleaned_data['family_name']
        user.personal_name = self.cleaned_data['personal_name']
        user.telephone_number = self.cleaned_data['telephone_number']
        user.mail_address = self.cleaned_data['mail_address']
        print(f"Before set_password: {user.password}")  
        user.set_password(self.cleaned_data["password1"])#平文で保存するのは×
        print(f"After set_password: {user.password}") 

        if commit:
            user.save()
        return user
            


class loginform(forms.Form):

    class Meta:
        model = DB.customer
        fields = ("username","password")

    username = forms.CharField(
        label="ユーザー名",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "creationform",
            "placeholder": "ユーザー名"
        })
    )
    password = forms.CharField(
        label="パスワード",
        max_length=20,
        widget=forms.PasswordInput(attrs={
            "class": "creationform",
            "placeholder": "パスワード"
        })
    )

    def __init__(self, *args, request=None, **kwargs):
        self.request = request  # 必要ならリクエストオブジェクトを保存
        super().__init__(*args, **kwargs)

    def get_user(self):
        # リクエストからユーザーを取得（例: ログインユーザー）
        return self.request.user if self.request else None
    
    




class dateform(forms.ModelForm):
    class Meta:
        model = DB.cafecalendar
        fields = ("date_field", )
        widgets = {"date_field": AdminDateWidget(), }

    
