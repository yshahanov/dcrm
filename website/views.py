from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm

from .models import Record

def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error loggin in, try again please!")
            return render(request, 'website/home.html', {})
    else:
        return render(request, 'website/home.html', {'records': records})



def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # auhtenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('home')
        # else:
        #     # Handle the case when the form is invalid (e.g., display error messages)
        #     # You can render the registration form with errors or take appropriate action.
        #     return HttpResponse("Registration failed. Please check your data.")  # Return an HttpResponse

    else:
        form = SignUpForm()
        return render(request, 'website/register.html', {'form':form})
    return render(request, 'website/register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # looking up for records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'website/record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in to view a page")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted succesfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete a record")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')

        return render(request, 'website/add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to add a record")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated!")
            return redirect('home')
        return render(request, 'website/update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('home')
