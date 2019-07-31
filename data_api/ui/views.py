from abc import ABCMeta

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from temba_client.v2 import TembaClient

from data_api.staging.tasks import import_org_with_client, sync_latest_data
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
                client = TembaClient(server, api_key)
                org = import_org_with_client(client, server, api_key)
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


class BasicTaskAPIView(APIView, metaclass=ABCMeta):
    task_function = None
    success_message = 'Task generated Successfully'

    def get(self, request, *args, **kwargs):
        try:
            self.task_function.delay()
        except BaseException as e:
            return Response(status=500, data=str(e))

        return Response({'success': self.success_message})


class SyncLastestData(BasicTaskAPIView):
    task_function = sync_latest_data
    success_message = 'Task generated Successfully: Sync All Users'
