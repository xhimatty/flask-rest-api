import os
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from werkzeug.exceptions import InternalServerError
from models import db, User, TokenBlocklist
from sqlalchemy import select

load_dotenv()

app = Flask(__name__)

app.config['API_TITLE'] = 'Products REST API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

app.config['API_SPEC_OPTIONS'] = {
    'components': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT'
            }
        }
    }
}

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def checke_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    stmt = select(TokenBlocklist).filter_by(jti=jti)
    token = db.session.scalar(stmt)

    return token is not None

api = Api(app)
db.init_app(app)

migrate = Migrate(app, db)

from routes import prd, cat, auth

api.register_blueprint(prd)
api.register_blueprint(cat)
api.register_blueprint(auth)


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'code': 500,
        'status': 'Internal Server Error',
        'message': 'An unexpected error occured'
    }), 500

print('Server is active and running')
if __name__ == '__main__':
    app.run(debug=True)