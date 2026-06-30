from functools import wraps

from django.shortcuts import redirect


def get_user_profile(user):
    try:
        return user.profile
    except Exception:
        return None


def get_current_business(request):
    if not request.user.is_authenticated:
        return None

    profile = get_user_profile(request.user)

    if profile and profile.business:
        return profile.business

    return None


def is_platform_admin(request):
    if not request.user.is_authenticated:
        return False

    profile = get_user_profile(request.user)

    return request.user.is_superuser or (
        profile and profile.role == 'SuperAdmin'
    )


def super_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        if is_platform_admin(request):
            return view_func(request, *args, **kwargs)

        return redirect('/dashboard/')

    return wrapper


def business_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        profile = get_user_profile(request.user)

        if profile and profile.role == 'BusinessAdmin' and profile.business:
            return view_func(request, *args, **kwargs)

        if profile and profile.role == 'Customer':
            return redirect('/customer-portal/')

        return redirect('/accounts/login/')

    return wrapper