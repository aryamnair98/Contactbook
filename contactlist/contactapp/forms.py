from django import forms
from .models import ContactBook
from django.contrib.auth.forms import UserCreationForm
# from phonenumber_field.modelfields import PhoneNumberField
# from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ContactBookForm(forms.ModelForm):
    
    class Meta:
        model = ContactBook
        fields = ['image', 'full_name', 'relationship', 'email', 'phone_number', 'address']

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove password help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
class RemoveMembersForm(forms.Form):
    selected_members = forms.ModelMultipleChoiceField(
        queryset=ContactBook.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Select members to remove'
    )
class AddMembersToGroupForm(forms.Form):
    selected_members = forms.ModelMultipleChoiceField(
        queryset=ContactBook.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Select members to add'
    )