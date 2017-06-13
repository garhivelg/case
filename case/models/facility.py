from app import db
import random


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), info={'label': "Предприятие"})
    description = db.Column(db.UnicodeText, info={'label': "Примечания"})

    cases = db.relationship("Case", backref="facility")

    def __repr__(self):
        return self.title

    def randomize(self, fake):
        self.title = fake.company()
        chance = random.randint(0, 100)
        if chance < 25:
            self.description = "\n".join(fake.paragraphs())
