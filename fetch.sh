#! /usr/bin/bash

dmidecode > dmid

dmidecode -t1 | grep -E "Manufac|Product" | awk '
BEGIN{ FS=": "}
{print $2}' > inf

dmidecode -t4 | grep -E "Socket Des|Family:|Manufac|Max Speed|Voltage" | awk '
BEGIN{ FS=": "}
{print $2}' >> inf

cat dmid | grep -i -E -c1 "Bluetooth" >> inf
cat dmid | grep -i -E -c1 "1394" >> inf

dmidecode -t17 | grep -E "Type:" | awk '
BEGIN{FS=": ";print $2}{}
END{print $2;
print NF}'>> inf

dmidecode -t17 | grep -E "Size:" | awk '
BEGIN{FS=": ";ORS=", "}
{if(FNR==NF) ORS=" ";
print $2}' >> inf

rm -f dmid

python run.py