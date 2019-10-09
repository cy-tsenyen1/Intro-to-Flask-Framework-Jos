from flask import Flask, redirect, render_template, request
app = Flask (__name__)

fellows = []
@app.route("/")
def index():
    name = request.args.get("name", "Tsenyen")
    return render_template("index.html", name=name)

@app.route("/registration")
def registeredfellows():
    return render_template("/registered.html", fellows=fellows)

@app.route ("/register", methods=["GET"])
def registerform():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name",)
    state = request.form.get("state")

    if not name or not state:
        return render_template("failure.html")
    fellows.append(f"{name} from {state} state of Nigeria")
    return redirect ("/registration")
      

# @app.route("/about_us", methods=["GET"])
# def about_us():
#     name = request.args.get("name")
#     return render_template("about_us.html")
    