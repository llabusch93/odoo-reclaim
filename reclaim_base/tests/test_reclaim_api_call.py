from odoo.tests.common import TransactionCase, tagged
from os import environ


@tagged("post_install", "-at_install")
class TestReclaimApiCall(TransactionCase):
    def test_reclaim_api_call(self):
        """
        Tests if the API call is successful, but only if the token
        is provided in the environment variable RECLAIM_TOKEN.
        """
        token = environ.get("RECLAIM_TOKEN")
        if token:
            user = self.env["res.users"].create(
                {
                    "name": "Test User",
                    "login": "test_user",
                    "reclaim_token": token,
                }
            )

            self.assertEqual(user.reclaim_state, "connection_success")

        else:
            self.skipTest(
                "No token provided in RECLAIM_TOKEN environment variable"
            )
