from marshmallow import Schema, fields

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float()
    qty = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    category_id = fields.Int(allow_none=True)
    category = fields.Nested(CategorySchema, dump_only=True)


class ProductQuerySchema(Schema):
    page = fields.Int(load_default=1)
    per_page = fields.Int(load_default=5)
    sort = fields.Str(load_default='id')


class PatchProductSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    qty = fields.Int()
    category_id = fields.Int(allow_none=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)