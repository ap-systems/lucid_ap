from odoo import api, fields, models, tools



class ProjectProject(models.Model):
    _inherit = 'project.project'
     
    
    prj_revenue = fields.Float(string='Revenue', compute='_compute_budget_prj',store=False, track_visibility='onchange')
    prj_disbursement = fields.Float(string='Cost', compute='_compute_budget_prj',store=False, track_visibility='onchange')
    prj_labour = fields.Float(string='Labour Cost')
    prj_gross_profit = fields.Float(string='Gross Margin',store=False, compute='_compute_pm_grosss_margin_prjct',track_visibility='onchange')
    ap_invoice_ids = fields.One2many('account.move', 'project_id', string='Invoice', track_visibility='onchange')
    percent = fields.Char(default="%")
    prj_revenue_progress = fields.Integer(string='Revenue',compute='_compute_revenue_progress')
    prj_cost = fields.Integer(string='Cost',compute='_compute_prj_cost')
    actual_disbursement_cost = fields.Float(string='Cost',compute="_compute_actual_disbursement_cost")
    actual_labour_cost = fields.Float(string='A.Labour Cost')
    actual_revenue_cost = fields.Float(string="Revenue",compute="_compute_actual_revenue_cost")

    def _compute_actual_disbursement_cost(self):
        for rec in self:
            tot_dis_cost = 0.0
            for line in self.env['account.analytic.line'].search([('project_id','=',rec.id)]):
                tot_dis_cost += line.employee_id.timesheet_cost * line.unit_amount
            rec.actual_disbursement_cost = tot_dis_cost


    def _compute_actual_revenue_cost(self):
        for rec in self:
            tot_revenue_cost = 0.0
            for line in self.env['account.move'].search([('state','in',['posted']),('project_id','=',rec.id),('move_type', '=', 'out_invoice')]):
                print("line.amount_untaxed_singned",line.amount_untaxed_signed)
                tot_revenue_cost += line.amount_untaxed_signed
            rec.actual_revenue_cost = tot_revenue_cost


    
    def _compute_budget_prj(self):
        for rec in self:
            tot_revenue_cost = 0.0
            tot_disc_cost = 0.0
            for line in rec.project_budget_id:
                tot_revenue_cost += line.price_subtotal
                tot_disc_cost += line.cost
            rec.prj_revenue = tot_revenue_cost
            rec.prj_disbursement = tot_disc_cost
        
    def _compute_pm_grosss_margin_prjct(self):
        self.prj_gross_profit = 0.0
        if self.prj_revenue and self.prj_disbursement:
            self.prj_gross_profit = (self.prj_revenue/self.prj_disbursement) * 100
        else:
            self.prj_gross_profit = 0.0
            
            
    def _compute_revenue_progress(self):
        if self.prj_revenue and self.actual_revenue_cost:
            self.prj_revenue_progress = (self.actual_revenue_cost/self.prj_revenue) * 100
        else:
            self.prj_revenue_progress = 0.0
            
                
    def _compute_prj_cost(self):
        if self.prj_disbursement and self.actual_disbursement_cost:
            self.prj_cost = (self.actual_disbursement_cost/self.prj_disbursement) * 100
        else:
            self.prj_cost = 0.0
        
               

class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_revenue = fields.Float(string='Revenue',track_visibility='onchange')
    task_disbursement = fields.Float(string='Cost',track_visibility='onchange')
    task_labour = fields.Float(string='Labour Cost',track_visibility='onchange')
    task_gross_profit = fields.Float(string='Gross Margin',compute='_compute_gross_profit_task',store=False)
    percent = fields.Char(default="%")

#     @api.depends('dis_forecast_ids','dis_forecast_ids.disbursement')
#     def compute_pm_disbursement(self):
#         for rec in self:
#             rec.pm_disbursement = rec.pm_disbursement_old + sum(rec.dis_forecast_ids.mapped('disbursement'))
 
     
    @api.depends('task_revenue','task_disbursement','task_labour')
    def _compute_gross_profit_task(self):
        print("\n\n\ncompute gross profit method called for task\n\n\n")
        self.task_gross_profit = 0.0
        if self.task_revenue:
            self.task_gross_profit = ((self.task_revenue - self.task_disbursement - self.task_labour) / self.task_revenue) * 100


    # @api.depends('dis_forecast_ids','dis_forecast_ids.disbursement')
    def compute_pm_disbursement(self):
        pass
        # for rec in self:
        #     rec.pm_disbursement = rec.pm_disbursement_old + sum(rec.dis_forecast_ids.mapped('disbursement'))


class account_move(models.Model):
    _inherit = 'account.move'   
    
    
    project_id = fields.Many2one('project.project', string='Project')