from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import TaskForm
from .models import Task,Profile
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .helpers import send_forget_password_mail
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')
def signup(request):
    if request.method=='GET':
        return render(request,'signup.html',{
            "form": UserCreationForm
        })
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email'])
                print(user.email)
                user.save()
                login(request,user)
                return redirect('tasks')
            except: 
                return render(request,'signup.html',{
                "form": UserCreationForm,
                "error": 'Username already exist'
                })
                
        return render(request,'signup.html',{
                "form": UserCreationForm,
                "error": 'Password do not match'
                })       

@login_required
def tasks(request):
    tasks=Task.objects.filter(user=request.user,date_completed__isnull=True)
    return render(request, 'tasks.html',{'tasks':tasks})

@login_required
def dashboard(request):
    return render(request,'dashboard.html')
@login_required
def tasks_completed(request):
    tasks=Task.objects.filter(user=request.user,date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'tasks.html',{'tasks':tasks})

@login_required
def create_task(request):
    if request.method=='GET':
        return render(request,'create_task.html',{
            'form': TaskForm
        })    
    else: 
        try:
            form=TaskForm(request.POST)
            new_task=form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('tasks')
        except ValueError: 
            return render(request,'create_task.html',{
            'form': TaskForm,
            'error': 'Please provide valid data'
             })    
            
@login_required
def task_detail(request,task_id):
    if request.method=='GET':
        task=get_object_or_404(Task,pk=task_id,user=request.user)
        form=TaskForm(instance=task)
        return render(request,'task_detail.html',{'task':task,'form':form})
    else:
        try:
            task=get_object_or_404(Task,pk=task_id,user=request.user)
            form=TaskForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html',{'task':task,'form':form,'error':"Error updating task"})

@login_required
def complete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method=='POST':
        task.date_completed =timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method=='GET':
        return render(request,'signin.html',{
            "form": AuthenticationForm
        })  
    else: 
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                "form": AuthenticationForm,
                "error": "Username or password is not correct"
            })
        else: 
            login(request,user)
            return redirect('tasks')

import uuid

def ChangePassword(request, token):
    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        if profile_obj is None:
            messages.error(request, 'Invalid token.')
            return redirect('/change-password/')

        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.error(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()

            messages.success(request, 'Password has been changed successfully. Please log in with your new password.')
            return redirect('login')

    except Profile.DoesNotExist:
        messages.error(request, 'Invalid token.')
        return redirect('/change-password/')
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('/change-password/')
    except Exception as e:
        messages.error(request, 'An error occurred.')
        print(e)

    return render(request, 'change-password.html', context)

def ForgetPassword(request):
    try:
        print("Has entrado al forget password")
        if request.method == 'POST':
            username = request.POST.get('username')
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'No user found with this username.')
                return redirect('/forget-password/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj, token)

            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('/forget-password/')

    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('/forget-password/')
    except Exception as e:
        messages.error(request, 'An error occurred.')
        print(e)

    return render(request, 'forget-password.html')
