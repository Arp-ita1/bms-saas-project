from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return '/platform/'

        try:
            profile = user.profile
        except Exception:
            profile = None

        if profile:
            if profile.role == 'SuperAdmin':
                return '/platform/'

            if profile.role == 'BusinessAdmin':
                return '/dashboard/'

            if profile.role == 'Employee':
                return '/employee-portal/'

            if profile.role == 'Customer':
                return '/customer-portal/'

        return '/dashboard/'


class CustomLogoutView(LogoutView):
    next_page = '/'


def register_view(request):
    messages.info(request, 'Please choose a pricing plan to create a business account.')
    return redirect('/pricing/')