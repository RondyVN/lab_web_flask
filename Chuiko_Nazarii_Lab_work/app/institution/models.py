import enum

from .. import db


class Categoryacr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(50), nullable=False)
    inst = db.relationship('Institution', backref='category', lazy=True)


class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_inst = db.Column(db.String(50), nullable=False)
    info = db.Column(db.Text, nullable=True)
    count_student = db.Column(db.Integer())
    city = db.Column(db.String(50), nullable=False)
    military_department = db.Column(db.Boolean, default=True, nullable=False)
    category_acr_id = db.Column(db.Integer, db.ForeignKey('categoryacr.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.name_inst}')"
