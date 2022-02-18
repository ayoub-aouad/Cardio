from odoo import api, fields, models
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import ValidationError
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from dateutil.relativedelta import relativedelta


class Rapport(models.Model):
    _name = 'osi.rapport'

    medicin_id = fields.Many2one(
        'res.partner',string='Médecins',required=True, 
        )
    hospi_id = fields.Many2one(string='Hospitalisation', comodel_name='osi.hospitalisation')
    
    text  = fields.Html(string='Rapport',required=True, )
    date = fields.Datetime(string='Date de rapport',required=True, )