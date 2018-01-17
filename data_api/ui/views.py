from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
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
        'feedback': feedback
    })