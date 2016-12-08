### A simple blog system base on Flask

It's developed base on the book [Oreilly.Flask.Web.Development][1]


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

###### More detail about db 
1. run ```python3 manage.py db init``` to generate migrations folder to use db migration.
2. run ```python3 manage.py db migrate -m "init migration"``` will generate generate the sqlite file.
3. update the model class and run ```python3 manage.py db upgrade``` will upgrade the db.

[1]:http://shop.oreilly.com/product/0636920031116.do
[excep1]: exception1.png