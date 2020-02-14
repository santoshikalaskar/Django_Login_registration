from django import forms

from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'

    def password_verify(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('conformpassword')

        if password1 != password2:
            raise forms.ValidationError('Recheck your password')
        return password1
        
    def clean(self, *args, **kwargs):
        data= self.cleaned_data
        fullname = data.get('fullname', None)
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        conformpassword = data.get('conformpassword', None)
        if fullname == "" or username == "" or email == "" or password == "" or conformpassword == "":
            raise forms.ValidationError('Fill all details')
        return super().clean(*args, **kwargs)