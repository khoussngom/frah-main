from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
import PIL
from PIL import Image

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    subTitle = models.CharField(max_length=255, blank=True, null=True)
    content = RichTextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class Image(models.Model):
    image = models.ImageField(upload_to='blog_images/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
    
# class RealCat(models.Model):
#     label = models.CharField(max_length=length,)    


class ImageGroup(models.Model):
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/',blank=True,null=True)


    def __str__(self):
        return self.description or "Image Group"

class Category(models.Model):
    nom_category=models.CharField(max_length=100,unique=True)

    def __str__(self) :
        return self.nom_category
    
class Realisation(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    date_evenement = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='realisations')

    def _str_(self):
        return self.title

class RealisationImage(models.Model):
    article = models.ForeignKey(Realisation, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='articles_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Image for {self.article.title}"



class Contact(models.Model):
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"



class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
