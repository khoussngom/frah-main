from django import forms
from .models import Realisation,Category

class ContactForm(forms.Form):
    prenom = forms.CharField(max_length=100)
    nom = forms.CharField(max_length=100)
    email = forms.EmailField()
    adresse = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)  # Ce champ peut être utilisé pour 'probleme' si nécessaire




class RechercheForm(forms.Form):
    CATEGORIE_CHOICES = [(cat.id, cat.nom_category) for cat in Category.objects.all()]
    categorie = forms.MultipleChoiceField(
        choices=CATEGORIE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Catégories")