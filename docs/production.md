# Some General Information about the Production UNICEF Instance

## Key Information

| Information | Value |
| ----------- | ----- |
| Url  | https://data.uniceflabs.org/ |
| Host  | 52.209.114.249 |
| User | www-data |
| Project Home | /var/www/data_api |
| Virtualenv Home | /var/www/.virtualenvs/api |
| Server log | /mnt/data1/data/log/api/server.log |
| Settings | /var/www/data_api/data_api/settings.py |
| Supervisor Config | /etc/supervisor/supervisord.conf |
| Nginx Config | /etc/nginx/sites-enabled/api.conf |
| SQL Database | /var/www/data_api/db.sqlite3 |
| Mongo Database | rapidpro-v2-test |

## Redash

The same machine is also running redash.
Here is some information about that setup.
It mostly mirrors the [installation script](https://raw.githubusercontent.com/getredash/redash/master/setup/ubuntu/bootstrap.sh)
though a few changes were made to run it in a virtualenv.

| Information | Value |
| ----------- | ----- |
| Url  | http://redash.uniceflabs.org/ |
| Host  | 52.209.114.249 |
| User | redash |
| Project Home | /opt/redash/current |
| Virtualenv Home | /usr/local/share/virtualenvs/redash/ |
| Settings | /opt/redash/current/.env |
| Supervisor Config | /etc/supervisor/conf.d/redash.conf |
| Nginx Config | /etc/nginx/sites-available/redash |
