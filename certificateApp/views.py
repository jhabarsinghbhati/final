import os
from django.shortcuts import render, redirect, reverse, Http404, get_object_or_404,render_to_response,HttpResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.core.files import File
from django.http import JsonResponse
from django.conf import settings
import threading
import datetime
from django.utils import timezone
from .functions import send_email, save_user, delete_inactive, generate_token, delete_user_inactive, change_token, get_intern, welcoming_message
from .certificate import generate_certificate
from .models import Report, Project, Certificate, User, UserProfile, Profile, TenureChoice,PersonalDetail,Project,CertificateConfig
from .forms import ReportSubmissionForm, PersonalDetailForm, ProjectDetailsForm, InternForm
from .decorators import is_admin, is_intern,is_personaldetail_editable,is_project_editable,is_report_editable

login_required = login_required(login_url=reverse_lazy('certificate_app:login'))

def register_user(request):
    ''' registration of interns '''
    if request.user.is_authenticated:
        if UserProfile.objects.all().filter(user=request.user):
            return redirect(reverse('certificate_app:personal_detail'))
        elif request.user.is_superuser or get_user_model().is_irscadmin:
            return redirect(reverse('certificate_app:mentor'))
    # delete inactive user
    # form = UserForm(None)
    form = InternForm(None)

    if request.method == 'POST':

        # form = UserForm(request.POST)
        form = InternForm(request.POST)
        # user = User.objects.all().filter(email='jhabarsinghbhati23@gmail.com').first()
        # Profile.objects.all().filter(user=user).first().delete()
        # user.delete()
        delete_inactive(request.POST.get('email'))
        if form.is_valid():
            if not get_user_model().objects.all().filter(email=request.POST.get('email')).first():
                save_user(request.POST)

                # id = User.objects.all().filter(email=request.POST.get('email')).first().id
                # full_name = request.POST.get('first_name')+' '+request.POST.get('last_name')
                # thread = threading.Thread(target=send_email, args=(full_name, id, request.POST.get('email')))

                # thread1 = threading.Thread(
                #     target=delete_user_inactive, args=(request.POST.get('email'),))
                # # thread.start()
                # thread1.start()
                # send_email(full_name, id, request.POST.get('email'))
                return redirect(reverse('certificate_app:register_activation'))
            messages.error(request, 'User Name Already Exist')
    return render(request, 'register.html', context={'form': form})


def login(request):
    ''' login user '''
    if request.user.is_authenticated:
        if UserProfile.objects.all().filter(user=request.user):
            return redirect(reverse('certificate_app:personal_detail'))
        elif request.user.is_superuser or get_user_model().is_irscadmin:
            return redirect(reverse('certificate_app:mentor'))
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile = Profile.objects.all().filter(intern=get_intern(email)).first()
        if get_user_model().objects.all().filter(email=email).first():
            user = authenticate(request, email=email,
                                password=password)
            if user and get_user_model().objects.all().filter(email=email).first().is_superuser:
                auth_login(request, user)
                return redirect(reverse("certificate_app:mentor"))
        if profile:
            if profile.is_active:
                user = authenticate(request, email=email,
                                    password=password)
                print('$$$$$$$$$$$$$$$$')
                if user:
                    if user.is_active:
                        auth_login(request, user)
                        id = user.id
                        return redirect(reverse("certificate_app:personal_detail"))
                    else:
                        messages.error(request, "Not A Active User")

    return render(request, "login.html")


# def login_admin(request):
#   ''' login admin '''

#   if request.method == "POST":
#       email = request.POST.get("email")
#       password = request.POST.get("password")

#       user = authenticate(request, email=email,
#                           password = password)
#       if user:
#           if user.is_superuser:
#               auth_login(request, user)
#               return redirect(reverse("certificate_app:mentor"))
#           else:
#               messages.error(request, "Not A Admin User")
#       else:
#               messages.error(request, "Invalid Credentials")
#   return render(request, "admin_login.html")


# @login_required
# def logout_user(request):
#   ''' logout user'''

#   return render(request, 'logout.html')


@login_required
def confirm_logout_user(request):
    # if request.user.is_authenticated:
    #       if UserProfile.objects.all().filter(user=request.user):
    #           if UserProfile.objects.all().filter(user=request.user).is_admin:
    #               return redirect(request, 'certificate_app:mentor')
    #           else:
    #               return redirect(request, 'certificate_app:personal_detail')

    if request.POST.get("ok" or None):
        logout(request)
        return redirect(reverse("certificate_app:confirm_logout"))
    if request.POST.get("cancel" or None):
        return redirect(reverse("certificate_app:personal_detail"))

    return render(request, "confirm_logout.html")


