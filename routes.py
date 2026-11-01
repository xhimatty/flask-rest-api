from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, create_refresh_token
from flask.views import MethodView
from schemas import ProductSchema, ProductQuerySchema, PatchProductSchema, CategorySchema, UserSchema, UserLoginSchema
from models import db, Products, Category, User, TokenBlocklist
from sqlalchemy import select

prd = Blueprint('products', __name__, url_prefix='/products')
cat = Blueprint('categories', __name__, url_prefix='/categories')
auth = Blueprint('auth', __name__, url_prefix='/auth')



@prd.route('/')
class ProductList(MethodView):

    # POST to add products

    @prd.arguments(ProductSchema)
    @prd.response(201, ProductSchema)
    def post(self, data):
        if data.get('price') < 0:
            abort(400, message='Price cannot be negative')
        products = Products(**data)
        db.session.add(products)
        db.session.commit()

        return products


    # GET to retrieve products / paginate / sort
    @jwt_required()
    @prd.doc(security=[{"BearerAuth": []}])
    @prd.arguments(ProductQuerySchema, location='query')
    @prd.response(200, ProductSchema(many=True))
    def get(self, args):
        current_user_id = get_jwt_identity()
        print(current_user_id)

        claims = get_jwt()

        if claims['role'] != 'admin':
            abort(403, message='Admin access required')

        stmt = select(Products)
        if args['sort'] == '-price':
            stmt = stmt.order_by(Products.price.desc())
        elif args['sort'] == 'price':
            stmt = stmt.order_by(Products.price)
        else:
            stmt = stmt.order_by(Products.id)
        return db.paginate(stmt, page=args['page'], per_page=args['per_page']).items



@prd.route('/<int:product_id>')
class ProductResource(MethodView):

    @prd.response(200, ProductSchema)
    def get(self, product_id):
        product = db.get_or_404(Products, product_id)
        return product


    # PUT to update product

    @prd.arguments(ProductSchema)
    @prd.response(200, ProductSchema)
    def put(self, data, product_id):
        product = db.get_or_404(Products, product_id)
        product.name = data['name']
        product.price = data.get('price')
        product.qty = data.get('qty')
        product.category_id = data['category_id']
        db.session.commit()
        return product


    # DELETE to remove product

    def delete(self, product_id):
        product = db.get_or_404(Products, product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'product deleted'}, 200


    # PATCH

    @prd.arguments(PatchProductSchema)
    @prd.response(200, ProductSchema)
    def patch(self, data, product_id):
        product = db.get_or_404(Products, product_id)
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        if 'qty' in data:
            product.qty = data['qty']
        if 'category_id' in data:
            product.category_id = data['category_id']
        db.session.commit()
        return product



# POST to add categories

@cat.route('/')
class CategoryList(MethodView):

    @cat.arguments(CategorySchema)
    @cat.response(201, CategorySchema)
    def post(self, data):
        category = Category(**data)
        db.session.add(category)
        db.session.commit()

        return category


@auth.route('/register')
class UserRegistration(MethodView):
    @auth.arguments(UserSchema)
    @auth.response(201, UserSchema)
    def post(self, data):
        stmt = select(User).filter_by(username=data['username'])

        if db.session.scalar(stmt):
            abort(409, message='User already exists.')

        user = User(name=data['name'], username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return user


@auth.route('/login')
class UserLogin(MethodView):
    @auth.arguments(UserLoginSchema)
    def post(self, data):
        stmt = select(User).filter_by(username=data['username'])
        user = db.session.scalar(stmt)

        if not user or not user.check_password(data['password']):
            abort(401, message='Invalid username or password')

        access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


    @auth.route('/refresh')
    class TokenRefresh(MethodView):
        @jwt_required(refresh=True)
        def post(self):
            current_user_id = get_jwt_identity()

            user = db.session.get(User, int(current_user_id))

            if user is None:
                abort(404, message='User not found.')

            access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})

            return {'access_token': access_token}, 200


@auth.route('/logout')
class UserLogout(MethodView):
    @jwt_required(verify_type=False)
    def post(self):
        jti = get_jwt()['jti']
        token = TokenBlocklist(jti=jti)

        db.session.add(token)
        db.session.commit()

        return {'message': 'Successfully logged out.'}, 200