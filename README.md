as my huginn jobs as rss source always show as not working,so i write a rss source from web,replace huginn.
the grab time interval can be configured ,in the config.py,the init value is 12 hours
# 0.known bugs:
 all kinds of css can not contain a space " ",or contain a single quote "'" or double quote '"' which is not belong 
to the xpath format,such as "//title's tr" or "//title tr",must be "//titletr" 

# 1.rss-from-web
a web do not have a rss,this project can get a rss source from the web
# 2.prerequiste
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
# 3.install
## 3.1 install command 
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
## 3.2 config postgresql
- create user ubuntu for postgresql 
- create database rss_from_web
- setup the password as "password" for user ubuntu when accessing database rss_from_web
# 4.run
```
cd /var/rss-from-web/
supervisord -c supervisor/supervisord.conf
lsof -i | grep python
```
if you see listen 8000,congratulations,it's working
visit "http://localhost:8000/rss-from-web",input user_name:admin and password:password
you will see the home page,it looks like this:
![image](https://github.com/su-sanzhou/rss-from-web/blob/master/screen/Selection_001.png)

# 5.usage
click the "Add a rss" on the right up corner,then you could add something like this:
![image](https://github.com/su-sanzhou/rss-from-web/blob/master/screen/Selection_002.png)

you can copy all the xpath css here:
```
https://sanzhou.live/

//section/article/header/h1/a

//section/article/header/h1/a

False

//header/div/div[1]/div/a/span[2]

//header/div/div[1]/p

//article

//header/div/div[1]/div/a/span[2]

//article/header/div/span[1]/time
```

then click the save button,you will see the rss source,like this:
![image](https://github.com/su-sanzhou/rss-from-web/blob/master/screen/Selection_003.png)

then you can use your rss reader subscribe it.

