from odoo import api, Command, fields, models, tools, SUPERUSER_ID, _

STATUS_COLOR = {
    'on_track': 20,  # green / success
    'at_risk': 2,  # orange
    'off_track': 23,  # red / danger
    'on_hold': 4,  # light blue
    False: 0,  # default grey -- for studio
}
class Project(models.Model):
    _inherit = "project.project"
    
    @api.depends('last_update_status')
    def _compute_last_update_color(self):
        for project in self:
            print('::::::::::::::::::::',project.last_update_status)
            if project.last_update_status == 'to_define':
                project.last_update_color = STATUS_COLOR['on_track']
            else:
                project.last_update_color = STATUS_COLOR[project.last_update_status]