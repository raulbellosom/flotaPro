from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'

    user_id = fields.Many2one(
        'res.users',
        string='Usuario vinculado',
        help='Usuario del sistema vinculado a este chofer para acceso al portal.'
    )
