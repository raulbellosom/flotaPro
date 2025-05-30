from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class FlotaProPortal(CustomerPortal):

    @http.route(['/my/trips'], type='http', auth='user', website=True)
    def portal_my_trips(self, **kwargs):
        user = request.env.user
        empleado = request.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)

        trips = request.env['flotapro.trip'].search([
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

    @http.route('/my/trips/new', type='http', auth='user', website=True)
    def portal_trip_new(self, **kwargs):
        return request.render('flotapro.portal_trip_form', {})
