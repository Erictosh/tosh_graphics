from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.message import EmailMessage
import os

EMAIL_ADDRESS = "toshgraphiics@gmail.com"  # replace with your Gmail
EMAIL_PASSWORD = "gxgr ukzv chsi yevh"   # replace with Gmail app password


app = Flask(__name__)  # This creates the Flask app
app.secret_key = 'my_secret_key'  # you can use any random string here

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Message {self.name}>'

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_content = request.form['message']

        # Save to database
        new_message = Message(name=name, email=email, message=message_content)
        db.session.add(new_message)
        db.session.commit()

        # Send email notification
        try:
            msg = EmailMessage()
            msg['Subject'] = 'New Contact Form Submission - Tosh Graphics'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS  # or another email to receive the messages
            msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_content}")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

            flash('✅ Your message has been sent successfully!')
        except Exception as e:
            flash(f'❌ Message saved, but failed to send email: {str(e)}')

        return redirect('/contact')
    
    return render_template('contact.html')


# Run the app + create DB
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
