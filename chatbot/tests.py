from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Chat  # Adjust if in different app


class ChatViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.chat_url = reverse('chat')  # Replace with your actual URL name

    def test_get_chat_page_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat_template.html')  # Replace with your actual template

    def test_post_message_returns_json_response(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.chat_url, {
            'message': 'Hello chatbot',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # Mimic AJAX call

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('response', response.json())
        self.assertTrue(len(response.json()['response']) > 0)

    def test_chat_message_saved_in_db(self):
        self.client.login(username='testuser', password='testpass')
        self.client.post(self.chat_url, {
            'message': 'Hello world',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        chat_entry = Chat.objects.last()
        self.assertEqual(chat_entry.user, self.user)
        self.assertEqual(chat_entry.message, 'Hello world')
        self.assertIsNotNone(chat_entry.response)

    def test_unauthenticated_user_redirected(self):
        response = self.client.get(self.chat_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn(response.status_code, [302, 403])
