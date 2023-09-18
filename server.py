from flask_app import app  

from flask_app.controllers import cookies 

if __name__ == "__main__":  
    app.run(debug=True, port=4000)

