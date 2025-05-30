from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class FlotaProPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if request.env.user.has_group('flotapro.group_portal_driver'):
            values['recharge_count'] = request.env['flotapro.recharge'].search_count([
                ('create_uid', '=', request.env.uid)
            ])
            values['trip_count'] = request.env['flotapro.trip'].search_count([
                ('chofer_id.user_id', '=', request.env.user.id)
            ])
        return values

    @http.route('/my/recargas', type='http', auth='user', website=True)
    def my_recargas(self, **kw):
        recargas = request.env['flotapro.recharge'].sudo().search([
            ('create_uid', '=', request.env.uid)
        ])
        return request.render('flotapro.portal_my_recargas', {'recargas': recargas})
