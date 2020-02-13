from django.contrib import admin
from .models import Registration
from .forms import RegistrationForm

class RegisterAdmin(admin.ModelAdmin):
    list_display = '__all__'
    form = RegistrationForm

admin.site.register(Registration)