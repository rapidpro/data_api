import json
from unittest import skip
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from mock import patch
from rest_framework.test import APIClient
from temba_client.tests import TembaTest, MockResponse
from temba_client.v2 import TembaClient
import uuid

from data_api.api.exceptions import ImportRunningException
from data_api.api.tests.test_utils import get_api_results_from_file
from data_api.api.models import LastSaved
from data_api.api.tasks import fetch_entity
from data_api.staging.models import Organization, Group, SyncCheckpoint, Channel, Contact, ChannelEvent, Field, \
    Broadcast
from data_api.staging.utils import import_org_with_client


@patch('temba_client.clients.request')
class DataImportTest(TembaTest):
    # this class heavily inspired by temba_client.v2.tests.TembaClientTest

    @classmethod
    def setUpClass(cls):
        cls.api_token = uuid.uuid4().hex
        cls.client = TembaClient('example.com', '1234567890', user_agent='test/0.1')
        cls.org = Organization.objects.create(
            name='test org', api_token=cls.api_token,
        )
        # for API tests
        username = 'unicef'
        password = '4thekids'
        cls.user = User.objects.create_user(
            username=username, email='rapidpro@unicef.org', password=password, is_superuser=True
        )
        cls.client = APIClient()
        cls.client.login(username=username, password=password)

    def tearDown(self):
        pass
        # Boundary.objects.all().delete()
        # Broadcast.objects.all().delete()
        # Campaign.objects.all().delete()
        # CampaignEvent.objects.all().delete()
        Channel.objects.all().delete()
        ChannelEvent.objects.all().delete()
        Contact.objects.all().delete()
        Group.objects.all().delete()
        # Flow.objects.all().delete()
        # FlowStart.objects.all().delete()
        # Label.objects.all().delete()
        # Message.objects.all().delete()
        # Run.objects.all().delete()
        # Resthook.objects.all().delete()
        # ResthookEvent.objects.all().delete()
        # ResthookSubscriber.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        Organization.objects.all().delete()

    def _run_import_test(self, mock_request, obj_class):
        api_results_text = get_api_results_from_file(obj_class.get_collection_name())
        api_results = json.loads(api_results_text)
        mock_request.return_value = MockResponse(200, api_results_text)
        before = timezone.now()
        objs_made = fetch_entity(obj_class, self.org, return_objs=True)
        after = timezone.now()
        for obj in objs_made:
            self.assertTrue(isinstance(obj, obj_class))
            self.assertEqual(self.org, obj.organization)
            self.assertTrue(before <= obj.first_synced <= after)
            self.assertTrue(before <= obj.last_synced <= after)

        # check last saved
        checkpoint = SyncCheckpoint.objects.get(organization=self.org,
                                                collection_name=obj_class.get_collection_name())
        self.assertIsNotNone(checkpoint.last_saved)
        self.assertEqual(checkpoint.last_saved, checkpoint.last_started)
        self.assertFalse(checkpoint.is_running)
        return api_results['results'], objs_made

    def _run_api_test(self, obj_class):
        # assumes run after an import has been done
        collection_name = obj_class.get_collection_name()
        rapidpro_api_results = json.loads(get_api_results_from_file(collection_name))['results']
        # todo: should ideally not hard-code urls like this
        warehouse_api_results = self.client.get('/api/v3/{}/org/{}/'.format(collection_name,
                                                                            str(self.org.id))).json()
        self.assertEqual(
            len(rapidpro_api_results),
            len(warehouse_api_results),
            'API result lenghts were different: \nRapidPRO\n{}\nWarehouse\n{}'.format(
                json.dumps(rapidpro_api_results, indent=2),
                json.dumps(warehouse_api_results, indent=2)
            )
        )
        sort_field = _get_sort_field(rapidpro_api_results[0])
        sorted_results = sorted(rapidpro_api_results, key=lambda x: x[sort_field])
        sorted_warehouse_results = sorted(warehouse_api_results, key=lambda x: x[sort_field])
        for i, rapidpro_result in enumerate(sorted_results):
            self.assertApiObjectsEquivalent(rapidpro_result, sorted_warehouse_results[i])

    def assertApiObjectsEquivalent(self, rapidpro_result, warehouse_api_result):
        IGNORE_KEYS = {'id'}
        IGNORE_TYPES = (list, dict)  # todo: probably want to test these eventually
        for key in rapidpro_result:
            rapidpro_value = rapidpro_result[key]
            if key in IGNORE_KEYS:
                continue
            # todo: should switch this back to failing if key not found once dicts and lists are supported
            warehouse_value = warehouse_api_result.get(key, None)
            if not isinstance(rapidpro_value, IGNORE_TYPES) and not isinstance(warehouse_value, IGNORE_TYPES):
                warehouse_value = warehouse_api_result[key]
                self.assertEqual(
                    _massage_data(rapidpro_value),
                    _massage_data(warehouse_value),
                    '{} was not the same (expected {}, got {})'.format(
                        key, rapidpro_value, warehouse_value
                    )
                )

    def test_import_org(self, mock_request):
        api_results_text = get_api_results_from_file('org')
        api_results = json.loads(api_results_text)
        mock_request.return_value = MockResponse(200, api_results_text)
        api_key = 'token'
        self.assertEqual(0, Organization.objects.filter(api_token=api_key).count())
        client = TembaClient('host', api_key)
        org = import_org_with_client(client, 'host', api_key)
        self.assertEqual(api_key, org.api_token)
        self.assertEqual(org.name, api_results['name'])
        self.assertEqual(1, Organization.objects.filter(api_token=api_key).count())

        # modify in place and confirm it updates instead of creating a new org
        new_name = 'Updated Name'
        api_results['name'] = new_name
        mock_request.return_value = MockResponse(200, json.dumps(api_results))
        second_org = import_org_with_client(client, 'host', api_key)
        self.assertEqual(second_org.id, org.id)
        self.assertEqual(1, Organization.objects.filter(api_token=api_key).count())
        self.assertEqual(new_name, second_org.name)

    # def test_import_boundaries(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, Boundary)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.name, api_results[i]['name'])
    #     self._run_api_test(Boundary)
    #
    def test_import_broadcasts(self, mock_request):
        Contact(
            organization=self.org,
            uuid='5079cb96-a1d8-4f47-8c87-d8c7bb6ddab9',
            created_on=datetime.now(),
            modified_on=datetime.now(),
        ).save()
        Group(
            organization=self.org,
            uuid='04a4752b-0f49-480e-ae60-3a3f2bea485c',
            count=1,
        ).save()
        api_results, objs_made = self._run_import_test(mock_request, Broadcast)
        self.assertEqual(2, len(objs_made))
        for i, obj in enumerate(objs_made):
            self.assertEqual(obj.text, api_results[i]['text'])
        self._run_api_test(Broadcast)

    # def test_import_campaigns(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, Campaign)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.name, api_results[i]['name'])
    #     self._run_api_test(Campaign)
    #
    # def test_import_campaign_events(self, mock_request):
    #     Campaign(org_id=str(self.org.id), uuid='9ccae91f-b3f8-4c18-ad92-e795a2332c11').save()
    #     api_results, objs_made = self._run_import_test(mock_request, CampaignEvent)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.message, api_results[i]['message'])
    #     self._run_api_test(CampaignEvent)
    #
    def test_import_channels(self, mock_request):
        api_results, objs_made = self._run_import_test(mock_request, Channel)
        self.assertEqual(2, len(objs_made))
        for i, obj in enumerate(objs_made):
            self.assertEqual(obj.name, api_results[i]['name'])
        self._run_api_test(Channel)

    def test_import_channel_events(self, mock_request):
        Channel(
            organization=self.org,
            uuid='9a8b001e-a913-486c-80f4-1356e23f582e',
            last_seen=datetime.now(),
            created_on=datetime.now(),
        ).save()
        Contact(
            organization=self.org,
            uuid='d33e9ad5-5c35-414c-abd4-e7451c69ff1d',
            created_on=datetime.now(),
            modified_on=datetime.now(),
        ).save()
        api_results, objs_made = self._run_import_test(mock_request, ChannelEvent)
        self.assertEqual(2, len(objs_made))
        for i, obj in enumerate(objs_made):
            self.assertEqual(obj.rapidpro_id, api_results[i]['id'])
        self._run_api_test(ChannelEvent)

    def test_import_contacts(self, mock_request):
        # todo: find a more generic way to bootstrap related models
        Group(
            organization=self.org,
            uuid='d29eca7c-a475-4d8d-98ca-bff968341356',
            count=1,
        ).save()
        api_results, objs_made = self._run_import_test(mock_request, Contact)
        self.assertEqual(3, len(objs_made))
        for i, obj in enumerate(objs_made):
            self.assertEqual(obj.name, api_results[i]['name'])
        self._run_api_test(Contact)

    def test_import_fields(self, mock_request):
        api_results, objs_made = self._run_import_test(mock_request, Field)
        self.assertEqual(2, len(objs_made))
        for i, obj in enumerate(objs_made):
            self.assertEqual(obj.key, api_results[i]['key'])
        self._run_api_test(Field)

    # @skip('import currently succeeds on bad object references because errors are swallowed')
    # def test_import_fails_if_no_related_object(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, FlowStart)
    #     self.assertEqual(0, len(objs_made))
    #
    # def test_import_flow_starts(self, mock_request):
    #     Flow(org_id=str(self.org.id), uuid='f5901b62-ba76-4003-9c62-72fdacc1b7b7', name='Registration').save()
    #     Flow(org_id=str(self.org.id), uuid='f5901b62-ba76-4003-9c62-72fdacc1b7b8', name='Thrift Shop').save()
    #     api_results, objs_made = self._run_import_test(mock_request, FlowStart)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.flow.name, api_results[i]['flow']['name'])
    #     self._run_api_test(FlowStart)
    #
    # def test_import_flows(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, Flow)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.name, api_results[i]['name'])
    #     self._run_api_test(Flow)
    #
    def test_import_groups(self, mock_request):
        api_results, objs_made = self._run_import_test(mock_request, Group)
        self.assertEqual(2, len(objs_made))
        for i, obj in enumerate(objs_made):
            self.assertEqual(obj.name, api_results[i]['name'])
        self._run_api_test(Group)

    # def test_import_labels(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, Label)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.name, api_results[i]['name'])
    #     self._run_api_test(Label)
    #
    # def test_import_messages(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, Message)
    #     self.assertEqual(12, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.text, api_results[i % 2]['text'])
    #     # todo: this is broken due to the custom way messages are imported not playing nice with mocks
    #     # self._run_api_test(Message)
    #
    # def test_import_runs(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, Run)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.tid, api_results[i]['id'])
    #     self._run_api_test(Run)
    #
    # def test_import_resthooks(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, Resthook)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.resthook, api_results[i]['resthook'])
    #     self._run_api_test(Resthook)
    #
    # def test_import_resthook_events(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, ResthookEvent)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.resthook, api_results[i]['resthook'])
    #     self._run_api_test(ResthookEvent)
    #
    # def test_import_resthook_subscribers(self, mock_request):
    #     api_results, objs_made = self._run_import_test(mock_request, ResthookSubscriber)
    #     self.assertEqual(2, len(objs_made))
    #     for i, obj in enumerate(objs_made):
    #         self.assertEqual(obj.resthook, api_results[i]['resthook'])
    #     self._run_api_test(ResthookSubscriber)
    #
    # def test_disallow_import_if_running(self, mock_request):
    #     ls = LastSaved.create_for_org_and_collection(self.org, ResthookSubscriber)
    #     ls.is_running = True
    #     ls.save()
    #     with self.assertRaises(ImportRunningException):
    #         self._run_import_test(mock_request, ResthookSubscriber)
    #     ls.delete()


def _get_sort_field(rapidpro_api_object):
    for field in ['uuid', 'id']:
        if field in rapidpro_api_object:
            return field
    return rapidpro_api_object.keys()[0]


def _massage_data(value):
    if _looks_like_a_date_string(value):
        # mongo strips microseconds so we have to as well.
        # todo: This could be drastically improved.
        return value[:23]
    return value


def _looks_like_a_date_string(value):
    # todo: can make this more advanced as needed
    return isinstance(value, basestring) and value.endswith('Z') and (len(value) == 27 or len(value) == 24)
