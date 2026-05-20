

from flask import Flask, render_template,request,redirect,url_for,flash
import smtplib
import os
app=Flask(__name__)
app.config["SECRET_KEY"]=os.environ.get("SECRET_KEY")
PASSWORD=os.environ.get("PASSWORD")
EMAIL=os.environ.get("EMAIL")
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
@app.route("/contact",methods=["GET","POST"])
def contact():
    
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        phone_number=request.form.get("phone_number")
        comment=request.form.get("comment")
        
        if not name or not email or not phone_number or not comment:
            flash("Please fill all the fields")
            
            return render_template("contact.html")
        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(EMAIL, PASSWORD)

                msg = f"""Subject: New message from {name}

                    Name: {name}
                    Email: {email}
                    Phone number: {phone_number}

                    Comment:
                    {comment}
                    """

                smtp.sendmail(EMAIL, EMAIL, msg)

            flash("Message sent successfully")
            return redirect(url_for("home"))

        except Exception as e:
            print(e)
            flash("Something went wrong. Please try again.")
            return redirect(url_for('home')) 
    return render_template("contact.html")
@app.route("/404")
def error():
    return render_template("404.html")
if __name__=="__main__":
    app.run(debug=True)