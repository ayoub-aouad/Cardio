from odoo import models, fields, api, _ 

class InheritHREmployee(models.Model):
    _inherit = 'hr.employee'

    department_id = fields.Many2one('hr.department', 'Département', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.onchange('department_id')
    def auto_assigne_group(self):
        name = ''
        for rec in self:
            name = rec.department_id.name
            group_1 = self.env['res.groups'].search([('name','=',name)])
            group_2 = self.env['res.groups'].search([('name','!=',name)])
            if group_1.users:
                for usr in group_1.users:
                    if usr.id != rec.user_id.id:
                        group_1.users = [(6, 0, [rec.user_id.id])]
            else:
                group_1.users = [(6, 0, [rec.user_id.id])]
            if group_2.users:
                for usr in group_2.users:
                    if usr.id == rec.user_id.id:
                        group_2.users = [(3, rec.user_id.id,False)]
    
    
    
                        



                    
    