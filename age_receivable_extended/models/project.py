from odoo import models, fields, api, _

class project_project(models.Model):
    _inherit = "project.project"
    
    
    project_age_receivable_lines = fields.One2many('project.age.receivable','project_id',string="Age Receivable")
