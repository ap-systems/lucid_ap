# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class AccountAnalyticLine(models.Model):

	_inherit = 'account.analytic.line'

	type = fields.Selection([('project','Project')
							,('proposal','Proposal')
							,('leave','Leave')
							,('internal','Internal')],string="Type")
	proposal = fields.Many2one('proposal.list',string="Proposal")
	project_manager = fields.Many2one('res.users',string="Project Manager",readonly=True)
	employee_id = fields.Many2one('hr.employee',string="Employee")

	@api.onchange('project_id')
	def onchange_project_id(self):
		for rec in self:
			if rec.project_id:
				rec.project_manager = rec.project_id.user_id.id

class HrExpense(models.Model):

	_inherit = 'hr.expense'

	proposal_id = fields.Many2one('proposal.list',string="Proposal/Project")
	project_id = fields.Many2one('project.project',string="Projects")
	task_id = fields.Many2one('project.task', domain="[('project_id','=?',project_id)]")
	category_id = fields.Many2one('product.category',string="Expense Type")

