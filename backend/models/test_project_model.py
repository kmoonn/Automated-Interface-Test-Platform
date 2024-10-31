from datetime import datetime

from backend.app import db


class TestProjectModel(db.Model):
    __tablename__ = 'test_project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    isDeleted = db.Column(db.Boolean, default=False, nullable=True)
    status = db.Column(db.Boolean, default=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=True)
    operation = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return '<TestProjectModel %r>' % self.project_name

    def to_dict(self):
        return {tcm.name: getattr(self, tcm.name) for tcm in TestProjectModel.__table__.columns}