def register_activation(request):
    ''' link open when user regiters and email is sent to his/her Id
        displays that got to your email to authenticate
    '''
    messages.info(request,'An email has been sent to you with instruction to login furthur. It will expire in 1 hour.')
    # return render(request, 'register_activation.html')
    return render(request, 'register_tok.html')


def register_token(request, key):
    ''' verifies if the given activation key is valid or not
    '''
    profile = Profile.objects.all().filter(activation_key=key).first()

    if profile:
        profile = Profile.objects.all().filter(activation_key=key).first()
        name = profile.intern
        welcoming_message(name)
        print(profile.intern)
        Profile.objects.all().filter(activation_key=key).update(is_active=True)
        Profile.objects.all().filter(activation_key=key).update(
            activation_key=generate_token())

        return redirect(reverse('certificate_app:login'))
    return render(request, 'register_token.html', context={'data': key})


def forgot_password(request):
    if request.user.is_authenticated:
        if UserProfile.objects.all().filter(user=request.user):
            return redirect(reverse('certificate_app:personal_detail'))
        elif request.user.is_superuser or get_user_model().is_irscadmin:
            return redirect(reverse('certificate_app:mentor'))
    ''' forgot password logic '''
    if request.POST.get('email'):
        if get_user_model().objects.all().filter(email=request.POST.get('email')).first():
            send_email(None, None, request.POST.get('email'), True)
            # thread1 = threading.Thread(
            #     target=change_token, args=(request.POST.get('email'),))
            # thread1.start()
            # return render(request, 'forgot_password_activation.html')
            # Profile.objects.all().filter(intern=get_intern(
            # email)).update(activation_key=generate_token(), forgot_password_activation)
            
            messages.info(request,'An Email has been sent to you with instructions to reset your password.')
            return render(request, 'forgot_password_activation.html')
    return render(request, 'forgot_password.html')


def forgot_password_confirm(request, key):
    if request.user.is_authenticated:
        if UserProfile.objects.all().filter(user=request.user):
            if not UserProfile.objects.all().filter(user=request.user).first().is_admin:
                return redirect(reverse('certificate_app:personal_detail'))
        elif request.user.is_superuser or get_user_model().is_irscadmin:
            return redirect(reverse('certificate_app:mentor'))

    profile = Profile.objects.all().filter(activation_key=key).first()
    print("######################\n")
    if profile:
        if profile.forgot_password_timestamp + timezone.timedelta(hours=1) <= timezone.now():
            return render(request, 'register_token.html')
        else:
            print("######################\n")
            password = request.POST.get('new_password') or ''
            new_password = request.POST.get('confirm_new_password') or ''
            print(password is new_password, '\n')
            if password and password == new_password and len(password) >= 8:
                profile.intern.user.set_password(password)
                profile.intern.user.save()
                change_token(profile.intern.user.email)
                return redirect(reverse('certificate_app:login'))
            elif len(password) < 8 and password != '':
                messages.error(request, 'Invalid Password')
        return render(request, 'new_password.html')
    return render(request, 'register_token.html')


# -------------------------------------------------------------------------------------------------
@login_required
def personaldetail(request):
    if request.method == 'POST':
        form = PersonalDetailForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid --------------------")
            form.instance.user = request.user
            form.save()
            return redirect('certificate_app:project')
        return render(request, 'personaldetail/detail.html', {'form': form})
    if hasattr(request.user, 'personaldetail'):
        # print("has personal details -------------------------")
        context = {
            'details': request.user.personaldetail
        }
    else:
        form = PersonalDetailForm()
        context = {
            'form': form
        }
    return render(request, 'personaldetail/detail.html', context=context)


@login_required
@is_personaldetail_editable
def personaldetailupdate(request):
    if not hasattr(request.user, 'personaldetail'):
        return redirect('certificate_app:personal_detail')
    if request.method == 'GET':
        personaldetail = request.user.personaldetail
        form = PersonalDetailForm(instance=personaldetail)
        return render(request, 'personaldetail/detailupdate.html', {'form': form})
    elif request.method == 'POST':
        personaldetail = request.user.personaldetail
        form = PersonalDetailForm(request.POST, instance=personaldetail)
        if form.is_valid():
            #logic for changing end date in project as well 
            tenure = form.cleaned_data.get('internship_tenure')
            try:
                key, duration = [val for val in str(tenure).split()]
            except:
                key, duration = ['1','month']
            if duration == "months" or duration == "month":
                duration = relativedelta(months=+int(key))
            else:
                duration = relativedelta(years=+int(key))
            project = get_object_or_404(Project,user=request.user)
            project.end_date = project.joining_date + duration
            project.tenure = tenure
            project.save()

            #logic for managing editability
            form.instance.is_editable = 'P'
            form.instance.request_edit = False

            form.save()
            return redirect('certificate_app:personal_detail')
        return render(request, 'personaldetail/detailupdate.html', {'form': form})

