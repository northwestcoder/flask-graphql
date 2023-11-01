import os
from flask import Flask, request, Response, render_template, session
from flask_graphql import GraphQLView
from models import db_session
from schema import schema, People, Transaction
import users
from functools import wraps


FLASK_SECRET = "asdjkl34389asjksjdsLLKS"



app = Flask(__name__)
app.debug = True

# Basic Authentication decorator
def check_auth(username, password):
    user_info = users.user_credentials.get(username)
    if user_info and user_info['password'] == password:
        return user_info

def authenticate():
    return Response('Please log in to access this page', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        returned_user = check_auth(auth.username, auth.password)
        session['username'] = returned_user['username']
        session['first_name'] = returned_user['first_name']
        session['last_name'] = returned_user['last_name']
        return f(*args, **kwargs)
    return decorated

# Route to render the login form
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


class CustomGraphQLView(GraphQLView):
    @requires_auth
    def dispatch_request(self):
        return super(CustomGraphQLView, self).dispatch_request()

app.add_url_rule(
    '/graphql', 
    view_func=CustomGraphQLView.as_view('graphql', 
        schema=schema, 
        graphiql=True)
    )

@app.route('/auth/user/current', methods=('GET', 'POST'))
@requires_auth
def getuser():
    username = session.get('username')
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    user = {
   "email": username,
   "firstName": first_name,
   "lastName": last_name
    }

    return user,  {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/', methods=(['GET']))
@requires_auth
def getindex():
    
    return render_template('index.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.secret_key = FLASK_SECRET  # Change this to a strong secret key in a production environment
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
