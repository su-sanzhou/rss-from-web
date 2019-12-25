# rss-from-web
a web do not have a rss,this project can get a rss source from the web
# prerequiste
- ubuntu 18.04
```
lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.3 LTS
Release:	18.04
Codename:	bionic
```
- ubuntu user:ubuntu
- python3.6
```
python --version
Python 3.6.9
```
- pip3 
```
pip --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```
# install
## install 
```
pip3 install -r requirements.txt
pip3 install git+https://github.com/Supervisor/supervisor
sudo apt-get install postgresql postgresql-server libpsql
cd 
git clone https://github.com/su-sanzhou/rss-from-web.git
sudo cp -rv rss-from-web /var
sudo chown -R ubuntu rss-from-web
sudo chgrp -R ubuntu rss-from-web
```
## config postgresql
- create user ubuntu for postgresql 
- create database rss_from_web
- setup the password as "password" for user ubuntu when accessing database rss_from_web
# run
```
cd /var/rss-from-web/
supervisord -c supervisor/supervisord.conf
lsof -i | grep python
```
if you see listen 8000,congratulations,it's working
visit "http://localhost:8000/rss-from-web",input user_name:admin and password:password
you will see the home page



