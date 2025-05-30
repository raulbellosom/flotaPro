from odoo import models, fields

class VehicleCard(models.Model):
    _name = 'flotapro.vehicle.card'
    _description = 'Tarjeta Virtual del Vehículo'

    name = fields.Char(string='Código de Tarjeta', required=True, coppy=False, help='Código único de la tarjeta virtual del vehículo')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo', required=True)
    vehicle_type = fields.Selection([
        ('small', 'Vehículo pequeño'),
        ('medium', 'Vehículo mediano'),
        ('large', 'Vehículo grande')
    ], string='Tipo de Vehículo', required=True)
    total_recharges = fields.Integer(string='Total de recargas', default=0, help='Número total de recargas realizadas en esta tarjeta', readonly=True)
    available_recharges = fields.Integer(string='Recargas disponibles', default=0, readonly=True, help='Número de recargas disponibles para usar en viajes', copy=False)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'El código de la tarjeta debe ser único.')
    ]
