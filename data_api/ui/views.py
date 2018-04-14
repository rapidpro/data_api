from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_POST

from data_api.api.models import LastSaved
from data_api.api.utils import import_org
from data_api.ui.forms import OrgForm


@user_passes_test(lambda u: u.is_superuser)
def import_org_view(request):
    form = OrgForm()
    feedback = ''
    if request.method == 'POST':
        post_form = OrgForm(request.POST)
        if post_form.is_valid():
            api_key = post_form.cleaned_data['api_key']
            server = post_form.cleaned_data['server']
            try:
                org = import_org(server, api_key)
                feedback = 'Successfully imported API key for <strong>{}</strong>. Data will show up within 24 hours.'.format(
                    org.name,
                )
            except Exception as e:
                feedback = 'Sorry, there was a problem importing the org. Details: <strong>{}</strong>'.format(e)
        else:
            form = post_form  # errors will show here

    return render(request, 'ui/import_org.html', {
        'form': form,
        'feedback': feedback,
        'page_title': 'RapidPro: Import Organization',
    })


@user_passes_test(lambda u: u.is_superuser)
def import_status(request):
    pending_runs = LastSaved.objects.filter(is_running=True).order_by('last_started')
    return render(request, 'ui/import_status.html', {
        'pending_runs': pending_runs,
        'page_title': 'RapidPro: Import Status Page',
    })


@user_passes_test(lambda u: u.is_superuser)
@require_POST
def mark_completed(request, last_saved_id):
    ls = LastSaved.objects.get(id=last_saved_id)
    assert ls.last_saved is None
    ls.is_running = False
    ls.save()
    return HttpResponseRedirect(reverse('import_status'))
