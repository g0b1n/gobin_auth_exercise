from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    """Create acct form"""

    #added later
    first_name = StringField("First Name", validators=[InputRequired(message="First name must be entered"), Length(max=20)])
    last_name = StringField("Last Name", validators=[InputRequired(message="Last name must be entered"), Length(max=20)])
    email = StringField("Email", validators=[InputRequired(message="Email must be entered"), Email(), Length(max=50)])

    username = StringField("Username", validators=[InputRequired(message="Username must be entered"), Length(min=1, max=20)])
    password = PasswordField("Create Password", validators=[InputRequired(message="Password must be entered"), Length(min=8, max=20)])
    confirm_pwd = PasswordField("Confirm Password", validators=[InputRequired(message="Please confirm password"), EqualTo('password', message='Password must match')])
    
    


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField("Username", validators=[InputRequired(message="Username must be entered"), Length(min=1, max=20)])
    password = PasswordField("Create Password", validators=[InputRequired(message="Password must be entered"), Length(min=8, max=20)])



class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )


class DeleteForm(FlaskForm):
    """Delete form -- blank"""