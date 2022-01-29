# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime


class Hospitalisation(models.Model):
    _name = 'osi.hospitalisation'
    _description = 'Hospitalisation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',required=True)
    start_date = fields.Datetime(string='Start date',required=True)
    end_date = fields.Datetime(string='End date')
    duration = fields.Integer(string='Duration', compute='_compute_days', store=True)
    description = fields.Text(string='Description')
    # patient
    patient_id = fields.Many2one(string='Patient', comodel_name='res.partner', required=True,)
    sexe  = fields.Selection(string='Sexe', selection=[('male', 'Male'),('female', 'Female')],related='patient_id.sexe',readonly=False)
    # diagnostics 
    diagnostics_id = fields.Many2one(string='Diagnostic', comodel_name='osi.diagnostics',required=True)
    # lits part 
    lits_id = fields.Many2one(string='Lit', comodel_name='osi.lits',required=True,)
    room  = fields.Char(string='Room',related='lits_id.room',readonly=False)
    sector  = fields.Char(string='Sector',related='lits_id.sector', readonly=False)
    # Stages 
    stage_id = fields.Many2one(string='Stages', comodel_name='osi.stages')

    # Compute days number
    @api.depends('start_date','end_date')
    def _compute_days(self):
        for rec in self:
            fmt = '%Y-%m-%d %H:%M:%S'
            if rec.start_date and rec.end_date:
                start_date = rec.start_date
                end_date = rec.end_date
                start_date = str(start_date)
                end_date = str(end_date)
                d1 = datetime.strptime(start_date, fmt)
                d2 = datetime.strptime(end_date, fmt)
                rec.duration = (d2 - d1).days +1
            else:
                rec.duration = rec.duration
class Diagnostics(models.Model):
    _name = 'osi.diagnostics'
    _description = 'Diagnostics'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name  = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one(string='Family', comodel_name='osi.diagnostics')

class Lits(models.Model):
    _name = 'osi.lits'
    _description = 'Lits'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name  = fields.Char(string='Name',required=True)
    room  = fields.Char(string='Room', required=True)
    sector  = fields.Char(string='Sector', required=True)
    medicins_ids = fields.Many2many('res.partner',string='Medicins')

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string='Is patient')
    is_medicins = fields.Boolean(string='Is medicins')
    sexe  = fields.Selection(string='Sexe', selection=[('male', 'Male'),('female', 'Female')])

class Tags(models.Model):
    _name = 'osi.tags'

    name  = fields.Char(string='Name' , required=True, )
    color  = fields.Integer(string='Color')

class Stages(models.Model):
    _name = 'osi.stages'

    name  = fields.Char(string='Name' , required=True, )

    
