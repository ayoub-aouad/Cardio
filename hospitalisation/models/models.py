# -*- coding: utf-8 -*-

from odoo import models, fields, api,_,SUPERUSER_ID
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
    is_red  = fields.Boolean(default=False)
    active  = fields.Boolean(string = 'active', default=True)
    # patient
    patient_id = fields.Many2one(string='Patient', comodel_name='res.partner', required=True,)
    sexe  = fields.Selection(string='Sexe', selection=[('male', 'Homme'),('female', 'Femme')],related='patient_id.sexe',readonly=False)
    age  = fields.Integer(string='Age',related='patient_id.age')
    # diagnostics 
    diagnostics_id = fields.Many2one(string='Diagnostique', comodel_name='osi.diagnostics',required=True)
    # lits part 
    lits_id = fields.Many2one(string='Lit', comodel_name='osi.lits',)
    room  = fields.Char(string='Chambre',related='lits_id.room',readonly=False,store=True)
    sector  = fields.Char(string='Secteur',related='lits_id.sector', readonly=False,store=True)
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('blocked', 'Blocked'),
        ('done', 'Ready')], string='Status',
        copy=False, default='normal', required=True)

    # rapport
    rapport_ids = fields.One2many(string='Rapport',comodel_name='osi.rapport',inverse_name='hospi_id' )
    repports_count  = fields.Integer(string='Counter', compute='_compute_count_all')
    # Stages 
    stage_id = fields.Many2one(string='Stages',default=lambda self: self.env['osi.stages'].search([('id','!=',False)],order='id asc', limit=1).id, comodel_name='osi.stages', copy=False, group_expand='_read_group_stage_ids')
    # This method fixes stages inside kanban view
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stages = self.env['osi.stages'].search([('name','!=',False)])
        num = len(stages) - 1
        search_domain = num*['|']
        for red in stages:
            search_domain.append(('id', '=', red.id))
        # perform search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # Compute repports 
    def _compute_count_all(self):
        repports = self.env['osi.rapport']
        for record in self:
            record.repports_count = repports.search_count([('hospi_id', '=', record.id)])

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

    # Verify duration
    @api.onchange('duration','start_date','end_date')
    def onchange_duration(self):
        for rec in self:
            params = self.env['ir.config_parameter'].sudo()
            max_duree = int(params.get_param('hospitalisation.max_duration'))
            if rec.duration >= max_duree:
                rec.kanban_state = 'blocked'
                rec.is_red = True
            else:
                rec.kanban_state = 'done'
                rec.is_red = False

    # Changing Lits Stages
    # @api.onchange('lits_id')
    # def onchange_lits_ids(self):
    #     for rec in self:
    #         if rec.lits_id:
    #             self.env['osi.lits'].search([('id','=',rec.lits_id.id)]).write({'kanban_state':'used'})
    
    # @api.onchange('stage_id')
    # def remove_hospi_ids_from_lits(self):
    #     for rec in self:
    #         stage = self.env['osi.stages'].search([('id','!=',False)],order='id desc', limit=1)
    #         if rec.stage_id.id == stage.id:
    #             self.env['osi.lits'].search([('id','=',rec.lits_id.id)]).write({'kanban_state':'free',
    #             'patient_id':False,
    #             'diagnostics_id':False,})

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
    kanban_state = fields.Selection([
        ('free', 'Libre'),
        ('used', 'Occupé'),
        ('blocked', 'Indisponible')], string='Status',
        copy=False, default='free', required=True, compute='auto_state',store=True)
    patient_id = fields.Many2one(string='Patient', comodel_name='res.partner',compute='patient_assignement',store=True)
    diagnostics_id = fields.Many2one(string='Diagnostique', comodel_name='osi.diagnostics',compute='patient_assignement',store=True)
    duration = fields.Integer(string='Durée de séjour', compute='patient_assignement', store=True)
    is_red  = fields.Selection([('true', 'True'),('false', 'False')],default='false',compute='background_changer',store=True)
    hospi_ids = fields.One2many('osi.hospitalisation', 'lits_id')
    # Automatically assigne state
    @api.depends('hospi_ids')
    def auto_state(self):
        for rec in self:
            if rec.hospi_ids:
                rec.kanban_state = 'used'

    @api.depends('duration')
    def background_changer(self):
        for rec in self:
            params = self.env['ir.config_parameter'].sudo()
            max_duree = int(params.get_param('hospitalisation.max_duration'))
            if rec.duration >= max_duree:
                rec.is_red = 'true'
            else:
                rec.is_red = 'false'

    # Automatically assigne Patient
    @api.depends('hospi_ids','hospi_ids.end_date')
    def patient_assignement(self):
        for rec in self:
            if rec.hospi_ids:
                for fields in rec.hospi_ids:
                    rec.patient_id = fields.patient_id.id
                    rec.diagnostics_id = fields.diagnostics_id.id
                    rec.duration = fields.duration
    
    # Change State 
    def sef_to_blocked(self):
        for rec in self:
            rec.kanban_state = 'blocked'
    def sef_to_free(self):
        for rec in self:
            rec.kanban_state = 'free'

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string='Est un patient', default=True)
    is_medicins = fields.Boolean(string='Est un médecin', default=False)
    sexe  = fields.Selection(string='Sexe', selection=[('male', 'Homme'),('female', 'Femme')])
    age  = fields.Integer(string='Age')
    # Medicins directory
    cnom = fields.Char(string="CNOM")
    # Patients directory
    ipp = fields.Char(string="IPP")

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


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    max_duration = fields.Integer( string="Durée max", config_parameter='hospitalisation.max_duration')

    