@login_required
def request_personaldetail_update(request):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        print(reason)
        intern = request.user
        f = PersonalDetail.objects.filter(user=intern).first()
        f.request_edit = True
        f.edit_reason = reason
        f.is_editable = 'P'
        f.save()
        return redirect('certificate_app:personal_detail')

# -----------------------------------------------------------------------


@login_required
def project(request):
    if not hasattr(request.user, 'personaldetail'):
        messages.warning(
            request, 'please fill your personal details to have access to next page')
        return redirect('certificate_app:personal_detail')

    try:
        key, duration = [val for val in str(
            request.user.personaldetail.internship_tenure).split()]
    except:
        key, duration = ['1','month']
    # print(duration,key)
    if duration == "months" or duration == "month":
        duration = relativedelta(months=+int(key))
    else:
        duration = relativedelta(years=+int(key))
    values = {
        'profile': request.user.personaldetail.profile,
        'project_worked_on': request.user.personaldetail.project,
        'tenure': request.user.personaldetail.internship_tenure,
        'joining_date': request.user.personaldetail.joining_date,
        'end_date': request.user.personaldetail.joining_date + duration
    }
    if request.method == 'POST':
        form = ProjectDetailsForm(request.POST, initial=values)
        if form.is_valid():
            print("form is valid --------------------")
            form.instance.user = request.user
            form.instance.joining_date = values['joining_date']
            form.instance.end_date = values['end_date']
            form.instance.profile = values['profile']
            form.instance.tenure = values['tenure']
            form.instance.project_worked_on = values['project_worked_on']
            form.save()
            return redirect('certificate_app:report')
        # print('form invalid',form.errors)
        return render(request, 'project/project.html', {'form': form})
    if hasattr(request.user, 'project'):
        # print("has personal details -------------------------")
        context = {
            'project': request.user.project
        }
    else:
        form = ProjectDetailsForm(initial=values)
        context = {
            'form': form
        }
    return render(request, 'project/project.html', context=context)


@login_required
@is_project_editable
def projectupdate(request):
    if not hasattr(request.user, 'project'):
        return redirect('certificate_app:project')
    try:
        key, duration = [val for val in str(
            request.user.personaldetail.internship_tenure).split()]
    except:
        key, duration = ['1','month']
    # print(duration,key)
    if duration == "months" or duration == "month":
        duration = relativedelta(months=+int(key))
    else:
        duration = relativedelta(years=+int(key))
    values = {
        'profile': request.user.personaldetail.profile,
        'project_worked_on': request.user.personaldetail.project,
        'tenure': request.user.personaldetail.internship_tenure,
        'joining_date': request.user.personaldetail.joining_date,
        'end_date': request.user.personaldetail.joining_date + duration
    }
    if request.method == 'GET':
        project = request.user.project
        form = ProjectDetailsForm(instance=project)
        return render(request, 'project/projectupdate.html', {'form': form})
    elif request.method == 'POST':
        project = request.user.project
        form = ProjectDetailsForm(request.POST, instance=project)
        if form.is_valid():
            form.instance.joining_date = values['joining_date']
            form.instance.end_date = values['end_date']
            form.instance.profile = values['profile']
            form.instance.tenure = values['tenure']
            form.instance.project_worked_on = values['project_worked_on']
            #logic for managing editability
            form.instance.is_editable = 'P'
            form.instance.request_edit = False
            form.save()
            return redirect('certificate_app:project')
        return render(request, 'project/projectupdate.html', {'form': form})

@login_required
def request_project_update(request):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        print(reason)
        intern = request.user
        f = Project.objects.filter(user=intern).first()
        f.edit_reason = reason
        f.request_edit = True
        f.is_editable = 'P'
        f.save()
        return redirect('certificate_app:project')


