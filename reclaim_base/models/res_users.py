from odoo import api, fields, models
from reclaim_sdk.client import ReclaimClient, ReclaimAPICall


class ResUsers(models.Model):
    _inherit = "res.users"

    reclaim_token = fields.Char(
        string="Reclaim.ai Token",
        help="Token for Reclaim.ai",
    )

    reclaim_state = fields.Selection(
        selection=[
            ("no_token", "No Token Provided"),
            ("connection_success", "Connection successful"),
            ("connection_failed", "Connection failed"),
        ],
        string="Reclaim.ai Connection State",
        help="State of the connection to Reclaim.ai",
        compute="_compute_reclaim_state",
    )

    def _check_reclaim_connection(self):
        """
        Checks if the connection to Reclaim.ai is successful.
        """
        client = ReclaimClient(self.reclaim_token)
        try:
            res = client.get("/api/accounts/main")
            res.raise_for_status()
            return True
        except Exception:
            return False

    @api.depends("reclaim_token")
    def _compute_reclaim_state(self):
        for user in self:
            if user.reclaim_token:
                if user._check_reclaim_connection():
                    user.reclaim_state = "connection_success"
                else:
                    user.reclaim_state = "connection_failed"
            else:
                user.reclaim_state = "no_token"
