from app import manager, db
from faker import Factory
import random


from .models import Register, Case, Facility


@manager.command
def fill():
    "Fill db with sample data"
    print("hello")
    fake = Factory.create('ru_RU')

    facilities = []
    facility_count = random.randint(10, 100)
    for facility_id in range(facility_count):
        facility = Facility()
        facility.randomize(fake)

        print("Facility#%d of %d: %s" % (facility_id, facility_count, facility))
        db.session.add(facility)
        facilities.append(facility)
    db.session.commit()

    registers = random.randint(10, 100)
    for register_id in range(registers):
        register = Register()
        register.randomize(fake)

        print("Record#%d of %d: %s" % (register_id, registers, register))
        db.session.add(register)
        db.session.commit()

        cases = random.randint(1, 100)
        for case_id in range(cases):
            case = Case()
            case.randomize(fake)
            case.register = register

            chance = random.randint(0, 100)
            if chance < 25:
                case.facility = random.choice(facilities)

            print("\tCase#%d of %d: %s" % (case_id, cases, case))
            db.session.add(case)
        db.session.commit()
