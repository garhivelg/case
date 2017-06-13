from app import db


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), info={'label': "Предприятие"})
    description = db.Column(db.UnicodeText, info={'label': "Примечания"})

    cases = db.relationship("Case", backref="facility")

    def __repr__(self):
        return self.title
