import unittest

from app import app


class ContactRouteTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_contact_route_returns_success_payload(self):
        response = self.client.post(
            '/contact',
            json={
                'name': 'Alice',
                'email': 'alice@example.com',
                'message': 'Hello from the portfolio form.'
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('whatsappUrl', data)
        self.assertIn('mailtoUrl', data)


if __name__ == '__main__':
    unittest.main()
