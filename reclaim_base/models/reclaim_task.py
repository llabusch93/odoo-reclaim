from odoo import api, fields, models


class ReclaimTask(models.Model):
    """
    Model to store and sync Reclaim.ai tasks.
    """

    _name = "reclaim.task"
    _description = "Reclaim.ai Task"

    name = fields.Char(
        string="Name",
        help="Name of the task",
        required=True,
    )

    reclaim_id = fields.Char(
        string="Reclaim.ai ID",
        help="ID of the task in Reclaim.ai",
        required=True,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        help="Owner of the task",
        required=True,
    )

    duration = fields.Float(
        string="Duration",
        help="Duration of the task in hours",
    )

    start_time = fields.Datetime(
        string="Start Time",
        help="Start time of the task",
    )

    due_time = fields.Datetime(
        string="Due Time",
        help="Due time of the task",
    )

    event_ids = fields.One2many(
        comodel_name="reclaim.task.event",
        inverse_name="task_id",
        string="Scheduled Events",
        help="Scheduled events of the task",
    )

    scheduled_start_time = fields.Datetime(
        string="Scheduled Start Time",
        help="Scheduled start time of the task",
        compute="_compute_state_and_schedule",
    )

    scheduled_end_time = fields.Datetime(
        string="Scheduled End Time",
        help="Scheduled end time of the task",
        compute="_compute_state_and_schedule",
    )

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("scheduled", "Scheduled"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ],
        string="State",
        help="State of the task",
        compute="_compute_state_and_schedule",
    )

    @api.depends("events")
    def _compute_state_and_schedule(self):
        """
        Compute the state and schedule of the task.
        """
        for task in self:
            if not task.event_ids:
                task.state = "new"
                task.scheduled_start_time = False
                task.scheduled_end_time = False
            else:
                task.state = "scheduled"
                task.scheduled_start_time = task.event_ids[0].start_time
                task.scheduled_end_time = task.event_ids[-1].end_time
