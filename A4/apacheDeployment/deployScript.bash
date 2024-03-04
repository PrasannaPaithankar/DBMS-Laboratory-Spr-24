#!/usr/bin/bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install python3-venv
sudo apt-get install git
sudo apt-get install python3-pip
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

cd /var/www/html
sudo git clone https://github.com/PrasannaPaithankar/DBMS-Laboratory-Spr-24 DBMSweb
cd DBMSweb
sudo python3 -m venv venv
sudo chmod -R a+rwx ../DBMSweb
source venv/bin/activate
pip3 install -r ./requirements.txt
deactivate

sudo cp ./apacheDeploy/DBMSweb.conf /etc/apache2/sites-available
sudo a2ensite DBMSweb.conf
sudo a2dissite 000-default.conf
sudo certbot --apache
sudo service apache2 restart