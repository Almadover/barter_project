from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = 'title', 'description', 'category', 'condition', 'image'

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']