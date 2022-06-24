from odoo import api, fields, models, tools



class ProjectProject(models.Model):
    _inherit = 'project.project'
     
    
    prj_revenue = fields.Float(string='Revenue', compute='_compute_budget_prj',store=False, track_visibility='onchange')
    prj_disbursement = fields.Float(string='Disbursements Cost', compute='_compute_budget_prj',store=False, track_visibility='onchange')
    prj_labour = fields.Float(string='Labour Cost', compute='_compute_budget_prj',store=False, track_visibility='onchange')
    prj_gross_profit = fields.Float(string='Gross Margin',store=False, compute='_compute_pm_grosss_margin_prjct',track_visibility='onchange')
    ap_invoice_ids = fields.One2many('account.move', 'project_id', string='Invoice', track_visibility='onchange')
    percent = fields.Char(default="%")
    prj_revenue_progress = fields.Integer(string='Revenue',compute='_compute_revenue_progress')
    prj_cost = fields.Integer(string='Cost',compute='_compute_prj_cost')
    actual_disbursement_cost = fields.Float(string='A.Disbursements Cost')
    actual_labour_cost = fields.Float(string='A.Labour Cost')
     

    @api.depends('task_ids.task_revenue', 'task_ids.task_disbursement', 'task_ids.task_labour','task_ids','task_ids.active')
    def _compute_budget_prj(self):
        for rec in self:
            tasks = self.env['project.task'].search([('project_id','=',self.id),('parent_id','=',False),'|',('active','!=',True),('active','!=',False)])
            rec.prj_revenue = sum(tasks.mapped('task_revenue'))
            rec.prj_disbursement = sum(tasks.mapped('task_disbursement'))
            rec.prj_labour = sum(tasks.mapped('task_labour'))
        
    @api.depends('prj_revenue', 'prj_disbursement', 'prj_labour')
    def _compute_pm_grosss_margin_prjct(self):
        self.prj_gross_profit = 0.0
        if self.prj_revenue:
            self.prj_gross_profit = ((self.prj_revenue - self.prj_disbursement - self.prj_labour) / self.prj_revenue ) * 100
            
            
            
    @api.depends('ap_invoice_ids','prj_revenue')
    def _compute_revenue_progress(self):
        self.prj_revenue_progress = 0.0
        total_invoice = sum(self.ap_invoice_ids.filtered(lambda x: x.state in ['posted']).mapped('amount_untaxed_signed'))
        if self.prj_revenue:
            self.prj_revenue_progress = total_invoice / self.prj_revenue
            
            
                
    @api.depends('prj_labour','prj_disbursement','actual_labour_cost','actual_disbursement_cost')
    def _compute_prj_cost(self):
        self.prj_cost = 0.0
        for rec in self:
            if rec.prj_labour or rec.prj_disbursement:
                rec.prj_cost = ((rec.actual_labour_cost + rec.actual_disbursement_cost)/(rec.prj_labour + rec.prj_disbursement)) * 100

               

class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_revenue = fields.Float(string='Revenue',track_visibility='onchange')
    task_disbursement = fields.Float(string='Disbursements Cost',track_visibility='onchange')
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



class account_move(models.Model):
    _inherit = 'account.move'   
    
    
    project_id = fields.Many2one('project.project', string='Project')