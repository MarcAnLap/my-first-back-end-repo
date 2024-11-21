from django.forms import ModelForm
from .models import Booking
from django import forms

# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        widgets = {
            'reservation_date': forms.SelectDateWidget(),  # Utiliser un widget pour le sélecteur de date
            'time_slot': forms.Select(choices=[('09:00', '09:00'), ('10:00', '10:00')]),  # Sélecteur pour les créneaux horaires
        }
