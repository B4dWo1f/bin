#!/bin/bash


wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz -P /tmp
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz -P /tmp
wget http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz -P /tmp

gunzip /tmp/GeoIP.dat.gz
gunzip /tmp/GeoIPASNum.dat.gz
gunzip /tmp/GeoLiteCity.dat.gz

sudo mv /tmp/GeoIP.dat /usr/share/GeoIP/
sudo mv /tmp/GeoIPASNum.dat /usr/share/GeoIP/
sudo mv /tmp/GeoLiteCity.dat /usr/share/GeoIP/
