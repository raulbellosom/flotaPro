{
    'name': 'FlotaPro',
    'version': '1.0',
    'category': 'Transport',
    'author': 'Raul Belloso - Racoon Devs',
    'license': 'LGPL-3',
    'summary': 'Gestión de Flotas de Vehículos, Conductores y Viajes',
    'description': """
        FlotaPro es un módulo de Odoo diseñado para la gestión integral de flotas de vehículos, conductores y viajes. Permite a las empresas optimizar sus operaciones logísticas y mejorar la eficiencia en la gestión de recursos.
        Características principales:
        - Gestión de vehículos: Registro, mantenimiento y seguimiento de vehículos.
        - Gestión de conductores: Registro, asignación y seguimiento de conductores.
        - Gestión de viajes: Planificación, seguimiento y control de viajes.
        - Integración con módulos de Odoo: Compatible con módulos de base, flota, recursos humanos y aprobaciones.
        - Informes y análisis: Generación de informes para la toma de decisiones.
    """,
    'website': 'https://www.racoondevs.com',
    'depends': ['base', 'fleet', 'hr', 'website', 'portal'],
    'application': True,
    'installable': True,
    'assets': {
    'web.assets_frontend': [],
    },
    'data': [
        'data/groups.xml',
        'security/ir.model.access.csv',
        'security/portal_driver_employee_rule.xml',
        'data/sequence.xml',
        'data/recharge_sequence.xml',
        'views/employee_views.xml',
        'views/vehicle_card_views.xml',
        'views/recharge_views.xml',
        'views/trip_views.xml',
        'views/menus.xml',
        'views/portal_templates.xml',
        'views/portal_my_trips.xml',
        'views/portal_my_trip_new.xml',
        'views/portal_trip_detail.xml',
    ],
}
