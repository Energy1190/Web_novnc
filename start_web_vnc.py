from functools import wraps
from flask import request, Response, Flask, redirect, render_template, url_for, send_from_directory
from ldap3 import ALL, NTLM, Tls, Connection, Server
import ssl
import sys
import subprocess
import os

app = Flask(__name__)
conn_server = str(os.environ['LDAP_SERVER']).split(sep="://")
if conn_server[0] == "ldaps":
    try:
        ca = os.environ['CA']
    except:
        print("You must specify the path to certificate")
        sys.exit(1)
port = os.environ['VNC_PORT']
web_port = int(port) + 1000

def connect_server (conn_user, conn_passwd, ca=None, conn_server=None):
    if ca:
        tls = Tls(validate=ssl.CERT_REQUIRED, ca_certs_file=ca)
        port = 636
        use_ssl = True
    else:
        tls = None
        port = 389
        use_ssl = False
    try:
        serverN = Server(conn_server, tls=tls, get_info=ALL, port=port, use_ssl=use_ssl)
        conn = Connection(serverN, user='ISL\\' + conn_user, password=conn_passwd, authentication=NTLM, auto_bind=True)
        conn.start_tls()
    except:
        return False
    return conn_user == conn_user and conn_passwd == conn_passwd

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not connect_server(auth.username, auth.password, ca=ca, conn_server=conn_server[1]):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
@app.route("/include/webutil.js", methods=['GET'])
def js_lib():
    return app.send_static_file('include/webutil.js')

@app.route("/include/base64.js", methods=['GET'])
def js_lib1():
    return app.send_static_file('include/base64.js')

@app.route("/include/websock.js", methods=['GET'])
def js_lib2():
    return app.send_static_file('include/websock.js')

@app.route("/include/des.js", methods=['GET'])
def js_lib3():
    return app.send_static_file('include/des.js')

@app.route("/include/keysymdef.js", methods=['GET'])
def js_lib4():
    return app.send_static_file('include/keysymdef.js')

@app.route("/include/keyboard.js", methods=['GET'])
def js_lib5():
    return app.send_static_file('include/keyboard.js')

@app.route("/include/input.js", methods=['GET'])
def js_lib6():
    return app.send_static_file('include/input.js')

@app.route("/include/display.js", methods=['GET'])
def js_lib7():
    return app.send_static_file('include/display.js')

@app.route("/include/rfb.js", methods=['GET'])
def js_lib8():
    return app.send_static_file('include/rfb.js')

@app.route("/include/keysym.js", methods=['GET'])
def js_lib9():
    return app.send_static_file('include/keysym.js')

@app.route("/include/inflator.js", methods=['GET'])
def js_lib10():
    return app.send_static_file('include/inflator.js')

if os.environ["LDAP_AUTH"]:
    @app.route("/", methods=['GET', 'POST'])
    @requires_auth
    def hello():
        path = '/web_noVNC/websockify.py'
        listen_port = str(int(port) + 10)
        vnc_server = '127.0.0.1:' + str(port)
        listen = '0.0.0.0:' + listen_port
        subprocess.Popen(['python3.4', path, listen, vnc_server, '--run-once'])
        return render_template('vnc.html', listen_port=listen_port)

else:
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        path = '/web_noVNC/websockify.py'
        listen_port = str(int(port) + 10)
        vnc_server = '127.0.0.1:' + str(port)
        listen = '0.0.0.0:' + listen_port
        subprocess.Popen(['python3.4', path, listen, vnc_server, '--run-once'])
        return render_template('vnc.html', listen_port=listen_port)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=web_port)
