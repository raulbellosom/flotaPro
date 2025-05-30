from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class PortalTrip(CustomerPortal):

    @http.route('/my/trips/new', type='http', auth='user', website=True, csrf=True)
    def portal_create_trip(self, **kw):
        if request.httprequest.method == 'POST':
            # Aquí extraes los datos y creas el viaje
            passenger_count = kw.get('passenger_count')
            payment_method = kw.get('payment_method')
            cost = kw.get('cost')
            currency = kw.get('currency')
            origin = kw.get('origin')
            destination = kw.get('destination')
            main_passenger = kw.get('main_passenger')
            comment = kw.get('comment')

            # Crea el viaje
            trip = request.env['flotapro.trip'].sudo().create({
                'passenger_count': passenger_count,
                'payment_method': payment_method,
                'cost': cost,
                'currency': currency,
                'origin': origin,
                'destination': destination,
                'main_passenger': main_passenger,
                'comment': comment,
                'partner_id': request.env.user.partner_id.id,
            })

            return request.redirect('/my/trips/%s' % trip.id)

        return request.render('flotapro.portal_my_trip_new')
