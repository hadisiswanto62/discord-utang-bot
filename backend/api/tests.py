from django.test import TestCase
from rest_framework.test import APIClient

DEFAULT_USERNAME = 'user1'
DEFAULT_FIRSTNAME = "user1"
DEFAULT_DISCORD_ID = 123
DEFAULT_PASSWORD = 'password123'

DEFAULT_TX_GROUP_DESC = "some description"

URL_USER = "/api/user/"
URL_TX_GROUP = "/api/transaction_group/"
URL_TX = "/api/transaction/"

def create_user(client, username=None, first_name=None, discord_id=None):
    username = username if username is not None else DEFAULT_USERNAME
    first_name = first_name if first_name is not None else DEFAULT_FIRSTNAME
    discord_id = discord_id if discord_id is not None else DEFAULT_DISCORD_ID
    payload = {"username": username, "first_name": first_name, "discord_id":discord_id, "password":DEFAULT_PASSWORD}
    return client.post(URL_USER, data=payload)

def create_transaction_group(client, desc=None):
    desc = desc if desc is not None else DEFAULT_TX_GROUP_DESC
    return client.post(URL_TX_GROUP, data={"desc": desc})

class UserModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # self.user = User.objects.create_user(
        #     username=self.DEFAULT_USERNAME,
        #     password=self.DEFAULT_PASSWORD
        # )
        # self.client.login(
        #     username=self.DEFAULT_USERNAME,
        #     password=self.DEFAULT_PASSWORD
        # )

    def test_create_user(self):
        response = create_user(self.client)
        self.assertEqual(response.data["username"], DEFAULT_USERNAME)
        self.assertEqual(response.data["first_name"], DEFAULT_FIRSTNAME)
        self.assertEqual(response.data["discord_id"], DEFAULT_DISCORD_ID)
        self.assertEqual(response.data["id"], 1)

    def test_get_user_list(self):
        create_user(self.client)
        response = self.client.get(URL_USER)
        self.assertEqual(response.data[0]["username"], DEFAULT_USERNAME)
        self.assertEqual(response.data[0]["first_name"], DEFAULT_FIRSTNAME)
        self.assertEqual(response.data[0]["discord_id"], DEFAULT_DISCORD_ID)
        self.assertEqual(response.data[0]["id"], 1)

class TransactionGroupTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        create_user(self.client)
        x = self.client.login(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)

    def test_create_transaction_group(self):
        response = create_transaction_group(self.client)
        self.assertEqual(response.data["desc"], DEFAULT_TX_GROUP_DESC)
        self.assertEqual(response.data["receiver"]["id"], 1)
        self.assertEqual(response.data["id"], 1)

class TransactionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        create_user(self.client, "user1")
        create_user(self.client, username="user2")
        create_user(self.client, username="user2")
        x = self.client.login(username="user1", password=DEFAULT_PASSWORD)
        create_transaction_group(self.client, desc="txg1")
        create_transaction_group(self.client, desc="txg2")
        create_transaction_group(self.client, desc="txg3")

    def test_create_transaction(self):
        payload = {"sender_id":2, "tx_group_id":1, "amount":123.0}
        response = self.client.post(URL_TX, data=payload)
        self.assertEqual(response.data["sender"]["username"], "user2")
        self.assertEqual(response.data["receiver"]["username"], "user1")
        self.assertEqual(response.data["group"]["desc"], DEFAULT_TX_GROUP_DESC)
        self.assertEqual(response.data["is_paid"], False)
        self.assertEqual(response.data["amount"], 123.0)
        self.assertEqual(response.data["id"], 1)