# --------------------------------------------------------------------------------
@login_required
def reportview(request):
    if not hasattr(request.user, 'personaldetail'):
        messages.warning(
            request, 'please fill your personal details to have access to next page')
        return redirect('certificate_app:personal_detail')
    elif not hasattr(request.user, 'project'):
        messages.warning(
            request, 'please fill your project details to have access to next page')
        return redirect('certificate_app:project')
    if request.method == 'POST':
        form = ReportSubmissionForm(request.POST, request.FILES)
        if form.is_valid:
            form.instance.user = request.user
            form.save()
            return redirect('certificate_app:report')
        return render(request, 'report/report.html', {'from': form})
    form = ReportSubmissionForm()
    return render(request, 'report/report.html', {'form': form})


@login_required
@is_report_editable
def reportupdate(request):
    if not hasattr(request.user, 'report') or hasattr(request.user, 'certificate'):
        return redirect('certificate_app:report')
    if request.method == 'GET':
        report = request.user.report
        form = ReportSubmissionForm(instance=report)
        return render(request, 'report/reportupdate.html', {'form': form})
    elif request.method == 'POST':
        report = request.user.report
        form = ReportSubmissionForm(
            request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.instance.status = "P"
            form.save()
            return redirect('certificate_app:report')
        return render(request, 'report/reportupdate.html', {'form': form})


# ---------------------------------------------------------------------------

@login_required
@is_admin
def adminpage(request):
    # if request.user.is_staff:
    get = request.GET.get
    if(get('reg_number')):
        # user = User.objects.filter(
        #     userprofile__registration_number=get('reg_number').strip())
        user = UserProfile.objects.filter(
            registration_number=get('reg_number').strip())
    elif(get('first_name')):
        # user = User.objects.filter(
        #     userprofile__first_name__iexact=get('first_name').strip())
        user = UserProfile.objects.filter(
            first_name__iexact=get('first_name').strip())
    elif(get('last_name')):
        user = UserProfile.objects.filter(
            last_name__iexact=get('last_name').strip())
    elif(get('days_from_now')):
        days = int(get('days_from_now').strip())
        user = UserProfile.objects.filter(project__end_date__gte=datetime.now(
        ), project__end_date__lt=datetime.now()+timedelta(days=days))
    elif(get('update_request')):
        user = UserProfile.objects.filter(Q(personaldetail__request_edit=True) | Q(project__request_edit=True))
        # print(user)
    else:
        user = UserProfile.objects.all()
    return render(request, 'admin/adminpage.html', {'user': user})
    # raise PermissionDenied()


@login_required
@is_admin
def create_certificate(request, pk):
    # if request.user.is_staff:
    intern = get_object_or_404(User, id=pk)
    try:
        intertype = intern.personaldetail.type_of_internship
        profile = intern.personaldetail.profile
        logo = intern.personaldetail.project
        name = intern.userprofile.get_full_name()
        renumber = intern.userprofile.registration_number
    except:
        return JsonResponse({'message': 'Intern has not proper personal details'}, status=404)

    try:
        start_date = intern.project.joining_date
        end_date = intern.project.end_date
    except:
        return JsonResponse({'message': 'Intern has not proper project details'}, status=404)

    if not hasattr(intern, 'certificate'):
        c = Certificate(user=intern)

        filepath = os.path.join(settings.BASE_DIR, 'certificate_file')
        # savepath = os.path.join(settings.MEDIA_ROOT, 'certificates')
        print(logo)
        logo = 'logo'

        png, pdf = generate_certificate(
            filepath, name, intertype, profile, start_date, end_date, logo, renumber)

        c.certificate_pdf.save(
            f'certificate_{renumber}.pdf', File(open(pdf, 'rb')), save=False)
        c.certificate_png.save(
            f'certificate_{renumber}.png', File(open(png, 'rb')), save=True)
        os.remove(png)
        os.remove(pdf)
        # return HttpResponse(f'<div>certificate created successfully with cf no - <a href="{c.certificate_pdf.url}" >{c.certificate_pdf}</a></div>')
        data = {
            'pdfurl': c.certificate_pdf.url,
            'pngurl': c.certificate_png.url,
            'delurl': reverse('certificate_app:delete_certificate',args=pk),
            'cktno': c.certificate_number
        }
        return JsonResponse(data)
    return JsonResponse({'message': 'certificate already created please refresh page.'}, status=404)
    # raise PermissionDenied()

@login_required
@is_admin
def delete_certificate(request, pk):
    try:
        certificate = get_object_or_404(User, id=pk).certificate
    except:
        return JsonResponse({'message':'User has no certificate'})
    # report = get_object_or_404(User, id=pk).report
    # report.status = 'P'
    # report.save()
    certificate.delete()
    data = {
        'message': 'Certificate deleted successfully',
        'creurl' : reverse('certificate_app:create_certificate',args=pk),
        'upurl' : reverse('certificate_app:certificate_upload',args=pk)
    }
    return JsonResponse(data)


@login_required
@is_admin
def change_status(request, pk):
    value = request.GET.get('status')
    try:
        report = get_object_or_404(User, id=pk).report
    except:
        return JsonResponse({'message': 'intern has not report submitted'}, status=404)
    report.status = value
    report.save()
    data = {
        'message': f'status changed to {value} successfully',
        'status': value
    }
    return JsonResponse(data)

@login_required
@is_admin
def change_personaldetail_update(request, pk):
    value = request.GET.get('status')
    try:
        detail = get_object_or_404(User, id=pk).personaldetail
    except:
        return JsonResponse({'message': 'intern has no personal details'},status=404)
    detail.is_editable = value
    detail.request_edit = False
    detail.edit_reason = ""
    detail.save()
    return JsonResponse({'message':'request status change successfully'})

@login_required
@is_admin
def change_project_update(request, pk):
    value = request.GET.get('status')
    try:
        project = get_object_or_404(User, id=pk).project
    except:
        return JsonResponse({'message': 'intern has no project details'},status=404)
    project.is_editable = value
    project.request_edit = False
    project.edit_reason = ""
    project.save()
    return JsonResponse({'message':'request status change successfully'})

@login_required
@is_admin
def iframe(request,pk):
    user = get_object_or_404(User,id=pk)
    context = {
        'user' : user,
        'project' : user.project,
        'report' : user.report,
        'details' : user.personaldetail
    }
    # return render(request,'admin/interniframe.html',context=context)
    return render_to_response('admin/interniframe.html',context=context)


@login_required
@is_admin
def certificateconfig(request):
    if request.method == 'POST':
        ckt = request.FILES.get('ckt')
        logo = request.FILES.get('logo')
        sign = request.FILES.get('sign')

        logol = request.POST['logol']
        logow = request.POST['logow']
        logox = request.POST['logox']
        logoy = request.POST['logoy']

        signl = request.POST['signl']
        signw = request.POST['signw']
        signx = request.POST['signx']
        signy = request.POST['signy']

        internamex = request.POST['internamex']
        internamey = request.POST['internamey']
        internnames = request.POST['internames']
        interntypex = request.POST['interntypex']
        interntypey = request.POST['interntypey']
        interntypes = request.POST['interntypes']
        profilex = request.POST['profilex']
        profiley = request.POST['profiley']
        profiles = request.POST['profiles']
        d1x = request.POST['d1x']
        d1y = request.POST['d1y']
        d1s = request.POST['d1s']
        d2x = request.POST['d2x']
        d2y = request.POST['d2y']
        d2s = request.POST['d2s']
        datex = request.POST['datex']
        datey = request.POST['datey']
        dates = request.POST['dates']
        renox = request.POST['renox']
        renoy = request.POST['renoy']
        renos = request.POST['renos']
        c = CertificateConfig(
            certificate_img = ckt,
            logo_img = logo,
            sign_img = sign,

            logox = logox,
            logoy = logoy,
            logol = logol,
            logow = logow,
            signx = signx,
            signy = signy,
            signl = signl,
            signw = signw,
            namex = internamex,
            namey = internamey,
            profilex = profilex,
            profiley = profiley,
            typex = interntypex,
            typey = interntypey,
            d1x = d1x,
            d1y = d1y,
            d2x = d2x,
            d2y = d2y,
            datex = datex,
            datey = datey,
            renox = renox,
            renoy = renoy,
            namesize = internnames,
            typesize = interntypes,
            profilesize = profiles,
            datesize = dates,
            dsize = d1s
        )
        c.save()
        messages.success(request,'Certificate configured successfully')
        return redirect('certificate_app:mentor')
    return render(request,'admin/certificate.html')


def upload_certificate(request,pk):
    if request.method == 'POST':
        user = get_object_or_404(User,id=pk)
        c = Certificate(
            user = user,
            certificate_pdf = request.FILES.get('ckt_pdf'),
            certificate_png = request.FILES.get('ckt_img')
        )
        c.save()
        delurl= reverse('certificate_app:delete_certificate',args=pk)
        pdfurl = c.certificate_pdf.url
        pngurl = c.certificate_png.url
        cktno = c.certificate_number
        return HttpResponse('<script>opener.closePopup(window,"{}","{}","{}","{}","{}");</script>'.format(pk,delurl,pdfurl,pngurl,cktno))
        # print(request.FILES.get('ckt_pdf'),request.FILES.get('ckt_png'))
    return render(request,'admin/certificate_upload.html')

