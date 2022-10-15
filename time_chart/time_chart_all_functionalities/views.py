from xml.sax.handler import property_interning_dict
from django.shortcuts import render , HttpResponseRedirect
from .models import user_settings , user_entry , user_status
from datetime import time , datetime , timedelta , date
from time import sleep
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from time_chart_index_page import views as index_view
from django.contrib import messages
from datetime import date

# Create your views here.

global start_tracker , stop_tracker , desc_for_track , category_of_work


@login_required()
def dashboard(request):

    new_user = "No"

    user = User.objects.get(pk=request.user.id)
    check_last_date_entry = user_settings.objects.filter(user_id=user).values('fiscal_year_start_date').last()
    tday = date.today()

    if check_last_date_entry['fiscal_year_start_date'] == None:

        status = user_status.objects.get(user_id=user)
        new_user = "Yes"
        final_display = {'user_status': status.status_now, 'remaining': 0, 'ytd': 0,
                         'performance': 0 , 'new_user': new_user}

        return render(request, 'dashboard.html', final_display)

    else:

        stop_date = check_last_date_entry['fiscal_year_start_date'] + timedelta(days=365)

        if request.user.is_authenticated:

            if tday > stop_date:

                print(bool(check_last_date_entry['fiscal_year_start_date'] < stop_date))
                print(check_last_date_entry['fiscal_year_start_date'] , stop_date)

                status = user_status.objects.get(user_id=user)
                new_user = "Yes"
                final_display = {'user_status': status.status_now, 'remaining': 0, 'ytd': 0,
                                'performance': 0 , 'new_user': new_user}

                return render(request, 'dashboard.html', final_display)
        
            else :


                status = user_status.objects.get(user_id=user)

                user_detail_to_display = user_settings.objects.filter(user_id=user).values('annual_billing_target_in_hours','user_worked_time').last()
                remaining_hour = user_detail_to_display['annual_billing_target_in_hours'] - user_detail_to_display['user_worked_time']
                remaining_hour_formatted = abs(float(format(remaining_hour,".2f")))
                ytd = user_detail_to_display['annual_billing_target_in_hours']
                performance = format((user_detail_to_display['user_worked_time'] / ytd) * 100 , ".2f")

                final_display = {'user_status' : status.status_now , 'remaining':remaining_hour_formatted , 'ytd' : ytd , 'performance':performance , 'new_user': new_user}

                return render(request,'dashboard.html',final_display)

        else:

            return HttpResponseRedirect(r'/login')


@login_required()
def account(request):

    user = User.objects.get(pk=request.user.id)
    status = user_status.objects.get(user_id=user)

    return render(request,'account.html' , {'user_status' : status.status_now})


@login_required()
def entry(request):

    new_user = "No"

    user = User.objects.get(pk=request.user.id)
    check_last_date_entry = user_settings.objects.filter(user_id=user).values('fiscal_year_start_date').last()
    tday = date.today()

    if check_last_date_entry['fiscal_year_start_date'] == None:

        status = user_status.objects.get(user_id=user)
        new_user = "Yes"
        check_ser = {'user_status': status.status_now, 'new_user': new_user}

        return render(request, 'entry.html', check_ser)

    else:

        stop_date = check_last_date_entry['fiscal_year_start_date'] + timedelta(days=365)

        if tday > stop_date:

            status = user_status.objects.get(user_id=user)
            new_user = "Yes"
            check_ser = {'user_status': status.status_now, 'new_user': new_user}

            return render(request, 'entry.html', check_ser)

        else:

            status = user_status.objects.get(user_id=user)

            if request.method == "POST":

                date1 = request.POST["date"]
                time1 = request.POST["time"]
                time1_split = time1.split(":")
                hour = int(time1_split[0])
                miniute = int(time1_split[1])
                correct_time = time(hour, miniute)
                desc = request.POST["desc"]
                category = request.POST["category"]
                user = User.objects.get(pk = request.user.id)

                new_record = user_entry(entry_date=date1 , work_time= correct_time , desc=desc , category=category , user = user)
                new_record.save()

                messages.success(request, "Entry Successfully.")

                return render(request,'entry.html', {'user_status' : status.status_now, 'new_user': new_user})

            else:

                return render(request,'entry.html', {'user_status' : status.status_now, 'new_user': new_user})


