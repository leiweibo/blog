### A simple blog system base on Flask

It's was developed base on what I read from the book [Oreilly.Flask.Web.Development][1]

#####Steps:
* pip install flask-bootstrap
* pip install flask-moment
* pip install flask-wtf
* pip install flask-sqlalchemy
* pip install flask-mail
* pip install Werkzeug
#####Notes:
* in Ch04, the ```validators=[Required()``` will cause an Exception as following:
![Exception][excep1]
the solution is:
change the Required in the form class to `Required()`

###### About db 
1. run ```python3 manage.py db init``` to generate migrations folder to use db migration.
2. run ```python3 manage.py db migrate -m "init migration"``` will generate generate the sqlite file.
3. update the model class and run ```python3 manage.py db upgrade``` will upgrade the db.

[1]:http://shop.oreilly.com/product/0636920031116.do
[excep1]: exception1.png