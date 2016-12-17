#####Steps:
  * Install virtualenv and configure the virtualenv: virtualenv -p <python3 path> python3env
  * Active the python3env: sorce python3env/bin/active (Just deactivate when you dont want to use the virtualenv)_
  * Install the dependiencies: pip install -r requirements/prod.txt
  * Configure the enviroment variable:
    - MAIL_USERNAME
    - MAIL_PASSWORD 
    - FLASKY_ADMIN

  * Congure the db: 
    - ```python3 manage.py db init```
    - ```python3 manage.py db migrate -m "init migration" <<The comment need to be changed for the real change comment>>```

  * Run the deploy: python manage.py deploy
  * install uwsgi: pip install uwsgi

  * Install supervisor in ubuntu: sudo apt-get install supervisor
    * Add a new conf in /etc/supervisor/conf.d/ folder: refer to flask_blog_supervisor.conf

  * Install nginx in ubuntu: apt-get install nginx
    * Backup the existed default in /etc/nginx/sites-available/default, and create a new default file in the folder, refer to: defualt_nginx

  Everything is up, run 
    ```service supervisor restart```
    ```service nginx restart```

  HERE WE GO!!!!