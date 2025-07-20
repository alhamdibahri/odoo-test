{
    'name': 'Material Management',
    'version': '1.0.0',
    'Author': 'Alhamdi Ferdiawan Bahri',
    'website': 'https://github.com/alhamdibahri',
    'category': 'Sales/Sales',
    'summary': 'Material Management system',
    'description': 'Material Management system',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',

    'data': [
        'views/materials.xml',
        'views/menu_items.xml'
    ],
    'test': [
        'tests/test_material_controller.py',
    ],
}