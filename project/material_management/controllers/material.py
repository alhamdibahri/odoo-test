# -*- coding: utf-8 -*-
import datetime
import logging

from werkzeug.exceptions import BadRequest

from odoo import api, http, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied
from odoo.http import request

_logger = logging.getLogger(__name__)

class MaterialController(http.Controller):
    
    @http.route('/auth/login', type='json', auth="none", csrf=False)
    def login(self, db, login, password):
        try:
            http.request.session.authenticate(db, login, password)
        except AccessDenied:
            return {'error': 'Invalid username or password'}
        except Exception as e:
            return {'error': str(e)}
        
        # FIX: ganti session_info() dengan get_context()
        return {
            'uid': request.session.uid,
            'context': request.session.context,
            'session_id': request.session.sid,
        }
        
    @http.route('/materials/create', type='json', auth="user", csrf=False)
    def create(self, data):
        try:
            # if data.get("buy_price", 0) < 100:
            #     return {"error": "Buy price must be greater than or equal to 100"}
            
            material = request.env['material.management.materials'].sudo().create(data)
            return {"id": material.id, "message": "Material created successfully"}
        except Exception as e:
            return {"error": f"Create materials: {str(e)}"}
    
    @http.route('/materials/get-data', type='json', auth="user", csrf=False)
    def get(self, type_material, sort, offset=0, limit=10):
        try:
           materials = request.env['material.management.materials'].sudo().search_read([['type',  '=', type_material]], order=sort, offset=offset, limit=limit)
           return materials
        except Exception as e:
            return "Get materials: %s" % str(e)

    @http.route('/materials/update', type='json', auth="user", csrf=False)
    def update(self, id, data):
        try:
           material = request.env['material.management.materials'].sudo().browse(id)
           material.update(data)
           return True
        except Exception as e:
            return "Update materials: %s" % str(e)
        
    @http.route('/materials/delete', type='json', auth="user", csrf=False)
    def delete(self, id):
        try:
           material = request.env['material.management.materials'].sudo().browse(id)
           material.unlink()
           return True
        except Exception as e:
            return "Delete materials: %s" % str(e)