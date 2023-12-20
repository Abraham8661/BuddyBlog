from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):

    class Meta:
        model= User
        fields = ("email", "first_name", "last_name")

    def save(self, commit: bool = True) -> User:
        email = self.cleaned_data["email"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        password = self.cleaned_data["password1"]

        return User.objects.create_user(email, first_name, last_name, password, commit=commit)
    
#class SignUpForm(UserCreationForm):
#
#    class Meta:
#        model= User
#        fields = ("email", "first_name", "last_name")
#
#    def save(self, commit: bool = True) -> User:
#        email = self.cleaned_data["email"]
#        password = self.cleaned_data["password1"]
#
#        return User.objects.create_user(email, password, commit=commit)
