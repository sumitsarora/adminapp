DEBUG = True

THREADS_PER_PAGE = 4

CSRF_ENABLED     = True
CSRF_SESSION_KEY = "secret"

#mysql configuartion local
MYSQL_USER ='root'
MYSQL_PASSWORD ='root'
MYSQL_DB ='pcatalog'
MYSQL_HOST ='localhost'

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/pcatalog'
