# -*- coding: utf-8 -*-
from odoo.tests.common import HttpCase
import json

class TestMaterialController(HttpCase):

    def setUp(self):
        super().setUp()
        self.supplier = self.env['res.users'].create({
            'name': 'Test Supplier',
            'login': 'supplier_test',
            'email': 'supplier@example.com',
            'password': 'test123',
        })

    def test_create_material(self):
        print("\n--- Starting test_create_material ---")

        print("-> Logging in...")
        login_data = {
            "jsonrpc": "2.0",
            "params": {
                "db": self.env.cr.dbname,
                "login": self.supplier.login,
                "password": "test123"
            }
        }
        login_response = self.url_open(
            '/auth/login',
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'}
        )
        login_json = login_response.json()
        print("-> Login response:", login_json)

        self.assertIn('result', login_json)
        self.assertIn('uid', login_json['result'])
        print("-> Login successful")

        print("-> Creating material...")
        create_data = {
            "jsonrpc": "2.0",
            "params": {
                "data": {
                    "code": "MTRL-001",
                    "name": "Cotton Premium",
                    "type": "cotton",
                    "buy_price": 120,
                    "user_id": self.supplier.id,
                }
            }
        }
        create_response = self.url_open(
            '/materials/create',
            data=json.dumps(create_data),
            headers={'Content-Type': 'application/json'}
        )
        create_json = create_response.json()
        print("-> Create response:", create_json)

        self.assertIn('result', create_json)
        self.assertIn('message', create_json['result'])
        self.assertEqual(create_json['result']['message'], "Material created successfully")

    def test_get_material(self):
        print("\n--- Starting test_get_material ---")
        print("-> Creating material manually in DB...")
        mat = self.env['material.management.materials'].create({
            "code": "MTRL-002",
            "name": "Jeans Premium",
            "type": "jeans",
            "buy_price": 150,
            "user_id": self.supplier.id,
        })
        print(f"-> Material '{mat.code}' created.")

        print("-> Logging in for session...")
        login_data = {
            "jsonrpc": "2.0",
            "params": {
                "db": self.env.cr.dbname,
                "login": self.supplier.login,
                "password": "test123"
            }
        }
        self.url_open(
            '/auth/login',
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'}
        )

        print("-> Calling /materials/get-data...")
        get_data = {
            "jsonrpc": "2.0",
            "params": {
                "type_material": "jeans",
                "sort": "name asc",
                "offset": 0,
                "limit": 10
            }
        }
        get_response = self.url_open(
            '/materials/get-data',
            data=json.dumps(get_data),
            headers={'Content-Type': 'application/json'}
        )
        get_json = get_response.json()
        print("-> Get response:", get_json)

        self.assertIn('result', get_json)
        self.assertIsInstance(get_json['result'], list)
        self.assertTrue(any(m['code'] == "MTRL-002" for m in get_json['result']))

    def test_update_material(self):
        print("\n--- Starting test_update_material ---")
        print("-> Creating material manually in DB...")
        mat = self.env['material.management.materials'].create({
            "code": "MTRL-003",
            "name": "Jeans Basic",
            "type": "jeans",
            "buy_price": 180,
            "user_id": self.supplier.id,
        })
        print(f"-> Material '{mat.code}' created.")

        print("-> Logging in for session...")
        login_data = {
            "jsonrpc": "2.0",
            "params": {
                "db": self.env.cr.dbname,
                "login": self.supplier.login,
                "password": "test123"
            }
        }
        self.url_open(
            '/auth/login',
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'}
        )

        print("-> Updating material...")
        update_data = {
            "jsonrpc": "2.0",
            "params": {
                "id": mat.id,
                "data": {
                    "name": "Jeans Premium",
                    "buy_price": 200
                }
            }
        }
        update_response = self.url_open(
            '/materials/update',
            data=json.dumps(update_data),
            headers={'Content-Type': 'application/json'}
        )
        update_json = update_response.json()
        print("-> Update response:", update_json)

        self.assertIn('result', update_json)
        self.assertTrue(update_json['result'])

        mat = self.env['material.management.materials'].browse(mat.id)
        self.assertEqual(mat.name, "Jeans Premium")
        self.assertEqual(mat.buy_price, 200)

    def test_delete_material(self):
        print("\n--- Starting test_delete_material ---")
        print("-> Creating material manually in DB...")
        mat = self.env['material.management.materials'].create({
            "code": "MTRL-004",
            "name": "fabric Basic",
            "type": "fabric",
            "buy_price": 220,
            "user_id": self.supplier.id,
        })
        mat_id = mat.id
        print(f"-> Material '{mat.code}' created with ID {mat_id}.")

        print("-> Logging in for session...")
        login_data = {
            "jsonrpc": "2.0",
            "params": {
                "db": self.env.cr.dbname,
                "login": self.supplier.login,
                "password": "test123"
            }
        }
        self.url_open(
            '/auth/login',
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'}
        )

        print("-> Deleting material...")
        delete_data = {
            "jsonrpc": "2.0",
            "params": {
                "id": mat_id
            }
        }
        delete_response = self.url_open(
            '/materials/delete',
            data=json.dumps(delete_data),
            headers={'Content-Type': 'application/json'}
        )
        delete_json = delete_response.json()
        print("-> Delete response:", delete_json)

        self.assertIn('result', delete_json)
        self.assertTrue(delete_json['result'])

        self.assertFalse(self.env['material.management.materials'].browse(mat_id).exists())

