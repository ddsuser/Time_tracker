from django.shortcuts import render , HttpResponseRedirect , HttpResponse
from .forms import registeration_form , login_form , change_password_form , change_email_form
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout , update_session_auth_hash
import csv
from django.contrib.auth.decorators import login_required
from time_chart_all_functionalities .models import user_entry , user_settings , user_status
from django.contrib.auth.models import User
from time_chart_all_functionalities.models import user_feedback
from datetime import datetime
import os

# Create your views here.
# registration_form = rf

def index(request):
    rf = registeration_form()
    if request.method == "POST":
        rf = registeration_form(request.POST)
        if rf.is_valid():

            uname = request.POST['username']
            rf.save()

            path = f"time_chart_all_functionalities\Screenshots\{uname}"

            if not os.path.exists(path):
                os.makedirs(path)

            reg_user = User.objects.get(username = uname)

            entry_record_settings = user_settings(user=reg_user)
            entry_record_settings.save()

            entry_record_status = user_status(user=reg_user)
            entry_record_status.save()

            messages.success(request,f'User Succrssfully Registred')
            messages.success(request,'Login Here')

            return HttpResponseRedirect('/login')
        else:
            return render(request, 'index_form.html', {'form': rf})
    else:
        return render(request, 'index_form.html', {'form': rf})

# login_form = lf
 
def user_login_form(request):

    lf = login_form()
    if request.method == "POST":
        lf = login_form(request=request , data= request.POST)
        if lf.is_valid():
            uname =lf.cleaned_data['username']
            pwd =lf.cleaned_data['password']
            user = authenticate(request , username=uname , password = pwd)
            if user is not None :
                login(request, user)
                global login_time
                login_time = datetime.now()

                messages.success(request, f'Welcome {uname}')

                return HttpResponseRedirect('/dashboard')
            else:
                return render(request, 'login.html', {'form': lf})
        else:
            return render(request, 'login.html', {'form': lf})
    else:
        return render(request, 'login.html', {'form': lf})

@login_required()
def user_logout(request):

    logout(request)
    messages.success(request, 'Thank you.')
    return HttpResponseRedirect('/login')

@login_required()
def user_password_change(request):
    cpm = change_password_form(request.user)
    if request.method == "POST":
        cpm = change_password_form(user=request.user , data=request.POST)
        if cpm.is_valid():
            cpm.save()
            update_session_auth_hash(request , cpm.user)
            messages.success(request, 'Password Changed Successfully')
            return HttpResponseRedirect('/account')
        else:
            return render(request , 'change_password.html',{'form':cpm})
    else:
        cpm = change_password_form(user=request.user)
        return render(request, 'change_password.html', {'form': cpm})

@login_required()
def user_email_change(request):

    cem = change_email_form(instance=request.user)

    if request.method == 'POST':
        cem = change_email_form(request.POST ,instance=request.user)

        if cem.is_valid():
            cem.save()
            messages.success(request, 'E-mail Changed Successfully')
            return HttpResponseRedirect('/account')
        else:
            return render(request, 'change_email_form.html', {'form': cem})

    else:
        cem = change_email_form(instance=request.user)

    return render(request , 'change_email_form.html' , {'form' : cem})

@login_required()
def user_time_chart_export(request):

    user = User.objects.get(username=request.user)

    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)

    writer.writerow(['Entry_date' , 'Work_time' , 'Worked_time' , 'Description' , 'Category_Of_Entry'])

    for entries in user_entry.objects.filter(user_id = user).values_list('entry_date','work_time','desc','category'):
        writer.writerow(entries)

    response['Content-Disposition'] = f'attachment; filename="{user.username}.csv"'

    messages.success(request, 'Your Time Chart exported successfully.;')

    return response

@login_required()
def submit_feedback(request):

    if request.method == "POST":

        feedback = request.POST["feedback"]
        dt = datetime.now()
        user = User.objects.get(pk = request.user.id)

        new_record = user_feedback(feedback=feedback, date_time=dt, user=user)

        new_record.save()

        messages.success(request, 'Feedback submitted successfully.')

        return HttpResponseRedirect('/account')

    else:

        return render(request , 'submitfeedback.html' )


