from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Herb, Disease, HerbDiseaseAssociation
from forms import AddHerbForm, AddDiseaseForm, AddAssociationForm

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('您没有权限访问此页面。')
        return redirect(url_for('main.index'))
    return render_template('admin/dashboard.html')

@admin.route('/admin/add_herb', methods=['GET', 'POST'])
@login_required
def add_herb():
    if not current_user.is_admin:
        flash('您没有权限访问此页面。')
        return redirect(url_for('main.index'))
    form = AddHerbForm()
    if form.validate_on_submit():
        herb = Herb(name=form.name.data)
        db.session.add(herb)
        db.session.commit()
        flash('中药添加成功！')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/add_herb.html', form=form)

@admin.route('/admin/add_disease', methods=['GET', 'POST'])
@login_required
def add_disease():
    if not current_user.is_admin:
        flash('您没有权限访问此页面。')
        return redirect(url_for('main.index'))
    form = AddDiseaseForm()
    if form.validate_on_submit():
        disease = Disease(name=form.name.data)
        db.session.add(disease)
        db.session.commit()
        flash('疾病添加成功！')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/add_disease.html', form=form)

@admin.route('/admin/add_association', methods=['GET', 'POST'])
@login_required
def add_association():
    if not current_user.is_admin:
        flash('您没有权限访问此页面。')
        return redirect(url_for('main.index'))
    form = AddAssociationForm()
    if form.validate_on_submit():
        herb = Herb.query.filter_by(name=form.herb.data).first()
        disease = Disease.query.filter_by(name=form.disease.data).first()
        if herb and disease:
            association = HerbDiseaseAssociation(herb_id=herb.id, disease_id=disease.id)
            db.session.add(association)
            db.session.commit()
            flash('关联添加成功！')
        else:
            flash('中药或疾病不存在，请先添加。')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/add_association.html', form=form)