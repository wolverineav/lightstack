echo "dropping statsapp database.."
mysql -uroot -proot -e 'drop database statsapp;'
echo "creating statsapp database.."
mysql -uroot -proot -e 'create database statsapp;'
echo "syncing db.."
python manage.py syncdb
echo "done."
