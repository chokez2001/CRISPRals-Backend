from flask import Flask

from api.constants.status_response import OK_SUCCES, BAD_REQUEST
from api.settings import APP_NAME, DATABASE_URI, TRACK_MODIFICATIONS
from flask_cors import CORS
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.db_models import db
from api.graphql import schema

def create_app(app_name='MYAPPNAME'):
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = TRACK_MODIFICATIONS
    db.init_app(app)


    @app.route('/')
    def index():
        return f'<h2>{APP_NAME}</h2>'


    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, OK_SUCCES


    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        status_code = OK_SUCCES if success else BAD_REQUEST
        return jsonify(result), status_code
    return app