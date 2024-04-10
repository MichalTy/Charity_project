from django import forms
from .models import Donation


class DonationForm(forms.ModelForm):
    """
    Form for handling donation submissions.
    """

    class Meta:
        model = Donation
        fields = ['quantity', 'categories', 'institution', 'address', 'phone_number', 'city', 'zip_code',
                  'pick_up_date', 'pick_up_time', 'pick_up_comment', 'user']
