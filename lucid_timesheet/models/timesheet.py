# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    type = fields.Selection([('project','Project')
                            ,('proposal','Proposal')
                            ,('leave','Leave')
                            ,('internal','Internal')],string="Type")
    proposal = fields.Many2one('crm.lead',string="Proposal",domain="[('proposal_team','=',employee_id)]")
    project_manager = fields.Many2one('res.users',string="Project Manager",readonly=True)
    project_id = fields.Many2one(group_expand="_group_expand_project_ids",domain="[('allow_timesheets','=',True),('proposal_team','=',employee_id)]")

    @api.onchange('project_id')
    def onchange_project_id(self):
        for rec in self:
            if rec.project_id:
                rec.project_manager = rec.project_id.user_id.id

class HrExpense(models.Model):

    _inherit = 'hr.expense'

    project_id = fields.Many2one('project.project', string = 'Project')
    related_project_id = fields.Many2one('project.project', string='Projects',readonly=True)
    task_id = fields.Many2one('project.task', string='Task')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Proposal/Project', 
                            related='project_id.analytic_account_id', store= True,
                            states={'post': [('readonly', True)], 'done': [('readonly', True)]}, oldname='analytic_account')

    category_id = fields.Many2one('product.category',string="Expense Type")

    @api.onchange('analytic_account_id')
    def onchange_account_analytic_id(self):
        if self.analytic_account_id:
            if self.analytic_account_id.project_id:
                self.related_project_id = self.analytic_account_id.project_id.id
    
class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    project_manager = fields.Many2one('res.users', related="project_id.user_id", store=True)
    project_id = fields.Many2one('project.project')