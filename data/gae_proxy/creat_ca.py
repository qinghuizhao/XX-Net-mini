import os
import platform
import subprocess

def runcmd(cmd):
	p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE , stderr=subprocess.PIPE)
	stdout, stderr = p.communicate()
	return (stdout, stderr,p.returncode)

cmd = "openssl req -x509 -newkey rsa:2048 -sha256 -days 3650 -set_serial 01 -nodes -keyout CA.key -out CA.crt -extensions v3_req -config ca_openssl.config"
runcmd(cmd)
cmd = "openssl genrsa  -out p.key 2048"
runcmd(cmd)
cmd = "openssl rsa -in p.key -pubout -out pub.key"
runcmd(cmd)


filenames = ['CA.crt', 'CA.key']
with open('CAkey.pem', 'wb') as outfile:
    for fname in filenames:
        with open(fname, 'rb') as infile:
            outfile.write(infile.read())

filenames = ['p.key', 'pub.key']
with open('Certkey.pem', 'wb') as outfile:
    for fname in filenames:
        with open(fname, 'rb') as infile:
            outfile.write(infile.read())

os.remove('CA.key')
os.remove('p.key')
os.remove('pub.key')

if(platform.system()=='Windows'):
    cmd = "certmgr /c /add CA.crt /s root"
    runcmd(cmd)
elif(platform.system()=='Linux'):
    cmd = 'certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n GoAgent-XX-Net-mini-4.5.2 -i CA.crt'
    runcmd(cmd)
else:
    pass
