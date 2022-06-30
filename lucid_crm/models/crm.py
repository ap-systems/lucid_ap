from odoo import api, fields, models, tools



class CrmLead(models.Model):

    _inherit = 'crm.lead'

    proposal_team = fields.Many2many('hr.employee',string="Proposal Team",required=False)
    proposal_list_id = fields.One2many('proposal.list','proposal_list_ids')
    project_name = fields.Char(string="Project Name",required=False)
    project_id = fields.Many2one('project.project')
    is_check = fields.Boolean(string="Is Check",compute='_compute_is_check')
    budget_crm_id = fields.One2many('budget.crm','budget_crm_ids')

    @api.depends('is_check')
    def _compute_is_check(self):
        self.is_check = True
        for rec in self:
            if rec.stage_id.sequence in [0,1]:
                rec.is_check = False

    def change_state(self):
        vals=[]
        stage_ids = self.env['crm.stage'].search([('sequence','>',self.stage_id.sequence)], limit = 1)
        if stage_ids:
            self.stage_id = stage_ids[0]

        if self.stage_id.sequence == 4:
            self.action_make_project()
    
    def action_set_won(self):
        res = super(CrmLead,self).action_set_won()
        self.action_make_project()        
        return res

    def action_make_project(self):
        for rec in self:
            if rec.project_name and rec.proposal_team:
                rec.project_id = self.env['project.project'].create({'name':rec.project_name,
                                                    'partner_id':rec.partner_id.id,
                                                    'user_id':rec.user_id.id,
                                                    'company_id':rec.company_id.id,
                                                    'proposal_team':[(6,0,rec.proposal_team.ids)],
                                                    'proposal_list_id':[(0,0,{'crm_a':order.crm_a,
                                                                            'crm_b':order.crm_b,
                                                                            'crm_c':order.crm_c,
                                                                            'crm_d':order.crm_d,
                                                                            'crm_e':order.crm_e,
                                                                            'crm_f':order.crm_f,
                                                                            'crm_g':order.crm_g,
                                                                            'crm_h':order.crm_h,
                                                                            'crm_i':order.crm_i,
                                                                            'crm_j':order.crm_j})for order in rec.proposal_list_id]})

class ProposalList(models.Model):

    _name = 'proposal.list'
    _description = 'Proposal List'

    crm_a = fields.Char(string="A")
    crm_b = fields.Char(string="B")
    crm_c = fields.Char(string="C")
    crm_d = fields.Char(string="D")
    crm_e = fields.Char(string="E")
    crm_f = fields.Char(string="F")
    crm_g = fields.Char(string="G")
    crm_h = fields.Char(string="H")
    crm_i = fields.Char(string="I")
    crm_j = fields.Char(string="J")
    proposal_list_ids = fields.Many2one('crm.lead')
    proposal_sale_list_ids = fields.Many2one('sale.order')
    proposal_project_list_ids = fields.Many2one('project.project')

# class SaleOrder(models.Model):

#     _inherit = 'sale.order'

#     proposal_list_id = fields.One2many('proposal.list','proposal_sale_list_ids') 
#     project_name = fields.Char(string="Project Name",required=True)
#     proposal_team = fields.Many2many('hr.employee',string="Proposal Team")
   
#     def action_confirm(self):
#         res = super(SaleOrder,self).action_confirm()
#         for rec in self:
#             if rec.project_name:
#                 rec.project_id = self.env['project.project'].create({'name':rec.project_name,
#                                                     'partner_id':rec.partner_id.id,
#                                                     'user_id':rec.user_id.id,
#                                                     'company_id':rec.company_id.id,
#                                                     'proposal_team':[(6,0,rec.proposal_team.ids)],
#                                                     'proposal_list_id':[(0,0,{'crm_a':order.crm_a,
#                                                                             'crm_b':order.crm_b,
#                                                                             'crm_c':order.crm_c,
#                                                                             'crm_d':order.crm_d,
#                                                                             'crm_e':order.crm_e,
#                                                                             'crm_f':order.crm_f,
#                                                                             'crm_g':order.crm_g,
#                                                                             'crm_h':order.crm_h,
#                                                                             'crm_i':order.crm_i,
#                                                                             'crm_j':order.crm_j})for order in rec.proposal_list_id]})
#         return res

class ProjectProject(models.Model):

    _inherit = 'project.project'

    proposal_list_id = fields.One2many('proposal.list','proposal_project_list_ids')
    proposal_team = fields.Many2many('hr.employee',string="Proposal Team")

class BudgetCrm(models.Model):

    _name = 'budget.crm'

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    product_id = fields.Many2one('product.product')
    name = fields.Text(string="Description")
    employee_id = fields.Many2one('hr.employee')
    product_uom_qty = fields.Float(string="Quantity",default="1.0")
    qty_delivered = fields.Float(string="Delivered")
    qty_invoiced = fields.Float(string="Invoiced")
    product_uom = fields.Many2one(related="product_id.uom_id",readonly=True)
    price_unit = fields.Float(string="Unit Price")
    tax_ids = fields.Many2many('account.tax',string="Taxes")
    discount = fields.Float(string='Disc%')
    price_subtotal = fields.Monetary(string="Subtotal",compute="_compute_amount")
    cost = fields.Monetary(string="Cost",compute="_compute_cost")
    budget_crm_ids = fields.Many2one('crm.lead')
    currency_id = fields.Many2one('res.currency', store=True, string='Currency',default=lambda self: self._default_currency_id())
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
        if self.product_uom_qty > 0:
            self.price_unit = self.product_id.lst_price
        if self.product_uom_qty == 0:
            self.price_unit = 0.0
        
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids')
    def _compute_amount(self):
        self.price_subtotal = 0.0
        
        for line in self:
            if line.product_uom_qty > 0:
                line.price_unit = line.product_id.lst_price
            if line.product_uom_qty == 0:
                line.price_unit = 0.0
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.currency_id, line.product_uom_qty, product=line.product_id, partner=line.budget_crm_ids.partner_id)
            line.update({
                'price_subtotal': taxes['total_excluded'],
            })
            
    @api.depends('product_uom_qty','employee_id')
    def _compute_cost(self):
        self.cost = 0.0
        for line in self:
            if line.product_uom.name == 'Days' and line.employee_id:
                line.cost = line.employee_id.timesheet_cost * line.product_uom_qty * 8
            else:
                if line.employee_id:
                    line.cost = line.employee_id.timesheet_cost * line.product_uom_qty