@login_required()
def listview(request):

    user = User.objects.get(pk=request.user.id)
    status = user_status.objects.get(user_id=user)
    check_last_date_entry = user_settings.objects.filter(user_id=user).values('fiscal_year_start_date').last()
    tday = date.today()

    if check_last_date_entry['fiscal_year_start_date'] == None:

        context = {'data': 'no_data', 'user_status': status.status_now}
        return render(request,'listview.html',context)

    else:

        start_date = user_settings.objects.filter(user_id=user).values('fiscal_year_start_date').last()
        stop_date = start_date['fiscal_year_start_date'] + timedelta(days=365)

        if tday > stop_date:

            context = {'data': 'no_data', 'user_status': status.status_now}
            return render(request, 'listview.html', context)

        else:

            user_entries = user_entry.objects.filter(user_id = user)

            if not user_entries:

                context = {'data': 'no_data', 'user_status': status.status_now}
                return render(request, 'listview.html', context)

            else :

                context = {'data':user_entries , 'user_status' : status.status_now}
                return render(request,'listview.html',context)


@login_required()
def user_settings1(request):

    new_user = "No"
    active_btn = "Yes"

    user = User.objects.get(pk=request.user.id)
    check_last_date_entry = user_settings.objects.filter(user_id=user).values('fiscal_year_start_date').last()
    tday = date.today()

    if check_last_date_entry['fiscal_year_start_date'] == None:

        status = user_status.objects.get(user_id=user)
        new_user = "Yes"

        if request.method == "POST":

            i = 0

            weeks = int(request.POST["time"])
            target_hour = request.POST["anl_bill"]
            year_start = request.POST["sd"]

            for c in range(0, 7):
                if request.POST.get(f"weekday{c}") is not None:
                    i = i + 1
                else:
                    continue

            work_day = i
            user = User.objects.get(pk=request.user.id)

            new_record = user_settings(annual_time_in_weeks=weeks, annual_billing_target_in_hours=target_hour,
                                       fiscal_year_start_date=year_start, working_days=work_day, user=user)
            new_record.save()

            return render(request, 'settings.html',
                          {'blocked': active_btn, 'user_status': status.status_now, 'new_user': new_user})

        else:

            return render(request, 'settings.html',
                          {'blocked': active_btn, 'user_status': status.status_now, 'new_user': new_user})
    
    else:

        stop_date = check_last_date_entry['fiscal_year_start_date'] + timedelta(days=365)

        if tday > stop_date:

            status = user_status.objects.get(user_id=user)
            new_user = "Yes"

            if request.method == "POST":

                i = 0

                weeks = int(request.POST["time"])
                target_hour = request.POST["anl_bill"]
                year_start = request.POST["sd"]

                for c in range(0, 7):
                    if request.POST.get(f"weekday{c}") is not None:
                        i = i + 1
                    else:
                        continue

                work_day = i
                user = User.objects.get(pk=request.user.id)

                new_record = user_settings(annual_time_in_weeks=weeks, annual_billing_target_in_hours=target_hour,
                                        fiscal_year_start_date=year_start, working_days=work_day, user=user)
                new_record.save()

                return render(request, 'settings.html',
                            {'blocked': active_btn, 'user_status': status.status_now, 'new_user': new_user})

            else:

                return render(request, 'settings.html',
                            {'blocked': active_btn, 'user_status': status.status_now, 'new_user': new_user})

        else :

            user = User.objects.get(pk=request.user.id)
            status = user_status.objects.get(user_id=user)
            start_date = user_settings.objects.filter(user_id=user).values('fiscal_year_start_date').last()

            if start_date['fiscal_year_start_date'] >= stop_date:

                active_btn = "No"

                if request.method == "POST":

                    i=0

                    weeks = int(request.POST["time"])
                    target_hour = request.POST["anl_bill"]
                    year_start = request.POST["sd"]

                    for c in range(0,7):
                        if request.POST.get(f"weekday{c}") is not None:
                            i = i+1
                        else:
                            continue

                    work_day = i
                    user = User.objects.get(pk = request.user.id)

                    new_record = user_settings(annual_time_in_weeks=weeks , annual_billing_target_in_hours = target_hour , fiscal_year_start_date=year_start , working_days=work_day, user=user)
                    new_record.save()

                    messages.success(request, "User settings updated successfully.")

                    return render(request,'settings.html',{'blocked':active_btn,'user_status' : status.status_now , 'new_user': new_user})

                else:

                    return render(request,'settings.html',{'blocked':active_btn,'user_status' : status.status_now, 'new_user': new_user})

            else:

                return render(request, 'settings.html',{'blocked':active_btn,'user_status' : status.status_now, 'new_user': new_user})

