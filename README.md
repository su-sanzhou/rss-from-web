Because my huginn jobs as rss source always show as not working,so i write a rss source from web,replace huginn.
the grab time interval can be configured ,in the config.py,the init value is 12 hours
# 0.known bugs
All kinds of css can not contain only a single quote ' or only a double quote " which is not belong to the xpath format,such as "//title's tr" or "//title tr",must be "//titletr" 

these bugs exist because lxml can not handle these situation
# 1.how it works
If a web do not have a rss,this project can get a rss source from the web

This project based on tornado and postgresql,after login,tornado shows you a html page which can be used to input the rss contents xpath css,after click save,the tornaodo will fetch the web contents use the "site_url",then get the articl title and article hyperlink,then tornado fetch every article from the article hyperlink,and generated a rss file.

I use postgresql stored the rss file's contents and its hyperlink,you can subscribe the rss  using the hyper link.
 
Every time interval in the config.py,tornado will regenerate the rss through the above process.

All process in tornado is async.
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
visit "http://localhost:8000/rss-from-web" ,input user_name:admin and password:password
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
# 6.todo
- fix the **only one** single or double quotes  in the xpath css
- fix the error when generate rss from the next web

```
```
- add the tornado log ,so that can debug easily
- add the xpath error to the browser when the some error happened
- add to the pypi library ,so that install easily
- construct a good document page
- reform the index.html,so that it looks more suitable
