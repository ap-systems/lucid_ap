from odoo import api, Command, fields, models, tools, SUPERUSER_ID, _

STATUS_COLOR = {
    'on_track': 20,  # green / success
    'at_risk': 2,  # orange
    'off_track': 23,  # red / danger
    'on_hold': 4,  # light blue
    False: 0,  # default grey -- for studio
}

class ProjectReportWizard(models.TransientModel):
    _name = 'project.report.wizard'
    _description = 'Project Report Wizard'

    project_id = fields.Many2one('project.project', required=True)
    report_type = fields.Selection([
        ('burndown', 'Burndown Chart'), ('project_update', 'Project Update')
    ], string='Report Type', required=True, default='burndown')

    def action_burndown_report_view(self):
        action = self.env['ir.actions.act_window']._for_xml_id('project.action_project_task_burndown_chart_report')
        action['context'] = {'search_default_project_id': self.project_id.id}
        return action

    def action_project_update_report_view(self):
        action = self.env['ir.actions.act_window']._for_xml_id('project.project_update_all_action')
        action['context'] = {'active_id': self.project_id.id, 'search_default_project_id': self.project_id.id}
        return action

class Project(models.Model):
    _inherit = "project.project"
    
    
    def get_last_update_or_default(self):
        self.ensure_one()
        if self.last_update_status == 'to_define':
                last_update_status = 'on_track'
        else:
            last_update_status = self.last_update_status
        labels = dict(self._fields['last_update_status']._description_selection(self.env))
        return {
            'status': labels[last_update_status],
            'color': self.last_update_color,
        }
        
    @api.depends('last_update_status')
    def _compute_last_update_color(self):
        for project in self:
            print('::::::::::::::::::::',project.last_update_status)
            if project.last_update_status == 'to_define':
                project.last_update_color = STATUS_COLOR['on_track']
            else:
                project.last_update_color = STATUS_COLOR[project.last_update_status]