from flask import Flask, send_from_directory, request, jsonify
import random

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('Client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('Client/public', path)

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))

"""
TODO Handle Register
Validate
user = { email, password, permission: "admin | permitted | user" };
Check if user not exist else return(string) errorMessage
Add user to db 
Return user data
"""


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        print("POST")
        data = request.get_json()
        print(data)
    else:
        print("NIE POST")


    email_server = data['email']
    password_server = data['password']
    print(email_server)
    print(password_server)
    return jsonify({
        'email': email_server,
        'password': password_server
    })

"""
TODO Handle Login
Validate
user = { email, password };
Return If ok user data else (string) errorMessage
"""

#TESTESTTEST
#asssssssfasfdssdaf


if __name__ == "__main__":
    app.run(debug=True)