from flask import render_template, request, redirect, flash
from flask.helpers import url_for


from app import app, db


from .forms import CaseForm, RegisterForm, FacilityForm
from .models import Register, Case, Facility


def page():
    page_str = request.args.get('page')
    try:
        page = int(page_str)
    except (ValueError, TypeError):
        page = 1
    return page


@app.route("/registers")
def list_registers():
    items = Register.query.paginate(page(), app.config.get('RECORDS_ON_PAGE'))

    return render_template(
        "cases/list_registers.html",
        items=items,
        add=url_for("edit_register"),
    )


@app.route("/register/edit/<int:register_id>", methods=["GET", "POST", ])
@app.route("/register/edit/<string:fund_title>/<int:fund_register>")
@app.route("/register/add", methods=["GET", "POST", ])
def edit_register(register_id=None, fund_title=None, fund_register=None):
    if fund_title is not None:
        register = Register.query \
            .filter(Register.fund == fund_title) \
            .filter(Register.register == fund_register) \
            .first_or_404()
    elif register_id is not None:
        register = Register.query.get_or_404(register_id)
    else:
        register = Register()
    form = RegisterForm(obj=register)

    if form.validate_on_submit():
        form.populate_obj(register)
        db.session.add(register)
        if register.id:
            flash("Опись изменена", 'success')
        else:
            flash("Опись добавлена", 'success')
        db.session.commit()
        return redirect(url_for("list_registers"))

    app.logger.debug(form.errors)
    return render_template(
        "cases/edit_register.html",
        form=form,
        register=register,
        items = Case.query.filter_by(register=register).paginate(page(), app.config.get('RECORDS_ON_PAGE'))
    )


@app.route("/register/<int:register_id>")
@app.route("/register/<string:fund_title>/<int:fund_register>")
def view_register(register_id=None, fund_title=None, fund_register=None):
    if fund_title is not None:
        register = Register.query \
            .filter(Register.fund == fund_title) \
            .filter(Register.register == fund_register) \
            .first_or_404()
    else:
        register = Register.query.get_or_404(register_id)

    return render_template(
        "cases/list_cases.html",
        register=register,
        items = Case.query.filter_by(register=register).paginate(page(), app.config.get('RECORDS_ON_PAGE'))
    )


@app.route("/register/del/<int:register_id>")
def del_register(register_id=None):
    register = Register.query.get_or_404(register_id)
    db.session.delete(register)
    db.session.commit()
    flash("Опись удалена", 'danger')
    return redirect(url_for("list_registers"))


@app.route("/facilities")
def list_facilities():
    items = Facility.query.paginate(page(), app.config.get('RECORDS_ON_PAGE'))

    return render_template(
        "cases/list_facilities.html",
        items=items,
        add=url_for("edit_facility"),
    )


@app.route("/facility/edit/<int:facility_id>", methods=["GET", "POST", ])
@app.route("/facility/add", methods=["GET", "POST", ])
def edit_facility(facility_id=None):
    if facility_id is not None:
        facility = Facility.query.get_or_404(facility_id)
    else:
        facility = Facility()
    form = FacilityForm(obj=facility)

    if form.validate_on_submit():
        form.populate_obj(facility)
        db.session.add(facility)
        if facility.id:
            flash("Предприятие изменено", 'success')
        else:
            flash("Предприятие добавлено", 'success')
        db.session.commit()
        return redirect(url_for("list_facilities"))

    app.logger.debug(form.errors)
    return render_template(
        "cases/edit_facility.html",
        form=form,
        facility=facility,
        items = Case.query.filter_by(facility=facility).paginate(page(), app.config.get('RECORDS_ON_PAGE'))
    )


@app.route("/facility/<int:facility_id>")
def view_facility(facility_id=None):
    facility = Facility.query.get_or_404(facility_id)

    return render_template(
        "cases/list_cases.html",
        facility=facility,
        items = Case.query.filter_by(facility=facility).paginate(page(), app.config.get('RECORDS_ON_PAGE'))
    )


@app.route("/facility/del/<int:facility_id>")
def del_facility(facility_id=None):
    facility = Facility.query.get_or_404(facility_id)
    db.session.delete(facility)
    db.session.commit()
    flash("Предприятие удалено", 'danger')
    return redirect(url_for("list_facilities"))


@app.route("/register/<int:register_id>/cases")
@app.route("/register/<string:fund_title>/<int:fund_register>/cases")
@app.route("/cases")
def list_cases(register_id=None, fund_title=None, fund_register=None):
    q = Case.query
    if fund_title is not None:
        register = Register.query \
            .filter(Register.fund == fund_title) \
            .filter(Register.register == fund_register) \
            .first()
        q = q.filter(Case.register_id == register.id)
    elif register_id is not None:
        app.logger.debug(q)
        q = q.filter(Case.register_id == register_id)
        app.logger.debug(q)
    items = q.paginate(page(), app.config.get('RECORDS_ON_PAGE'))

    app.logger.debug(items)
    return render_template(
        "cases/list_cases.html",
        items=items,
        add=url_for("edit_case"),
    )


@app.route("/case/edit/<int:case_id>", methods=["GET", "POST", ])
@app.route("/case/edit/<string:fund_title>/<int:fund_register>/<int:case_num>")
@app.route("/case/add/<int:register_id>", methods=["GET", "POST", ])
@app.route("/case/add", methods=["GET", "POST", ])
def edit_case(
    case_id=None,
    case_num=None,
    fund_title=None,
    fund_register=None,
    register_id=0
):

    if fund_title is not None:
        register = Register.query \
            .filter(Register.fund == fund_title) \
            .filter(Register.register == fund_register) \
            .first_or_404()
        case = Case.query \
            .filter(Case.register_id == register.id) \
            .filter(Case.case_num == case_num) \
            .first_or_404()
        case.normalize()
    elif case_id is not None:
        case = Case.query.get_or_404(case_id)
        case.normalize()
    else:
        case = Case()
    form = CaseForm(obj=case)

    if form.validate_on_submit():
        form.populate_obj(case)
        if form.register.data:
            case.register_id = form.register.data.id
        if form.facility.data:
            case.facility_id = form.facility.data.id
        case.normalize()
        db.session.add(case)
        if case.id:
            flash("Опись изменена", 'success')
        else:
            flash("Опись добавлена", 'success')
        db.session.commit()
        return redirect(url_for("list_cases"))

    case.normalize()
    if register_id:
        register = Register.query.get(register_id)
        form.register.data = register
    app.logger.debug(form.errors)

    return render_template("cases/edit_case.html", form=form, case=case)


@app.route("/case/<int:case_id>")
@app.route("/case/<string:fund_title>/<int:fund_register>/<int:case_num>")
def view_case(case_id=None, fund_title=None, fund_register=None, case_num=None):
    if fund_title is not None:
        register = Register.query \
            .filter(Register.fund == fund_title) \
            .filter(Register.register == fund_register) \
            .first_or_404()
        case = Case.query \
            .filter(Case.register_id == register.id) \
            .filter(Case.case_num == case_num) \
            .first_or_404()
    else:
        case = Case.query.get_or_404(case_id)

    return render_template(
        "cases/view_case.html",
        case=case,
    )


@app.route("/case/del/<int:case_id>")
def del_case(case_id=None):
    case = Case.query.get_or_404(case_id)
    db.session.delete(case)
    db.session.commit()
    flash("Дело удалено", 'danger')
    return redirect(url_for("list_cases"))
