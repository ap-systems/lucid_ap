from odoo import api, fields, models, tools



class CrmLead(models.Model):

    _inherit = 'crm.lead'

    proposal_team = fields.Many2many('hr.employee',string="Proposal Team")
    proposal_list_id = fields.One2many('proposal.list','proposal_list_ids')

    def change_state(self):
        vals=[]
        stage_ids = self.env['crm.stage'].search([('sequence','>',self.stage_id.sequence)], limit = 1)
        if stage_ids:
            self.stage_id = stage_ids

        if self.stage_id.sequence == 4:
            for rec in self:
                rec.order_ids = self.env['sale.order'].create({'partner_id':rec.partner_id.id,
                                               'tag_ids':[(6,0,rec.tag_ids.ids)],
                                               'user_id':rec.user_id.id,
                                               'company_id':rec.company_id.id,
                                               'validity_date':rec.date_deadline,
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

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    proposal_list_id = fields.One2many('proposal.list','proposal_sale_list_ids') 
    project_name = fields.Char(string="Project Name",required=True)
    proposal_team = fields.Many2many('hr.employee',string="Proposal Team")
    

    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        for rec in self:
            if rec.project_name:
                self.env['project.project'].create({'name':rec.project_name,
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
                
        return res

class ProjectProject(models.Model):

    _inherit = 'project.project'

    proposal_list_id = fields.One2many('proposal.list','proposal_project_list_ids')
    proposal_team = fields.Many2many('hr.employee',string="Proposal Team")