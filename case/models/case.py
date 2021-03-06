from app import db
import random


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund = db.Column(db.String(8), info={'label': "Фонд"})
    register = db.Column(db.Integer(), info={'label': "Опись"})
    description = db.Column(db.UnicodeText, info={'label': "Примечания"})

    def title(self, format="ф. %s оп. %s"):
        return format % (self.fund, self.register)

    def __repr__(self):
        return self.title()

    def randomize(self, fake):
        letter = chr(random.randint(ord('а'), ord('я')))
        self.fund = "%s-%d" % (letter, fake.pyint())
        self.register = fake.pyint()
        chance = random.randint(0, 100)
        if chance < 25:
            self.description = "\n".join(fake.paragraphs())

    def import_yml(self, data=dict()):
        self.fund = data.get('fund')
        self.register = data.get('register')
        self.description = data.get('description')


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_id = db.Column(db.Integer, db.ForeignKey('register.id'))
    book_id = db.Column(db.String(8), info={'label': "Дело №"})
    book_num = db.Column(db.Integer, nullable=False, default=0)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    description = db.Column(db.UnicodeText, info={'label': "Примечания"})

    register = db.relationship("Register", backref="cases")
    # facility = db.relationship("Facility")

    def title(self, format="%s д. %s"):
        book_num = self.case_id_txt
        if self.register:
            return format % (self.register, book_num)
        return format % ('', book_num)

    def __repr__(self):
        return self.title()

    def randomize(self, fake):
        # book_id
        self.book_num = fake.pyint()
        # facility_id
        chance = random.randint(0, 100)
        if chance < 25:
            self.description = "\n".join(fake.paragraphs())

    @property
    def case_id_txt(self):
        if not self.book_id:
            if self.book_num:
                return self.book_num
            else:
                return ""
        return self.book_id

    def normalize(self):
        if not self.book_id:
            self.book_id = self.book_num
            return
        
        try:
            res = int(''.join(c for c in str(self.book_id) if c.isdigit()))
        except ValueError:
            res = 0
        self.book_num = res

    def import_yml(self, data=dict()):
        self.book_id = data.get('book')
        self.facility_id = data.get('facility')
        self.description = data.get('description')
