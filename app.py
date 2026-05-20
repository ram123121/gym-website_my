from flask import Flask, render_template, request, redirect, url_for, flash
import os
import resend

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

EMAIL = os.environ.get("EMAIL")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

resend.api_key = RESEND_API_KEY


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/timing")
def timing():
    return render_template("class-timetable.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        comment = request.form.get("comment")

        # validation
        if not name or not email or not phone_number or not comment:
            flash("Please fill all the fields")
            return redirect(url_for("contact"))

        if "@" not in email:
            flash("Please enter a valid email")
            return redirect(url_for("contact"))

        try:

            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": EMAIL,
                "subject": f"New message from {name}",
                "html": f"""
                <h2>New Contact Form Message</h2>

                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Phone Number:</strong> {phone_number}</p>

                <h3>Comment:</h3>
                <p>{comment}</p>
                """
            })

            flash("Message sent successfully")
            return redirect(url_for("home"))

        except Exception as e:
            app.logger.error(e)
            flash("Something went wrong. Please try again.")
            return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/404")
def error():
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)