from functools import wraps

from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        if request.user.is_superuser or request.user.is_staff:
            return view_func(request, *args, **kwargs)

        try:
            profile = request.user.profile
        except Exception:
            profile = None

        if profile and profile.role == 'BusinessAdmin' and profile.business:
            return view_func(request, *args, **kwargs)

        if profile and profile.role == 'Customer':
            return redirect('/customer-portal/')

        return redirect('/accounts/login/')

    return wrapper