### A simple blog system base on Flask

It's developed base on the book [Oreilly.Flask.Web.Development][1]


######TODO
    Look more detail about HttpAuth(flask-httpauth) in Flask.
    http://www.bjhee.com/flask-ext9.html

#####Steps:

##### 1. Install the extensions via `pip`

	* pip install flask-bootstrap
	* pip install flask-moment
	* pip install flask-wtf
	* pip install flask-sqlalchemy
	* pip install flask-mail
	* pip install Werkzeug
	* pip install flask-login
	* pip install forgerypy
	* pip install flask-script
	* pip install flask-pagedown markdown bleach
	* pip install flask-httpauth

##### 2. Config enviroment
  	Configure the `MAIL_USERNAME` and `MAIL_PASSWORD` in your enviroment which used to as host email.

##### 3. init database
	python3 manage.py db init

##### 4. Start the server
	python3 manage.py runserver -h 0.0.0.0

	`-h 0.0.0.0` can make your website request via ip address.


#####Notes:
* in Ch04, the ```validators=[Required()``` will cause an Exception as following:
![Exception][excep1]
the solution is:
change the Required in the form class to `Required()`

#####More detail about db 
1. run ```python3 manage.py db init``` to generate migrations folder to use db migration.
2. run ```python3 manage.py db migrate -m "init migration"``` will generate generate the sqlite file.
3. update the model class and run ```python3 manage.py db upgrade``` will upgrade the db.

#####API accessing:

    curl -u eyJleHAiOjE0ODE0NjkyMTIsImlhdCI6MTQ4MTQ2NTYxMiwiYWxnIjoiSFMyNTYifQ.eyJpZCI6Mn0.7ULasdD93HwcR3PWL6gh7coT7C1t40ykg255Vm9mg_M: -i -X POST -H "Content-Type: application/json" -d '{"body":"This is the comment from rest-api"}' http://localhost:5000/api/v1.0/posts/1/comments/

		curl -u <your email>:<your password> -i -X POST -H "Content-Type: application/json" -d '{"body":"This is the comment from rest-api"}' http://localhost:5000/api/v1.0/posts/1/comments/



[1]:http://shop.oreilly.com/product/0636920031116.do
[excep1]: exception1.png

