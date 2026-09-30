import os, sys, json
from flask import Flask, request, render_template, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from config import SECRET_KEY
from db import q, init_db
from fields import GROUPS, CODES
from ml_model.predictor import predict_age

app = Flask(__name__,
            template_folder=os.path.join(ROOT, "frontend", "templates"),
            static_folder=os.path.join(ROOT, "frontend", "static"))
app.secret_key = SECRET_KEY


def login_required(fn):
    def w(*a, **k):
        if "uid" not in session:
            return redirect(url_for("login"))
        return fn(*a, **k)
    w.__name__ = fn.__name__
    return w

# ---------- routes ----------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        n, e, p = request.form["name"].strip(), request.form["email"].strip().lower(), request.form["password"]
        if not (n and e and len(p) >= 6):
            flash("Fill all fields (password min 6 chars).")
        elif q("SELECT id FROM users WHERE email=%s", (e,), one=True):
            flash("Email already registered.")
        else:
            uid = q("INSERT INTO users (name,email,password_hash) VALUES (%s,%s,%s)",
                    (n, e, generate_password_hash(p)), commit=True)
            session.update(uid=uid, name=n)
            return redirect(url_for("calculator"))
    return render_template("auth.html", title="Register", register=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = q("SELECT * FROM users WHERE email=%s", (request.form["email"].strip().lower(),), one=True)
        if u and check_password_hash(u["password_hash"], request.form["password"]):
            session.update(uid=u["id"], name=u["name"])
            return redirect(url_for("calculator"))
        flash("Wrong email or password.")
    return render_template("auth.html", title="Login", register=False)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/calculator", methods=["GET", "POST"])
@login_required
def calculator():
    result = None
    if request.method == "POST":
        given = {}
        for code in CODES:
            v = request.form.get(code, "").strip()
            if v:
                given[code] = float(v)
        if "BMXHT" in given and "BMXWT" in given:            # BMI auto
            given["BMXBMI"] = round(given["BMXWT"] / (given["BMXHT"] / 100) ** 2, 1)
        bio = predict_age(given)          # ml_model folder nundi
        age = request.form.get("age", "").strip()
        gap = round(bio - float(age), 1) if age else None
        q("INSERT INTO predictions (user_id,real_age,predicted_age,age_gap,inputs_filled,inputs) VALUES (%s,%s,%s,%s,%s,%s)",
          (session["uid"], int(age) if age else None, bio, gap, len(given), json.dumps(given)), commit=True)
        result = dict(bio=bio, gap=gap, age=age, used=len(given))
    return render_template("calculator.html", groups=GROUPS, result=result)

@app.route("/history")
@login_required
def history():
    rows = q("SELECT * FROM predictions WHERE user_id=%s ORDER BY id DESC LIMIT 50", (session["uid"],))
    return render_template("history.html", rows=rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
