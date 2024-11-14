from backend.app import db


class TestUserModel(db.model):
    __tablename__ = 'test_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {tcm.name: getattr(self, tcm.name) for tcm in TestUserModel.__table__.columns}