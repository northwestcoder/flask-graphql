### Simple Hello World GraphQL Server


#### Steps



1. edit the database connection variables at the top of ```models.py```
2. edit the flask secret at the top of ```main.py```
3. edit the user info in ```users.py``` - this is a mock and meant to be replaced by an actual SSO mechanism.
4. We tested with python 3.10.4
5. run ```pip install -r requirements.txt```
6. launch the flask server: ```python main.py```

This assumes you have a database available that matches the schema shown in schema.py, e.g. two tables named graphql_people and graphql_transactions