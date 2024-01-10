from flask import Flask, render_template, g
from flask_oidc import OpenIDConnect

app = Flask(__name__)

#This is the minimum configurations required to run the application
app.config.update({
  "PREFERRED_URL_SCHEME": "https", #To enable https with the localhost server
  "OIDC_CLIENT_SECRETS": "client_secrets.json", #You can change the json name if you want, it doesn't need to be client_secrets, just ensure it's a json file.
  "SECRET_KEY": "secret", #The secret key is necessary to use a session in flask.
  'OIDC_ID_TOKEN_COOKIE_SECURE': True #If the cookie isn't secure w3id won't work within your project
}) 

#We pass our app configuration to the OpenIdConnect class, this class comes from the flask_oidc
oidc = OpenIDConnect(app) 

@app.route('/')
@oidc.require_login #This is what tells the program that the w3id SSO needs to be done in order to perform this function
def index():
    if oidc.user_loggedin: #This is a flag that determines if the user logged in or not
        return render_template('index.html',token = g.oidc_id_token) #g.oidci_id_token returns the de-hashed id token.
    else:
        return 'Not Logged in' #If we take the @oidc.require_login from the function this message will show.

if __name__ == "__main__": #This is just a validation to check if this is the main application.
    #In order to run a https connection the certificates need to be attached when running the application
    app.run(ssl_context=('certificate.pem','key.pem'),debug=True)