@login_required()
def user_delete(request):

    user = User.objects.get(pk = request.user.id)
    user.delete()
    messages.warning(request, 'User Deleted successfully')
    return HttpResponseRedirect(r'/login')

@login_required()
def user_start_tracking(request):

    user = User.objects.get(pk=request.user.id)
    check_last_date_entry = user_settings.objects.filter(user_id=user).values('fiscal_year_start_date').last()

    if check_last_date_entry['fiscal_year_start_date'] == None:

        status = user_status.objects.get(user_id=user)
        new_user = "Yes"
        return HttpResponseRedirect('/dashboard', {'new_user': new_user, 'user_status': status.status_now})

    else:

        if request.method == "POST":

            global start_tracker , desc_for_track , category_of_work
            start_tracker = datetime.now()

            status = "Active"
            user = User.objects.get(pk=request.user.id)

            desc_for_track = request.POST["desc"]
            category_of_work = request.POST["category"]

            update_user = user_status.objects.get(user_id=user)
            update_user.status_now = status
            update_user.save()

            messages.success(request, 'Tracker Started successfully.')

            return HttpResponseRedirect( '/dashboard')

        else:

            return HttpResponseRedirect('/dashboard')

@login_required()
def user_stop_track(request):

    if request.method == "POST":

        global stop_tracker , start_tracker, desc_for_track , category_of_work
        stop_tracker = datetime.now()
        today_date = date.today()
        today_date_in_str = today_date.strftime('%Y-%m-%d')

        status = "Inactive"
        user = User.objects.get(pk=request.user.id)

        user_worked_time_of_day = stop_tracker - start_tracker
        user_worked_time_of_day_hour = format(user_worked_time_of_day.total_seconds() / 60 ** 2, ".4f")

        time1_split = str(user_worked_time_of_day).split(":")
        hour = int(time1_split[0])
        miniute = int(time1_split[1])
        correct_time = time(hour, miniute)

        new_record = user_entry(entry_date=today_date_in_str, work_time=correct_time, desc=desc_for_track, category=category_of_work, user=user)
        new_record.save()

        update_user = user_status.objects.get(user_id=user)
        update_user.status_now = status
        update_user.save()

        check_eentry = user_entry.objects.last()

        if check_eentry.category == "billable":

            total_work_time = user_settings.objects.filter(user_id=user).values('annual_billing_target_in_hours','user_worked_time').last()

            if total_work_time['annual_billing_target_in_hours'] < total_work_time['user_worked_time'] :

                update_user_time = user_settings.objects.filter(user_id=user).last()

                update_user_time.user_worked_time = total_work_time['user_worked_time'] + float(user_worked_time_of_day_hour)
                update_user_time.save()

                messages.warning(request, 'You are doing overtime now.')

                return HttpResponseRedirect('/dashboard')

            else:

                update_user_time = user_settings.objects.filter(user_id=user).last()

                update_user_time.user_worked_time = total_work_time['user_worked_time'] + float(user_worked_time_of_day_hour)
                update_user_time.save()

                messages.success(request, 'Tracker Stopeed successfully.')

                return HttpResponseRedirect( '/dashboard')

        else:

            return HttpResponseRedirect('/dashboard')

    else:

        return HttpResponseRedirect('/dashboard')