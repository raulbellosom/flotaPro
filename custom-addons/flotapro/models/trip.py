from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

class Trip(models.Model):
    _name = 'flotapro.trip'
    _description = 'Registro de viaje de transporte'
    _order = 'fecha_inicio desc'

    name = fields.Char(string='Folio del viaje', readonly=True, default='/', copy=False, help='Número de folio único del viaje')
    chofer_id = fields.Many2one('hr.employee', string='Chofer', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo')
    tarjeta_id = fields.Many2one('flotapro.vehicle.card', string='Tarjeta virtual', required=True)

    fecha_inicio = fields.Datetime(string='Inicio del viaje')
    fecha_fin = fields.Datetime(string='Fin del viaje')

    origen = fields.Char(string='Origen', default='Aeropuerto Internacional de Puerto Vallarta', required=True)
    destino = fields.Char(string='Destino', required=True)  # Campo abierto

    pasajeros = fields.Integer(string='Cantidad de pasajeros')
    pasajero_principal = fields.Char(string='Nombre de pasajero (opcional)')
    recargas_usadas = fields.Integer(string='Recargas usadas', default=0, readonly=True)

    comentarios = fields.Text(string='Comentarios del chofer')

    monto_total = fields.Float(string='Monto total del viaje')
    divisa = fields.Selection([
        ('MXN', 'MXN'),
        ('USD', 'USD'),
        ('EUR', 'EUR')
    ], string='Divisa', default='MXN')
    forma_pago = fields.Selection([
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ], string='Forma de pago')
    referencia_pago = fields.Char(string='Referencia de pago (opcional)')

    estado = fields.Selection([
        ('draft', 'Borrador'),
        ('en_curso', 'En curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='draft')

    adjunto_ids = fields.Many2many('ir.attachment', string='Archivos adjuntos')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('flotapro.trip') or '/'

        # Si se ha seleccionado una tarjeta, obtener su vehículo
        if not vals.get('vehicle_id') and vals.get('tarjeta_id'):
            tarjeta = self.env['flotapro.vehicle.card'].browse(vals['tarjeta_id'])
            vals['vehicle_id'] = tarjeta.vehicle_id.id if tarjeta.vehicle_id else False

        return super().create(vals)


    @api.onchange('tarjeta_id')
    def _onchange_tarjeta_id(self):
        for rec in self:
            rec.vehicle_id = rec.tarjeta_id.vehicle_id if rec.tarjeta_id else False

    def action_iniciar(self):
        for rec in self:
            if rec.estado != 'draft':
                raise UserError(_("Solo se pueden iniciar viajes en estado Borrador."))
            if rec.tarjeta_id.available_recharges < 1:
                raise UserError(_("La tarjeta seleccionada no tiene recargas disponibles."))

            rec.tarjeta_id.available_recharges -= 1
            rec.recargas_usadas = 1
            rec.estado = 'en_curso'
            rec.fecha_inicio = fields.Datetime.now()

    def action_finalizar(self):
        for rec in self:
            rec.estado = 'finalizado'
            rec.fecha_fin = datetime.now()

    def action_cancelar(self):
        for rec in self:
            rec.estado = 'cancelado'

    # def action_borrador(self):
    #     for rec in self:
    #         rec.estado = 'draft'
