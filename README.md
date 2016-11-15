### A simple blog system base on Flask

It's was developed base on what I read from the book [Oreilly.Flask.Web.Development][1]

#####Steps:
* pip install flask-bootstrap
* pip install flask-moment
* pip install flask-wtf
* pip install flask-sqlalchemy
* pip install flask-mail
#####Notes:
* in Ch04, the ```validators=[Required()``` will cause an Exception as following:
![Exception][excep1]
the solution is:
change the Required in the form class to `Required()`

[1]:http://shop.oreilly.com/product/0636920031116.do
[excep1]: exception1.png