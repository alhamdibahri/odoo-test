# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import ValidationError

class Materials(models.Model):
    _name = 'material.management.materials'
    _description = 'Materials'

    code = fields.Char("Material Code", required=True)
    name = fields.Char("Material Name", required=True)
    buy_price = fields.Float("Material Buy Price", required=True)
    type = fields.Selection([
            ("fabric", "Fabric"),
            ("jeans", "Jeans"),
            ("cotton", "Cotton")
        ], string="Material Type", required=True)
    user_id = fields.Many2one("res.users", string="Supplier", required=True)

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError("Material Buy Price must be at least 100.")