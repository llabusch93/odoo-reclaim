from odoo import api, fields, models


class ReclaimTaskEvent(models.Model):
    """
    Model to store and sync Reclaim.ai task events.
    """

    _name = "reclaim.task.event"
    _description = "Reclaim.ai Task Event"

    reclaim_id = fields.Char(
        string="Reclaim.ai ID",
        help="ID of the event in Reclaim.ai",
        required=True,
    )

    task_id = fields.Many2one(
        comodel_name="reclaim.task",
        string="Task",
        help="Task of the event",
        required=True,
    )

    start_time = fields.Datetime(
        string="Start Time",
        help="Start time of the event",
    )

    end_time = fields.Datetime(
        string="End Time",
        help="End time of the event",
    )
