import os
DB = dict(host=os.getenv("MYSQL_HOST", "localhost"), user=os.getenv("MYSQL_USER", "root"),
          password=os.getenv("MYSQL_PASSWORD", "your_password"),
          database=os.getenv("MYSQL_DB", "biological_age"))
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")