from datetime import datetime

from backend.app import db


class TestSuiteModel(db.Model):
    __tablename__ = 'test_suite'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    suite_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.Boolean, default=True, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    operator = db.Column(db.String(20), nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('test_project.id'), nullable=False)
    project = db.relationship('TestProjectModel', backref=db.backref('test_suite'))

    def __repr__(self):
        return '<TestSuiteModel %r>' % self.suite_name

    def to_dict(self):
        return {tcm.name: getattr(self, tcm.name) for tcm in TestSuiteModel.__table__.columns}
