# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime


class Hospitalisation(models.Model):
    _name = 'osi.hospitalisation'
    _description = 'Hospitalisation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom',default='Hospitalisation normale',required=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
    ], default='0', index=True, string="Starred", tracking=True)
    start_date = fields.Datetime(string='Date d\'entrée',required=True)
    end_date = fields.Datetime(string='Date de sortie')
    duration = fields.Integer(string='Durée de séjour', compute='_compute_days', store=True)
    description = fields.Text(string='Description')
    # patient
    patient_id = fields.Many2one(string='Patient', comodel_name='res.partner', required=True,)
    sexe  = fields.Selection(string='Sexe', selection=[('male', 'Homme'),('female', 'Femme')],related='patient_id.sexe',readonly=False)
    age  = fields.Integer(string='Age',related='patient_id.age')
    # region = fields.Many2one(string='Région',comodel_name='osi.region',readonly=False)
    # diagnostics 
    diagnostics_id = fields.Many2one(string='Diagnostique', comodel_name='osi.diagnostics',required=True)
    # lits part 
    lits_id = fields.Many2one(string='Lit', comodel_name='osi.lits',required=True,)
    room  = fields.Char(string='Chambre',related='lits_id.room',readonly=False)
    sector  = fields.Char(string='Secteur',related='lits_id.sector', readonly=False)
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')], string='Status',
        copy=False, default='normal', required=True)

    # Stages 
    stage_id = fields.Many2one(string='Stages', comodel_name='osi.stages')

    # Compute days number
    @api.depends('start_date','end_date')
    def _compute_days(self):
        for rec in self:
            fmt = '%Y-%m-%d %H:%M:%S'
            fnt = '%Y-%m-%d %H:%M:%S.%f'
            if rec.start_date and rec.end_date:
                start_date = rec.start_date
                end_date = rec.end_date
                start_date = str(start_date)
                end_date = str(end_date)
                d1 = datetime.strptime(start_date, fmt)
                d2 = datetime.strptime(end_date, fmt)
                rec.duration = (d2 - d1).days +1
            elif rec.start_date and  not rec.end_date :
                start_date = rec.start_date
                today = datetime.now()
                start_date = str(start_date)
                end_date = str(today)
                d1 = datetime.strptime(start_date, fmt)
                d2 = datetime.strptime(end_date, fnt)
                rec.duration = (d2 - d1).days +1
            else:
                rec.duration = rec.duration

class Diagnostics(models.Model):
    _name = 'osi.diagnostics'
    _description = 'Diagnostics'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name  = fields.Char(string='Nom', required=True)
    family = fields.Char(string='Famille', required=True)

class Lits(models.Model):
    _name = 'osi.lits'
    _description = 'Lits'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name  = fields.Char(string='Nom',required=True)
    room  = fields.Char(string='Chambre', required=True)
    sector  = fields.Char(string='Secteur', required=True)
    medicins_ids = fields.Many2many('res.partner',string='Médecins')

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string='Est un patient', default=True)
    is_medicins = fields.Boolean(string='Est un médecin', default=False)
    sexe  = fields.Selection(string='Sexe', selection=[('male', 'Homme'),('female', 'Femme')])
    age  = fields.Integer(string='Age')
    # region = fields.Many2one(string='Région',comodel_name='osi.region')

class Tags(models.Model):
    _name = 'osi.tags'

    name  = fields.Char(string='Nom' , required=True, )
    color  = fields.Integer(string='Color')

class Stages(models.Model):
    _name = 'osi.stages'

    name  = fields.Char(string='Nom' , required=True, )

class Region(models.Model):
    _name = 'osi.region'

    name  = fields.Char(string='Nom' , required=True, )
    arab_name  = fields.Char(string='Région(arabe)' )

    
