from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Contact,BlogPost,PersonalBlogPost
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('num')
        desc=request.POST.get('desc')

        from_email=settings.EMAIL_HOST_USER

        if len(phone)<10:
            messages.error(request,"INVALID PHONE NUMBER")
            return render(request,'contact.html')
        if len(desc)<5:
            messages.error(request,"PROVIDE SUFFICIENT INFORMATION")
            return render(request,'contact.html')
        
        connection=mail.get_connection()
        connection.open()
        email=mail.EmailMessage(name,desc,from_email,['payalramkumar03@gmail.com'],connection=connection)
        connection.send_messages([email])
        connection.close()

        myusercontact=Contact(name=name,email=email,phone=phone,desc=desc)
        myusercontact.save()
        messages.info(request,"YOUR RESPONSE HAS BEEN RECORDED AND SENT TO ADMIN")
        return redirect('/')
    return render(request,'contact.html')

def handleSignup(request):
    if request.method == "POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1 != pass2:
            messages.warning(request,"PASSWORD DOESN'T MATCH, PLEASE TRY AGAIN")
            return redirect('/signup')
        
        try:
            if User.objects.get(username=username):
                messages.warning(request,"USERNAME EXISTS")
                return redirect('/signup')
        except Exception as identifier:
            pass

        myuser=User.objects.create_user(username,email,pass2)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.warning(request,"REGISTRATION COMPLETE")
        return redirect('/login')
    return render(request,'signup.html')

def handleLogin(request):
    if request.method == "POST":
        username=request.POST['username']
        pass1=request.POST['pass1']
        user=authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            messages.info(request,'Login Successful')
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/login") 
    return render(request,'login.html')

def handleBlog(request):
    posts=PersonalBlogPost.objects.all()
    context={'posts':posts}
    return render(request,'handleblog.html',context) 

def friends(request):
    if not request.user.is_authenticated:
        messages.error(request,"PLEASE LOGIN AND TRY AGAIN")
        return redirect('/login')

    allPosts=BlogPost.objects.all()
    context={'allPosts':allPosts}
    return render(request,'friends.html',context)

def handleLogout(request):
    logout(request)
    messages.info(request,"LOGOUT SUCCESSFUL")
    return redirect('/login')

def search(request):
    query=request.GET['search']
    if len(query) > 80:
        allPosts = BlogPost.objects.none()
    else:
        allPostsTitle = BlogPost.objects.filter(title__icontains=query)
        allPostsContent = BlogPost.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,"RESULT NOT FOUND")
    params={'allPosts':allPosts,'query':query}
    return render(request,'search.html',params)