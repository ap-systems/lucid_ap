from odoo import models, fields, api, _
import xlsxwriter   #import xlwt #help http://nullege.com/codes/search/xlwt.Style.easyxf    http://nullege.com/codes/search/xlwt
from io import StringIO
from io import BytesIO
import base64
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF

class ProjectAgeReceivable(models.Model):
    _name = 'project.age.receivable'
    
    
    project_id = fields.Many2one('project.project',string='Project')
    invoice_id = fields.Many2one('account.move',string='Invoice')
    reason_id = fields.Many2one('outstanding.reason',string='Reason')
    annotate_ap = fields.Char(string='Annotate')
    date_receivable = fields.Date(string="Date")
    
    
class cancel_reason_receivable(models.TransientModel):   
    _name = 'cancel.reason.receivable'
    
    receivable_reason_id = fields.Many2one('outstanding.reason',string='Reason')
    date_outstanding = fields.Date(string="Date")
    annotate_outstanding = fields.Text(string="Annotate")
    
    
    
    def save_reason(self):
        print(11111111111111111111111111111111,self._context)
        if self._context and self._context.get('active_id'):
            for aml in self.env['account.move.line'].browse(self._context.get('active_id')):
                if aml.move_id and aml.move_id.project_id:
                    self.env['project.age.receivable'].create({
                        'project_id' : aml.move_id.project_id.id,
                        'invoice_id' : aml.move_id.id,
                        'reason_id' : self.receivable_reason_id.id,
                        'annotate_ap' : self.annotate_outstanding,
                        'date_receivable' : self.date_outstanding,
                        })
                    manager = self.env['account.report.manager'].search([('report_name', '=', 'account.aged.receivable'),('company_id', '=', self.env.user.company_id.id)], limit = 1)
                    if self.annotate_outstanding:
                        footnote = self.env['account.report.footnote'].create({
                                'line' : aml.id,
                                'text' : self.annotate_outstanding,
                                'manager_id' : manager.id,
                                })
                        
                    
        
        

class AccountReport(models.AbstractModel):
    _inherit = 'account.report'


    def open_reason(self, options, params=None):
        document = params.get('object', 'cancel.reason.receivable')
        view_name = 'wizard_cancel_reason_receivable'
        view_id = self.env['ir.model.data']._xmlid_lookup("%s.%s" % ('age_receivable_extended', view_name))[2]
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': document,
            'view_id': view_id,
            'target': 'new',
            'context': self.env.context.copy(),
        }
        
        
        
    def get_html_footnotes(self, footnotes):
        print(66666666666666666666666)
        missing_footnotes = []
        footn_obj = self.env['account.report.footnote']
        count = len(footnotes)
        # footnotes.append({'id': 467, 'line': '175555', 'text': 'tttttttt', 'number': 2})
        for item in footnotes:
            if item.get('id'):
                for missing in footn_obj.search([('line', '=', item.get('line')), ('id', '!=', item.get('id'))]):
                    count = count + 1
                    missing_footnotes.append({'id': missing.id, 'line': str(missing.line), 'text': missing.text, 'number': count})
        footnotes = footnotes + missing_footnotes
        template = self._get_templates().get('footnotes_template', 'account_reports.footnotes_template')
        rcontext = {'footnotes': footnotes, 'context': self.env.context}
        html = self.env['ir.ui.view']._render_template(template, values=dict(rcontext))
        return html



# class AccountInvoice(models.Model):
#     _inherit = "account.invoice"
#  
# 
# 
#     def script_annote_footnote(self):
#         invoice_obj = self.env['account.invoice']
#         move_line_obj = self.env['account.move.line']
#         manager = self.env['account.report.manager'].search([('report_name', '=', 'account.aged.receivable'), ('company_id', '=', self.env.user.company_id.id)], limit = 1)
#         for prj_note in self.env['project.age.receivable'].search([('annotate_ap','!=','')]):
#             aml = move_line_obj.search([('debit', '!=', 0.0), ('invoice_id', '=', prj_note.invoice_id.id)], limit = 1)
#             if not self.env['account.report.footnote'].search([('text','=',prj_note.annotate_ap), ('manager_id','=',manager.id), ('line', '=', str(aml.id))]):
#                 footnote = self.env['account.report.footnote'].create({
#                                 'line' : aml.id,
#                                 'text' : prj_note.annotate_ap,
#                                 'manager_id' : manager.id,
#                                 })
# 
# 
#  
#     def script_footnote(self):
#         invoice_obj = self.env['account.invoice']
#         move_line_obj = self.env['account.move.line']
#         for note in self.env['account.report.footnote'].search([('manager_id.report_name','=','account.aged.receivable')]):
#             for aml in move_line_obj.search([('id', '=', int(note.line))]):
#                 if aml.invoice_id and aml.invoice_id.project_id:
#                     receivable = self.env['project.age.receivable'].create({
#                             'project_id' : aml.invoice_id.project_id.id,
#                             'invoice_id' : aml.invoice_id.id,
#                             'date_receivable' : aml.create_date,
#                             'annotate_ap' : note.text,
#                             
#                             })
                    
                
        
        
        
        

# class AccountReportFootnoteap(models.Model):
#     _inherit = 'account.report.footnote'
# 
#     
#     @api.model
#     def create(self, vals):
#         res = super(AccountReportFootnoteap, self).create(vals)
#         for aml in self.env['account.move.line'].browse(int(res.line)):
#             if aml.invoice_id and aml.invoice_id.project_id:
#                 self.env['project.age.receivable'].create({
#                         'project_id' : aml.invoice_id.project_id.id,
#                         'invoice_id' : aml.invoice_id.id,
#                         'annotate_ap' : res.text,
#                         })
#         return res