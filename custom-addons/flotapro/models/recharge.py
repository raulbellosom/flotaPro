from odoo import models, fields, api, _
from odoo.exceptions import UserError

class VehicleCardRecharge(models.Model):
    _name = 'flotapro.recharge'
    _description = 'Recarga de tarjeta virtual'
    _order = 'fecha desc'

    name = fields.Char(string='Folio', readonly=True, default='/', copy=False)
    tarjeta_id = fields.Many2one('flotapro.vehicle.card', string='Tarjeta', required=True)
    cantidad = fields.Integer(string='Cantidad de recargas', required=True)
    fecha = fields.Date(string='Fecha de compra', required=True, default=fields.Date.context_today)
    
    ticket = fields.Binary(string='Comprobante de pago (ticket)')
    ticket_filename = fields.Char(string='Nombre del ticket')
    
    factura = fields.Binary(string='Factura (opcional)')
    factura_filename = fields.Char(string='Nombre de la factura')
    
    estado = fields.Selection([
        ('draft', 'Borrador'),
        ('validado', 'Validado'),
        ('rechazado', 'Rechazado')
    ], string='Estado', default='draft')
    
    observaciones = fields.Text(string='Observaciones')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('flotapro.recharge') or '/'
        return super().create(vals)

    def action_validar(self):
        for rec in self:
            if rec.estado != 'draft':
                raise UserError(_("Esta recarga ya fue procesada. Solo puedes validar recargas en estado borrador."))
            rec.estado = 'validado'

            # ✅ Aumentar recargas disponibles
            rec.tarjeta_id.available_recharges += rec.cantidad

            # ✅ También actualizar total si lo estás usando
            rec.tarjeta_id.total_recharges += rec.cantidad

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Recarga validada'),
                'message': _('La recarga fue validada correctamente.'),
                'type': 'success',
                'sticky': False,
            }
        }


    def action_rechazar(self):
        for rec in self:
            if rec.estado != 'draft':
                raise UserError(_("Esta recarga ya fue procesada. Solo puedes rechazar recargas en estado borrador."))
            rec.estado = 'rechazado'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Recarga rechazada'),
                'message': _('La recarga fue rechazada correctamente.'),
                'type': 'warning',
                'sticky': False,
            }
        }
