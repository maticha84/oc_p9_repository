from django import forms

from .models import Ticket, Review, User


class TicketForm(forms.ModelForm):
    """
    Template for the ticket creation/change form
    """
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    """
    Template for the review creation / change form
    """
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body', ]
        CHOICES = (
            (0, ' - 0'),
            (1, ' - 1'),
            (2, ' - 2'),
            (3, ' - 3'),
            (4, ' - 4'),
            (5, ' - 5'),
        )
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.RadioSelect(choices=CHOICES),
        }
