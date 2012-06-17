import urllib, urllib2, cookielib

username = 'cwhiteside'
password = 'stspassword'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'UserName' : username, 'Password' : password})
opener.open('http://www.kyozou.com/index.php/main/login-seller.html', login_data)
resp = opener.open('http://my1.kyozou.com/Modules/Inventory/startaddproduct.aspx?tid=1')
print resp.read() 
