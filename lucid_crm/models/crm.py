from odoo import api, fields, models, tools

PARTNER_ADDRESS_FIELDS_TO_SYNC = [
    'street',
    'street2',
    'city',
    'zip',
    'state_id',
    'country_id',
]

class CrmLead(models.Model):

    _inherit = 'crm.lead'

    proposal_team = fields.Many2many('hr.employee',string="Proposal Team",required=False)
    proposal_list_id = fields.One2many('proposal.list','proposal_list_ids')
    project_name = fields.Char(string="Project Name",required=False)
    project_id = fields.Many2one('project.project')
    is_check = fields.Boolean(string="Is Check",compute='_compute_is_check')
    budget_crm_id = fields.One2many('budget.crm','budget_crm_ids')
    # is_check_proposal = fields.Boolean('Proposal',compute='_compute_is_check_proposal')
    # is_check_nobid = fields.Boolean("No Bid",compute="_compute_is_check_nobid")
    # is_check_followup = fields.Boolean('Follow Up',compute='_compute_is_check_followup')
    # is_check_graveyard = fields.Boolean("GraveYard",compute='_compute_is_check_graveyard')
    sequence_stage = fields.Integer(string='Sequence Stage',compute='_compute_is_check_stage',store=True)

    @api.depends('is_check')
    def _compute_is_check(self):
        print("\n\n\nis check method called")
        self.is_check = True
        for rec in self:
            if rec.stage_id.sequence in [0,1]:
                rec.is_check = False

    @api.depends('stage_id')
    def _compute_is_check_stage(self):
        for rec in self:
            rec.sequence_stage = rec.stage_id.sequence 

    # @api.depends('is_check_proposal')
    # def _compute_is_check_proposal(self):
    #     self.is_check_proposal = True
    #     for rec in self:
    #         if rec.stage_id.sequence not in [0,1,2]:
    #             rec.is_check_proposal = False

    # @api.depends('is_check_nobid')
    # def _compute_is_check_nobid(self):
    #     self.is_check_nobid = True
    #     for rec in self:
    #         if rec.stage_id.sequence == 6:
    #             rec.is_check_nobid = False
    
    # @api.depends('is_check_followup')
    # def _compute_is_check_followup(self):
    #     self.is_check_followup = True
    #     for rec in self:
    #         if rec.stage_id.sequence == 7:
    #             rec.is_check_followup = False

    @api.depends('is_check_graveyard')
    def _compute_is_check_graveyard(self):
        self.is_check_graveyard = True
        for rec in self:
            if rec.stage_id.sequence == 8:
                rec.is_check_graveyard = False

    def change_state(self):
        vals=[]
        stage_ids = self.env['crm.stage'].search([('sequence','>',self.stage_id.sequence)], limit = 1)
        if stage_ids:
            self.stage_id = stage_ids[0]

        if self.stage_id.sequence == 4:
            self.action_make_project()

    def change_nobid(self):
        if self.stage_id:
            self.stage_id = 7
    
    def change_follwup(self):
        if self.stage_id:
            self.stage_id = 6
    
    def change_graveyard(self):
        if self.stage_id:
            self.stage_id = 8
    
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
                                                    'description':rec.description,
                                                    'crm_id':rec.id,
                                                    'partner_name':rec.partner_name,
                                                    'contact_name':rec.contact_name,
                                                    'street':rec.street,
                                                    'street2':rec.street2,
                                                    'zip':rec.zip,
                                                    'state_id':rec.state_id.id,
                                                    'country_id':rec.country_id.id,
                                                    'function':rec.function,
                                                    'mobile':rec.mobile,
                                                    'title':rec.title.id,
                                                    'lang_id':rec.lang_id.id,
                                                    'website':rec.website,
                                                    'campaign_id':rec.campaign_id.id,
                                                    'medium_id':rec.medium_id.id,
                                                    'source_id':rec.source_id.id,
                                                    'day_open':rec.day_open,
                                                    'day_close':rec.day_close,
                                                    'referred':rec.referred,
                                                    'proposal_list_id':[(0,0,{'crm_a':order.crm_a,
                                                                            'crm_b':order.crm_b,
                                                                            'crm_c':order.crm_c,
                                                                            'crm_d':order.crm_d,
                                                                            'crm_e':order.crm_e,
                                                                            'crm_f':order.crm_f,
                                                                            'crm_g':order.crm_g,
                                                                            'crm_h':order.crm_h,
                                                                            'crm_i':order.crm_i,
                                                                            'crm_j':order.crm_j})for order in rec.proposal_list_id],
                                                    'project_budget_id':[(0,0,{'product_id':budget.product_id.id,
                                                                               'name':budget.name,
                                                                               'employee_id':budget.employee_id.id,
                                                                               'product_uom_qty':budget.product_uom_qty,
                                                                               'qty_delivered':budget.qty_delivered,
                                                                               'qty_invoiced':budget.qty_invoiced,
                                                                               'product_uom':budget.product_uom.id,
                                                                               'price_unit':budget.price_unit,
                                                                               'tax_ids':[(6,0,budget.tax_ids.ids)],
                                                                               'discount':budget.discount,
                                                                               'price_subtotal':budget.price_subtotal,
                                                                               'cost':budget.cost,
                                                                               'currency_id':budget.currency_id.id})for budget in rec.budget_crm_id]})

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

    crm_id = fields.Many2one('crm.lead',string="Crm")
    proposal_list_id = fields.One2many('proposal.list','proposal_project_list_ids')
    proposal_team = fields.Many2many('hr.employee',string="Proposal Team")
    project_budget_id = fields.One2many('budget.crm','project_budget_ids')
    description = fields.Html()
    partner_name = fields.Char(
        'Company Name', tracking=20, index=True,
        compute='_compute_partner_name', readonly=False, store=True,
        help='The name of the future partner company that will be created while converting the lead into opportunity')
    function = fields.Char('Job Position', compute='_compute_function', readonly=False, store=True)
    title = fields.Many2one('res.partner.title', string='Title', compute='_compute_title', readonly=False, store=True)
    mobile = fields.Char('Mobile', compute='_compute_mobile', readonly=False, store=True)
    website = fields.Char('Website', index=True, help="Website of the contact", compute="_compute_website", readonly=False, store=True)
    lang_id = fields.Many2one('res.lang', string='Language')
    # # Address fields
    street = fields.Char('Street', compute='_compute_partner_address_values', readonly=False, store=True)
    street2 = fields.Char('Street2', compute='_compute_partner_address_values', readonly=False, store=True)
    zip = fields.Char('Zip', change_default=True, compute='_compute_partner_address_values', readonly=False, store=True)
    city = fields.Char('City', compute='_compute_partner_address_values', readonly=False, store=True)
    state_id = fields.Many2one(
        "res.country.state", string='State',
        compute='_compute_partner_address_values', readonly=False, store=True,
        domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one(
        'res.country', string='Country',
        compute='_compute_partner_address_values', readonly=False, store=True)
    campaign_id = fields.Many2one('utm.campaign',string="Campaign")
    medium_id = fields.Many2one('utm.medium',string="Medium")
    source_id = fields.Many2one('utm.source',string="Source")
    day_open = fields.Float('Days to Assign')
    day_close = fields.Float('Days to Close')
    referred = fields.Char('Referred By')
    contact_name = fields.Char(
        'Contact Name', tracking=30,
        compute='_compute_contact_name', readonly=False, store=True)

    def _prepare_partner_name_from_partner(self, partner):
        """ Company name: name of partner parent (if set) or name of partner
        (if company) or company_name of partner (if not a company). """
        partner_name = partner.parent_id.name
        if not partner_name and partner.is_company:
            partner_name = partner.name
        elif not partner_name and partner.company_name:
            partner_name = partner.company_name
        return {'partner_name': partner_name or self.partner_name}

    def _prepare_address_values_from_partner(self, partner):
        # Sync all address fields from partner, or none, to avoid mixing them.
        if any(partner[f] for f in PARTNER_ADDRESS_FIELDS_TO_SYNC):
            values = {f: partner[f] for f in PARTNER_ADDRESS_FIELDS_TO_SYNC}
        else:
            values = {f: self[f] for f in PARTNER_ADDRESS_FIELDS_TO_SYNC}
        return values

    @api.depends('partner_id')
    def _compute_partner_name(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            lead.update(lead._prepare_partner_name_from_partner(lead.partner_id))

    @api.depends('partner_id')
    def _compute_function(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            if not lead.function or lead.partner_id.function:
                lead.function = lead.partner_id.function

    @api.depends('partner_id')
    def _compute_title(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            if not lead.title or lead.partner_id.title:
                lead.title = lead.partner_id.title

    @api.depends('partner_id')
    def _compute_mobile(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            if not lead.mobile or lead.partner_id.mobile:
                lead.mobile = lead.partner_id.mobile

    @api.depends('partner_id')
    def _compute_website(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            if not lead.website or lead.partner_id.website:
                lead.website = lead.partner_id.website

    @api.depends('partner_id')
    def _compute_partner_address_values(self):
        """ Sync all or none of address fields """
        for lead in self:
            lead.update(lead._prepare_address_values_from_partner(lead.partner_id))



    @api.depends('partner_id')
    def _compute_contact_name(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            lead.update(lead._prepare_contact_name_from_partner(lead.partner_id))


    def _prepare_contact_name_from_partner(self, partner):
        contact_name = False if partner.is_company else partner.name
        return {'contact_name': contact_name or self.contact_name}


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
    project_budget_ids = fields.Many2one('project.project')

    @api.onchange('product_id')
    def onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.name = line.product_id.name
            if line.product_uom_qty > 0:
                line.price_unit = line.product_id.lst_price
            if line.product_uom.name == 'Days' and line.employee_id:
                line.cost = line.employee_id.timesheet_cost * line.product_uom_qty * 8
            else:
                if line.employee_id:
                    line.cost = line.employee_id.timesheet_cost * line.product_uom_qty

        
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids')
    def _compute_amount(self):
        self.price_subtotal = 0.0

        for line in self:
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
