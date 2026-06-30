from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.decorators import admin_required
from activity_logs.utils import log_activity
from businesses.utils import get_current_business

from .forms import BusinessProfileForm
from .models import BusinessProfile


@admin_required
def settings_page(request):
    business = get_current_business(request)
    profile = BusinessProfile.get_profile(business)

    form = BusinessProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.business = profile.business or business
        profile.save()

        log_activity(request.user, 'Updated business settings', 'Business Settings')
        messages.success(request, 'Business settings updated successfully.')
        return redirect('/business-settings/')

    return render(request, 'business_settings/settings_page.html', {
        'form': form,
        'business': business,
    })