from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import models
from django.http.request import HttpRequest
from django.http.response import HttpResponse,Http404
from .models import Blog,Realisation
from .forms import ContactForm
from .email import envoyer_email
from .models import Contact
from django.contrib import messages
from django.http import JsonResponse
from .forms import RechercheForm
from .models import Newsletter
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


# Create your views here.
def blog(request):
    form = RechercheForm(request.GET or None)
    blogs = Blog.objects.all()  # Commencez avec tous les objets Blog

    # Filtre de recherche
    if 'search' in request.GET and request.GET['search']:
        search_query = request.GET['search']
        blogs = blogs.filter(title__icontains=search_query)  # Filtre la liste `blogs` existante

    # Filtre par catégories
    if 'categorie' in request.GET:
        selected_categories = request.GET.getlist('categorie')
        blogs = blogs.filter(category__id__in=selected_categories)  # Applique le filtre supplémentaire

    context = {
        'form': form,
        'blogs': blogs,  # Passe les blogs filtrés dans le contexte
    }

    return render(request, 'blog.html', context)



def blog_detail(request,slug,id):
    blog = get_object_or_404(Blog,slug=slug,id=id)
    title = blog.title

    return render(request, 'blog_detail.html',{'blog':blog,'title':title})

def Accueil(request):
    return render(request,'index.html')  

def realisation(request):
        form = RechercheForm(request.GET or None)
        realisations = Realisation.objects.all()

        if 'search' in request.GET and request.GET['search']:
            
            realisations=realisations.filter(title__icontains=request.GET['search'])

        if 'categorie' in request.GET:
            selected_categories = request.GET.getlist('categorie')
            realisations = realisations.filter(category__id__in=selected_categories)

        context = {
            'form': form,
            'realisations': realisations,
        }

        return render(request,'realisation.html',context)  

def contact(request):
    return render(request,'contact.html')

def detail_realisation(request,id):
    
    realisation = get_object_or_404(Realisation, id=id)
    
    return render(request,'detail_realisation.html', {'realisation': realisation})

def nous_decouvrir(request):
    return render(request,'nous_decouvrir.html')


def contact(request):
    request_success = False
    if request.method == 'POST':
        # Traitement du formulaire de contact
        form = ContactForm(request.POST)
        if form.is_valid():
            prenom = form.cleaned_data['prenom']
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            adresse = form.cleaned_data['adresse']
            message = form.cleaned_data['message']

            try:
                # Envoi de l'email interne et de confirmation
                envoyer_email(prenom, nom, email, adresse, message)
                
                # Marquer le succès de l'envoi de message
                request_success = True
                messages.success(request, "Votre message a été envoyé avec succès par e-mail. Vous recevrez une confirmation sous peu.")
                
                # Enregistrez les données du message dans la base de données
                Contact.objects.create(
                    prenom=prenom,
                    nom=nom,
                    email=email,
                    adresse=adresse,
                    message=message
                )

                form = ContactForm()  # Réinitialiser le formulaire après soumission

            except Exception as e:
                messages.error(request, f"Erreur lors de l'envoi de l'e-mail : {e}")

        # Traitement de l'inscription à la newsletter
        email_newsletter = request.POST.get('email')
        if email_newsletter:
            try:
                validate_email(email_newsletter)  # Validation de l'email
                if Newsletter.objects.filter(email=email_newsletter).exists():
                    messages.info(request, "Vous êtes déjà inscrit à notre newsletter.")
                else:
                    Newsletter.objects.create(email=email_newsletter)
                    messages.success(request, "Vous êtes maintenant inscrit à notre newsletter !")
            except ValidationError:
                messages.error(request, "L'email que vous avez fourni est invalide.")
        else:
            messages.error(request, "Veuillez entrer un email valide.")

        # Rediriger vers la page de contact après traitement
        return redirect('contact')  

    else:
        form = ContactForm()

    # Rendre le template avec le formulaire et l'indication de succès
    return render(request, 'contact.html', {'form': form, 'request_success': request_success})



