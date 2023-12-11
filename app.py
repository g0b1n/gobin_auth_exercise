from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
# db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'authExercise'
# debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///my_auth'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home_page():

    return redirect(url_for('login_user'))



@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register new user. Render and handle form submission for new users"""

    if 'username' in session:
        return redirect(f"/users/{session['username']}")


    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        # db.session.add(new_user)
        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")
    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Render and handle login form"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f'Welcome Back, { user.username }', 'primary')
            session['username'] = user.username #stores username in session
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid Username or Password']
            return render_template("users/login.html", form=form)
    
    return render_template("users/login.html", form=form)


@app.route('/logout')
def logout_user():
    """Logout user"""

    session.pop('user_id', None)
    session.pop('username', None)
    flash("Successfully logged out", 'info')
    return redirect('/')




@app.route('/users/<username>')
def show_user(username):
    """users page to display their info"""

    if "username" not in session or username != session['username']:
        return render_template('404.html')
    
    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)



@app.route("/users/<username>/delete", methods=['POST'])
def remove_user(username):
    """Remove/delete a username and redirec user to login page"""

    if "username" not in session or username != session['username']:
        return render_template('404.html')
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect('/login')


@app.route('/users/<username>/feedback/new', methods=['GET', 'POST'])
def new_feedback(username):
    """show form to add feedback"""

    if "username" not in session or username != session['username']:
        return render_template('404.html')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title = title,
            content = content,
            username = username
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback/new.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """render a form to edit feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return render_template('404.html')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=['POST'])
def delete_feedback(feedback_id):
    """delete feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return render_template('404.html')

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f"/users/{feedback.username}")



# THE END 
if __name__ == '__main__':
    app.run(debug=True)