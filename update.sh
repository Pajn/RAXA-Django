cd /RAXA/web
source env/bin/activate
./manage.py migrate backend --fake
./manage.py migrate common --fake
./manage.py migrate django_cron --fake