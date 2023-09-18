from flask_app import app
from flask import Flask, render_template,redirect, request , session
# import the class 'Cookies' from folder 'flask_app/models/user.py
from flask_app.models.cookie import Cookies 


@app.route("/")
def home():
   return redirect('/cookie/new')


@app.route("/cookies")
def index():
   cookies = Cookies.get_all()
   session.clear()
   return render_template("index.html",all_cookies = cookies)


@app.route("/cookie/new")
def create_new_cookie():
   return render_template("create.html")



@app.route('/new', methods=["POST"])
def create():
    datass = {
        "name": request.form["name"],
        "type": request.form["type"],
        "nboxes": request.form["nboxes"]
    }

    if not Cookies.validate_cookie_infos(datass) or not Cookies.is_unique_user(datass) : # ADD 'VALIDATE' METHOD COOKIES_INFOS AND UNIQUE USER 

        session["name"] = request.form["name"]
        session["type"] = request.form["type"]
        session["nboxes"] = request.form["nboxes"]
        return redirect("/")
    
    Cookies.create_cookie(datass)

    return redirect('/cookies')


@app.route('/cookie/show/<int:cookie_id>')
def show(cookie_id):
    data = {'id': cookie_id}
    cookie = Cookies.get_one(data)
    session.clear()
    return render_template("show_cookie.html", Cookie = cookie)
    


@app.route('/cookie/update/<int:cookie_id>')
def show_update_page(cookie_id):
    data = {'id': cookie_id}
    cookie = Cookies.get_one(data)
    return render_template("update_cookie.html", Cookie = cookie)


@app.route('/edit/<int:cookie_id>',methods=['POST'])
def update(cookie_id):
    data = {
        'name': request.form['name_c'],
        'type': request.form['type_c'],
        'nboxes': request.form['nboxes_c'],
        'id': cookie_id,
    }

    if not Cookies.validate_cookie_infos(data) or not Cookies.is_unique_user(data) : # ADD 'VALIDATE' METHOD COOKIES_INFOS AND UNIQUE USER 

        session["name_updt"] = request.form["name_c"]
        session["type_updt"] = request.form["type_c"]
        session["nboxes_updt"] = request.form["nboxes_c"]

        return redirect(f"/cookie/update/{cookie_id}")

    Cookies.update(data)

    return redirect(f'/cookie/show/{cookie_id}')



@app.route('/cookie/delete/<int:cookie_id>')
def delete(cookie_id):
    data = {"id": cookie_id}
    Cookies.delete(data)
    return redirect('/cookies')



@app.errorhandler(404)  # we specify in parameter here the type of error, here it is 404
def page_not_found(
    error,
):  # (error) is important because it recovers the instance of the error that was thrown
    return f"<h2 style='text-align:center;padding-top:40px'>Error 404. Sorry! No response. Try again</h2>"    

