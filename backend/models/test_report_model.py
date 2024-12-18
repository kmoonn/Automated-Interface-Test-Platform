import datetime
from backend.app import db


class TestReportModel(db.Model):
    __tablename__ = 'test_report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_name = db.Column(db.String(50), nullable=False)
    report_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    project_name = db.Column(db.String(50), nullable=False)
    case_count = db.Column(db.Integer, nullable=False)
    pass_count = db.Column(db.Integer, nullable=False)
    fail_count = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    operator = db.Column(db.String(50), nullable=True)
    conclusion = db.Column(db.String(50), nullable=True)
    total_time = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=True)
    case_data = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<TestReportModel %r>' % self.report_name

    def to_dict(self):
        return {tcm.name: getattr(self, tcm.name) for tcm in TestReportModel.__table__.columns}
