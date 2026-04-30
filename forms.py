# This file is used to define the forms for the project app. It includes forms for user registration, booking, review, and messaging.
# Rey Ameen, CS412

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Review, Message, Listing 

#form for creating and editing listings, with fields for title, location, price per night, description, and image

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'location', 'price_per_night', 'description', 'image']


#form for user registration, with fields for username, email, and password
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#form for creating a booking, with fields for check-in date and check-out date, and widgets to display date pickers
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }


#form for adding a review, with fields for rating and comment, and widgets to display a number input for rating and a textarea for comment
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }



#
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your message to the host...'}),
        }