#!/bin/bash
# update apt itself.
apt-get -y update
apt-get -y install git
apt-get -y install apache2
apt-get -y install php5-cli
apt-get -y install php5
apt-get -y install php5-mcrypt
sh -c 'echo "extension=mcrypt.so" >> /etc/php5/cli/php.ini'
sh -c 'echo "extension=mcrypt.so" >> /etc/php5/apache2/php.ini'
apt-get -y install mysql-client
apt-get -y install php5-mysql
debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'

apt-get -y install mysql-server
/etc/init.d/mysql start

aptitude -y install libapache2-mod-php5 php5 php5-common php5-curl php5-dev php5-gd \
php5-imagick php5-mcrypt php5-memcache php5-mhash php5-mysql php5-pspell php5-snmp \
php5-sqlite php5-xmlrpc php5-xsl
apt-get -y install mysql-server-core
aptitude -y install mysql-server
apt-get -y install beanstalkd
apt-get -y install sendmail 
apt-get -y install imagemagick
# for queue not to print errors. not sure why. 

a2enmod rewrite	

###### configuration

echo "create database {{environment['dbname']}}" | mysql --user=root --password=root

# run apache under vagrant user to avoid issues with permissions. 
sudo perl -pi -e 's/APACHE_RUN_USER=www-data/APACHE_RUN_USER=vagrant/' /etc/apache2/envvars
sudo perl -pi -e 's/APACHE_RUN_GROUP=www-data/APACHE_RUN_GROUP=vagrant/' /etc/apache2/envvars

#This will add the webserver to your apache2 000-default.conf file.
(
cat <<Endofmessage
<VirtualHost *:80>
    RewriteEngine On
    ServerName {{environment['name']}}
    ServerAdmin webmaster@localhost
    DocumentRoot {{environment['apache_root']}}/public
    DirectoryIndex index.php
    <Directory {{environment['apache_root']}}/public>
    AllowOverride All
    Options Indexes FollowSymLinks
    Require all granted
    </Directory>
    ErrorLog {{environment['log_dir']}}/error.log
    CustomLog {{environment['log_dir']}}/access.log combined
    Options +FollowSymLinks
    RewriteEngine On
    php_value memory_limit 2000M
</VirtualHost>
Endofmessage
) > /etc/apache2/sites-available/000-default.conf
# end of here doc.

hostname {{environment['site']}}
timedatectl set-timezone America/New_York
 
