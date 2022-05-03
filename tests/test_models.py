from rest_framework.test import APITestCase

from main.models import Client, MobileOperator, GroupClients

class TestClient(APITestCase):
    def setUp(self) -> None:
        self.test_mobile_operator = MobileOperator(code="920", name="test_mobile_operator")
        self.test_group_clients = GroupClients(tag="test_group", name='group for testing')
        self.test_phone_number = '79000000000'

    def test_create_new_client(self):
        count_clients = Client.objects.count()
        try:
            client = Client.objects.get(phone_number=self.test_phone_numberphone_number)
        except Client.DoesNotExist:
            client = Client.objects.create(phone_number=self.test_phone_number, mobile_operator=self.test_mobile_operator,
                                           tag=self.test_group_clients, timezone='UTC')
            count_clients_after_create = Client.objects.count()
            self.assertEqual(count_clients+1, count_clients_after_create)

