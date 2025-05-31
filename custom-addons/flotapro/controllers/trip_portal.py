from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import logging

_logger = logging.getLogger(__name__)

class FlotaProPortal(CustomerPortal):

    @http.route(['/my/trips'], type='http', auth='user', website=True)
    def portal_my_trips(self, **kwargs):
        user = request.env.user
        empleado = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)

        trips = request.env['flotapro.trip'].sudo().search([
            ('chofer_id', '=', empleado.id)
        ], order='create_date desc')

        return request.render('flotapro.portal_my_trips', {
            'trips': trips,
            'page_name': 'my_trips',
        })

    @http.route('/my/trips/<int:trip_id>', type='http', auth='user', website=True)
    def portal_trip_detail(self, trip_id, **kwargs):
        trip = request.env['flotapro.trip'].sudo().browse(trip_id)
        return request.render('flotapro.portal_trip_detail', {
            'trip': trip
        })

    @http.route('/my/trips/new', type='http', auth='user', website=True, csrf=True)
    def portal_trip_new(self, **kw):
        user = request.env.user
        empleado = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)

        if not empleado:
            _logger.warning("No se encontró empleado vinculado al usuario %s", user.login)
            return request.render('flotapro.portal_my_trip_new', {
                'cards': [],
                'error': "No tienes un chofer vinculado. Contacta a administración."
            })

        tarjetas = request.env['flotapro.vehicle.card'].sudo().search([('active', '=', True)])

        if request.httprequest.method == 'POST':
            try:
                trip = request.env['flotapro.trip'].sudo().create({
                    'chofer_id': empleado.id,
                    'tarjeta_id': int(kw.get('card_id')),
                    'pasajeros': int(kw.get('passenger_count') or 0),
                    'forma_pago': kw.get('payment_method'),
                    'monto_total': float(kw.get('cost') or 0),
                    'divisa': kw.get('currency'),
                    'origen': kw.get('origin'),
                    'destino': kw.get('destination'),
                    'pasajero_principal': kw.get('main_passenger'),
                    'comentarios': kw.get('comment'),
                    'partner_id': user.partner_id.id,
                })

                return request.redirect('/my/trips/%s' % trip.id)

            except Exception as e:
                _logger.error("Error al crear viaje desde portal para usuario %s: %s", user.login, e, exc_info=True)
                return request.render('flotapro.portal_my_trip_new', {
                    'cards': tarjetas,
                    'error': str(e),
                })

        return request.render('flotapro.portal_my_trip_new', {
            'cards': tarjetas
        })
