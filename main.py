# flask_sqlalchemy/app.py
import os

from flask import Flask, render_template
from flask_graphql import GraphQLView

from models import db_session
from schema import schema, People, Transaction

from functools import wraps
from flask import request

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@app.route('/auth/user/current', methods=('GET', 'POST'))
def getuser():
    
    user = {
   "email": "noone@satoricyber.com",
   "firstName": "John",
   "lastName": "Smith"
    }

    return user,  {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/', methods=(['GET']))
def getindex():
    
    return render_template('index.html')



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
