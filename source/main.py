from flask import Flask, request, jsonify
from datetime import datetime

from routes.user_routes import user_router
from routes.todo_routes import todo_router
from routes.authentication_routes import auth_router
from locales.translations import get_text
from models.key_translation import KeyTranslation

app = Flask(__name__)

app.config['DEBUG'] = True

app.register_blueprint(user_router)
app.register_blueprint(todo_router)
app.register_blueprint(auth_router)

@app.route('/', methods=['GET'])
def index():
    return jsonify(
        { 
            'status': True, 
            'data': { 
                'message': get_text(request.headers, KeyTranslation.HEALT_MESSAGE.value),
                'date': datetime.utcnow()
            } 
        })

app.run()