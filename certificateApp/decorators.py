from django.shortcuts import redirect, reverse
from .models import UserProfile
from django.core.exceptions import PermissionDenied


def is_admin(fun):
    def authorized(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_irscdmin:
                return fun(request, *args, **kwargs)
            else:
                return redirect(reverse('certificate_app:register'))
        else:
            return redirect(reverse("certificate_app:login"))

    return authorized


def is_intern(fun):
    def authorized(request, *args, **kwargs):
        if UserProfile.objects.all().filter(user=request.user).first():
            if not request.user.is_superuser or request.user.is_irscdmin:
                return fun(request, *args, **kwargs)
            else:
                return redirect(reverse('certificate_app:login'))
        else:
            return redirect(reverse("certificate_app:login"))

    return authorized

def is_personaldetail_editable(fun):
    def authorized(request,*args, **kwargs):
        if request.user.personaldetail.is_editable == 'A':
            return fun(request,*args, **kwargs)
        return redirect('certificate_app:personal_detail')
    return authorized

def is_project_editable(fun):
    def authorized(request,*args, **kwargs):
        if request.user.project.is_editable == 'A':
            return fun(request,*args, **kwargs)
        return redirect('certificate_app:project')
    return authorized

def is_report_editable(fun):
    def authorized(request,*args, **kwargs):
        if request.user.report.status == 'R':
            return fun(request,*args, **kwargs)
        return redirect('certificate_app:report')
    return authorized
