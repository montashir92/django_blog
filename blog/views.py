from django.shortcuts import render, Http404, get_object_or_404, redirect

from . models import author, category, article, comment
from django.contrib.auth import authenticate, login, logout
#from .form import CreateForm
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import CreateForm, registerUser, createAuthor, commentForm, categoryForm
from django.contrib import messages
from django.views import View


#front Page
class index(View):
    template = "index.html"
    def get(self, request):
        post = article.objects.all()
        search_data = request.GET.get('search')
        if search_data:
            post=post.filter(
                Q(title__icontains=search_data)|
                Q(body__icontains=search_data)
            )

        paginator = Paginator(post, 6) # Show 25 contacts per page
        page = request.GET.get('page')
        total_article = paginator.get_page(page)

        context = {
            "post": total_article
        }
        return render(request, self.template, context)

#Get Post Author
class getauthor(View):
    template = "profile.html"
    def get(self, request, name):
        post_author = get_object_or_404(User, username=name)
        auth = get_object_or_404(author, name=post_author.id)
        post = article.objects.filter(article_author=auth.id)
        context = {
            "auth": auth,
            "post": post
        }
        return render(request, self.template, context)

#Post Details
class getsingle(View):
    def get(self, request, id):
        post = get_object_or_404(article, pk=id)
        getComment = comment.objects.filter(post=id)
        related = article.objects.filter(category=post.category).exclude(id=id)[:3]
        form=commentForm
        context = {
            "post": post,
            "related": related,
            "form": form,
            "comment": getComment
        }
        return render(request, "single.html", context)

    def post(self, request, id):
        post = get_object_or_404(article, pk=id)
        form = commentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post=post
            instance.save()
            return redirect('single_post', id=id)


#Category Post
class getTopic(View):
    def get(self, request, name):
        cat = get_object_or_404(category, name=name)
        post = article.objects.filter(category=cat.id)
        return render(request, "category.html",{"post":post, "cat":cat})

#User Login
class getLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        else: 
            return render(request, "login.html")

    def post(self, request):
        user=request.POST.get('user')
        password=request.POST.get('pass')
        auth=authenticate(request, username=user, password=password)
        if auth is not None:
            login(request, auth)
            return redirect('index')
        else:
            messages.add_message(request, messages.WARNING, 'Your User Name or Password not Match !!')
            return redirect('login')

#Registration
def getRegister(request):
    form = registerUser(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Registration Successfully Completed')
        return redirect('login')
    return render(request, "register.html",{"form":form})


#User Logout 
class getlogout(View):
    def get(self, request):
        logout(request)
        return redirect('index')

#Insert Post Data
def getcreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        form = CreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=u
            instance.save();
            return redirect('index')
        return render(request, 'create.html',{"form":form})
    else:
        return redirect('login')

#Update Post Data
def getUpdate(request, id):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=id)
        form = CreateForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=u
            instance.save();
            messages.success(request, 'Article Updated Successfully..')
            return redirect('profile')
        
        return render(request, 'create.html',{"form":form})
    else:
        return redirect('login')

#Delete Post Data
def getDelete(request, id):

    if request.user.is_authenticated:
        post = get_object_or_404(article, id=id)
        post.delete()
        messages.warning(request, 'Article Deleted Successfully..')
        return redirect('profile')
    else:
        return redirect('login')


#View User Profile
def getProfile(request):
    if request.user.is_authenticated:
        #user = get_object_or_404(author, name=request.user.id)
        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            post = article.objects.filter(article_author=authorUser.id)
            return render(request, "user_profile.html",{"post":post, "user":authorUser})
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name=user
                instance.save()
                return redirect('profile')
            return render(request, 'createauthor.html',{"form":form})
    else:
        return redirect('login')

#Create Category       
class getCategory(View):
    def get(self, request):
        query = category.objects.all()
        return render(request, 'topics.html', {"topic": query})

#Create Topics       
def createTopic(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = categoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Category Topics Careted Successfully..')
                return redirect('category')

            return render(request, 'create_category.html', {"form": form})
        else:
            raise Http404("You Are Not Authorized to access this page")
    else:
        return redirect('login')

#Update Topics Data
'''
def updateTopics(request, id):
        topic = get_object_or_404(category, id=id)
        form = categoryForm(request.POST or None, instance=topic)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save();
            messages.success(request, 'Topic Updated Successfully..')
            return redirect('category')
        
        return render(request, 'topics.html',{"form":form})
    

'''


 