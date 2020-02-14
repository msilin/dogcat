#!/usr/bin/python3
from flask import request, after_this_request, url_for, redirect, make_response
from flask import jsonify
from flask import Flask
from flask import render_template
import json

from datetime import datetime
app = Flask(__name__)

user_id=0
@app.route("/")
def index():
 
    return render_template('index.html') 
        

@app.route('/img/<name>')
def hello(name):

    return redirect("/") 
    #return '<a href=/> </a>' 
@app.after_request
def after_request_func(response):
    global user_id
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

   # cookie = request.cookies.get("user_cookie")
    cookie = request.cookies.get("bot_cookie")
        
    if not cookie:
        cookie = time
        response.set_cookie( "bot_cookie", cookie,  max_age=60*60*24*365*2)
    

    if ( str(request.path).startswith('/img')):
        f = open("app.log", "a+")
        f.write("**********************************************\n" + str(request.path))
        
        f.write ("\nMMMM COOKIE " + cookie + " @@@\n")
        f.write ("time: " + time + " \n")
        
        f.write("\n" + str(request.headers) + "\n")
        f.close()


    return response

if __name__ == '__main__':
    # Will make the server available externally as well
    app.run(host='0.0.0.0')
