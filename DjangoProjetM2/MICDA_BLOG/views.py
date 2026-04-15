from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Article, Commentaire
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django import forms

def home (request):
    
    query = request.GET.get('q')

    if query:
        articles = Article.objects.filter(
            Q(titre__icontains=query) | 
            Q(contenu__icontains=query)
        )
    else:
        articles = Article.objects.all().order_by('-date_publication')
    return render (request, 'MICDA_BLOG/home.html', {'articles': articles})
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image']

@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            return redirect( 'home')
    else:
        form = ArticleForm()
    return render(request, 'MICDA_BLOG/add_article.html', {'form': form})



def article_detail(request, id):

    article = get_object_or_404(Article, id=id)
    commentaires = article.commentaire_set.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login') 
        
    contenu = request.POST.get('contenu')
    if contenu and contenu.strip():
            Commentaire.objects.create(
                article=article,
                utilisateur=request.user,
                contenu=contenu
            )
            return redirect('article_detail', id=id)

    return render(request, 'MICDA_BLOG/article_detail.html', {
        'article': article,
        'commentaires': commentaires
    })

def register(request): 
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, "Compte créé avec succès ")
            
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'MICDA_BLOG/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'MICDA_BLOG/profile.html')

class CustomLoginView(LoginView):
    template_name = 'MICDA_BLOG/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.username == "MalickBa3":
            return reverse_lazy('admin:index')
        
        return reverse_lazy('home')
