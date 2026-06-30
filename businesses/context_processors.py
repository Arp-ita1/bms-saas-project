def business_context(request):
    current_business = None
    current_role = None
    current_plan = None

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            current_role = profile.role
            current_business = profile.business

            if current_business:
                try:
                    current_plan = current_business.subscription.plan
                except Exception:
                    current_plan = None

        except Exception:
            current_role = 'Admin' if request.user.is_staff or request.user.is_superuser else 'User'

    return {
        'current_business': current_business,
        'current_role': current_role,
        'current_plan': current_plan,
    }