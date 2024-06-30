from django import forms
from .models import TelegramUser

class TelegramUserForm(forms.ModelForm):
    class Meta:
        model = TelegramUser
        fields = ['user', 'userid', 'username', 'first_name', 'last_name', 'image_data']
