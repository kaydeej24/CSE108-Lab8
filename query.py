from app import db, User
# Queries all users
User.query.all()
# Queries first user
User.query.filter_by(username='admin').first()