from django.shortcuts import render,redirect
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import Post,Contact,Team,About,What_we_do
from django.contrib import messages
from django.views import generic
# Create your views here.
from django.template import RequestContext

def home(request):
    blogs = Post.objects.all()[:3]
    team = Team.objects.all()
    about = About.objects.all()[:1]
    what = What_we_do.objects.all()[:3]
    context = {'blogs': blogs , 'team': team , 'about': about , 'what': what}

    # create contact post
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('subject') and request.POST.get('message') :

            contact = Contact.objects.create(
                email=request.POST.get('email'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message'),
            )
            messages.success(request, 'Message Sent successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Sorry ,Please try again later!')
            return redirect('home')

    else:
        return render(request, "index.html",context)

    # return render(request, "index.html",{'blogs': blogs})

def register(request):
  #register
        if request.method == 'POST':
            password=request.POST.get('password')
            password2=request.POST.get('password2')
            if password==password2:
                if request.POST.get('username') and request.POST.get('password') and request.POST.get('email'):
                    user=User.objects.create_user(
                        first_name=request.POST.get('firstname'),
                        last_name=request.POST.get('lastname'),
                        username=request.POST.get('username'),
                        email=request.POST.get('email'),
                        password=request.POST.get('password'),
                    )
                    messages.success(request, 'User created successfully!!')
                    return render(request, "user/register.html")

                else:
                    messages.error(request, 'Something went wrong')
                    return render(request, "user/register.html")
            else:
                messages.error(request, 'User doesnt match ')
                return render(request, "user/register.html")
        else:
              return render(request, "user/register.html")

def login(request):
  #login
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_password_hashed = make_password(password)
        user = authenticate(username=username, password=password)
        if user is not None:
                auth_login(request, user)
                return redirect('../dashboard')
        else:
            messages.error(request, 'Incorrect credentials ')
            return render(request, 'user/login.html')

    return render(request, 'user/login.html')

def logout_func(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/login")

@login_required(login_url='/login')
def dashboard(request):
    blogs = Post.objects.filter(author=request.user)
    total_blogs = Post.objects.filter(author=request.user).count()
    total_members = Team.objects.all().count()
    total_contacts = Contact.objects.all().count()

    context = {'blogs': blogs, 'total_blogs': total_blogs, 'total_members': total_members, 'total_contacts': total_contacts}

    return render(request, 'dashboard/index.html', context)

@login_required(login_url='/login')
def new_blog(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('tags') and request.POST.get('content') and request.FILES['thumbnail']:

            blog_author = request.user
            status = 1
            blog = Post.objects.create(
                title=request.POST.get('title'),
                tags=request.POST.get('tags'),
                content=request.POST.get('content'),
                thumbnail=request.FILES['thumbnail'],
                status=status,
                author=blog_author,
            )
            messages.success(request, 'Blog Created successfully!')
            return redirect('create-blog')
        else:
            messages.error(request, 'Something went wrong ,Please try again later!')
            return redirect('create-blog')
    else:
        return render(request, 'dashboard/create-blog.html')

@login_required(login_url='/login')
def new_team(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('title') and request.POST.get('description')  and request.FILES['profile']:

            new_member = Team.objects.create(
                name=request.POST.get('name'),
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                profile=request.FILES['profile'],
            )
            messages.success(request, 'You Have successfully Joined Team!')
            return redirect('new-team')
        else:
            messages.error(request, 'Something went wrong. Please try again !')
            return redirect('new-team')
    else:
        return render(request, 'dashboard/new-team.html')

@login_required(login_url='/login')
def about_us(request):
    if request.method == 'POST':
        if request.POST.get('content') and request.FILES['cover']:

            about = About.objects.create(
                content=request.POST.get('content'),
                profile=request.FILES['cover'],
            )
            messages.success(request, 'You Have successfully Created About Content')
            return redirect('about-us')
        else:
            messages.error(request, 'Something went wrong. Please try again !')
            return redirect('about-us')
    else:
        return render(request, 'dashboard/new-about.html')

@login_required(login_url='/login')
def what_we_do(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('content') and request.FILES['cover']:

            new_serv = What_we_do.objects.create(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                cover=request.FILES['cover'],
            )
            messages.success(request, 'You Have successfully Created New Service Content')
            return redirect('what-we-do')
        else:
            messages.error(request, 'Something went wrong. Please try again !')
            return redirect('what-we-do')
    else:
        return render(request, 'dashboard/new-what.html')

def blogs(request):
    blog_list = Post.objects.all()
    return render(request, "blogs.html",{'blog_list': blog_list})

def blog_details(request,by):
    blogs = Post.objects.get(id=by)
    related_blogs= Post.objects.filter(tags =blogs.tags).exclude(id=blogs.id)

    context = {'blogs':blogs , 'related_blogs':related_blogs}

    return render(request,"blog_details.html",context)

def edit_blog(request,by):
    blogs = Post.objects.get(id=by)
    context = {'blogs':blogs }

    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('tags') and request.POST.get('content') and request.FILES['thumbnail']:

            blog = Post.objects.filter(pk=by).update(
                title=request.POST.get('title'),
                tags=request.POST.get('tags'),
                content=request.POST.get('content'),
                thumbnail=request.FILES['thumbnail'],
            )
            messages.success(request, 'Blog Updated successfully ')
            return render(request, "dashboard/edit-blog.html", context)
        else:
            messages.error(request, 'Something went wrong ,Please try again later!')
            return render(request,"dashboard/edit-blog.html",context)
    else:
        return render(request,"dashboard/edit-blog.html",context)

def delete_blog(request,by):
    blog_to_delete = Post.objects.get(id=by)
    blog_to_delete.delete()
    messages.success(request, 'Blog Deleted successfully!')
    return redirect('dashboard')

def search_post(request):
    if request.method == 'POST':

        title = request.POST['title']
        blog_list = Post.objects.filter(title__icontains=title)
        return render(request, "blog_results.html",{'blog_list': blog_list})
    else:
        return redirect(request, 'blogs/blog_results.html')