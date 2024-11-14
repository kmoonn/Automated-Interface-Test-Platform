from datetime import datetime

from backend.app import db


class TestCaseModel(db.Model):
    __tablename__ = 'test_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(20), default='GET', nullable=False)
    protocol = db.Column(db.String(20), default='HTTP', nullable=False)
    host = db.Column(db.String(50), nullable=True)
    port = db.Column(db.String(10), nullable=True)
    path = db.Column(db.String(100), default='/', nullable=True)
    params = db.Column(db.String(50), nullable=True)
    headers = db.Column(db.String(500), nullable=True)
    body = db.Column(db.String(500), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    predict = db.Column(db.String(500), nullable=True)
    isDeleted = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(10), default=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None)
    operator = db.Column(db.String(50), nullable=True)

    suite_id = db.Column(db.Integer, db.ForeignKey('test_suite.id'))
    suite = db.relationship('TestSuiteModel', backref=db.backref('test_case', lazy='dynamic'))

    def __repr__(self):
        return '<TestCaseModel %r>' % self.case_name

    def to_dict(self):
        return {tcm.name: getattr(self, tcm.name) for tcm in TestCaseModel.__table__.columns}
