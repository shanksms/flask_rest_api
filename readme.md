# Flask Rest concepts

## resources
[O'Reilly course] (https://learning.oreilly.com/videos/rest-apis-with/9781788621526/9781788621526-video3_4/)
[Deploy Flask to prod] (https://vsupalov.com/flask-web-server-in-production/)
[Flask rest end points design] (https://stackoverflow.com/questions/20715238/flask-restful-api-multiple-and-complex-endpoints)
[Rest design principles] (https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design)
[Flask jwt] (https://blog.teclado.com/simple-jwt-authentication-with-flask-jwt/)

## Authentication
### JWT
#### what is it
What is a JWT?
JWT stands for JSON Web Token, and it is a piece of text with some information encoded into it.
The information stored when doing authentication in a Flask app is usually something that we can use to identify the user for whom we generated the JWT.
The flow goes like this:
User provides their username and password
1. We verify they are correct inside our Flask app
2. We generate a JWT which contains the user's ID.
3. We send that to the user.
4. Whenever the user makes a request to our application, they must send us the JWT we generated earlier. By doing this, we can verify the JWT is valid—and then we'll know the user who sent us the JWT is the user for whom we generated it.
That last point is important. When we receive a JWT we know to be valid, we know we generated it for a specific user. We can check this using the information stored inside the JWT.
Since we know the user sent us the JWT that we generated when they logged in, we can treat this used as a "logged in user".
Any user that does not send us a valid JWT, we will treat as a "logged out" user.
in flask App this is how we configure jwt:
```python
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)
# this creates /auth end point
jwt = JWT(app, authenticate, identity)
```
As a result of above code, flask rest app will expose an end point /auth, which will first call authenticate method and
if authentication is successful, it will return jwt token

## Authentication - ends

## Rest Principles

### Thinking end points as resources
Lets say there is a chair resource on a server.
|HTTP Method|Resource|
|----|-----|
|GET|/items/chair|
|POST|/items|
|PUT|/items|
|DELETE|/items/chair|

<br>
as you can see for all the http verbs, same url is sufficient.

### Test-First API design
in this we start with designing the API end points. If possible use a tool like Postman to save the end points.

### important http status codes
1. 200 for success
2. 201 for resource created. Generally this code is returned from post request
3. 404 for resource not found. 
4. 400 for bad request

## Rest Principles - ends
 

### json always used " while python dictionaries can use ' also

## Flask restfull
### This is a sample Flask restful code.
it lets you encapsulate a Resource in a class
```python
from flask import Flask
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)
class Student(Resource):
    def get(self, name):
        return {'student': name}
api.add_resource(Student, '/student/<string:name>')
app.run(port=5000)
```

## Flask restful - ends

### how to return response and status code from Flask
```python
from flask import Response
def rest_end_point_method():
    return Response("{'a':'b'}", status=201, mimetype='application/json')
```