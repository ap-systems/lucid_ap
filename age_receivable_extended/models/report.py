from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import time
from odoo import api, models, _
from odoo.tools import float_is_zero
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo.tools.safe_eval import safe_eval





class outstanding_reason(models.Model):
    _name='outstanding.reason' 
    
    
    name = fields.Char(string="Name")
    