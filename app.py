from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from models import db, User, Teacher, Class, Enrollment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

# init db
db.init_app(app)

# migrations
migrate = Migrate(app, db)

# admin
admin = Admin(app, name="Dashboard")
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Class, db.session))
admin.add_view(ModelView(Enrollment, db.session))

# create tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/users")
def users():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)

if __name__ == "__main__":
    app.run(debug=True)