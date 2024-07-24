from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Herb, Disease, HerbDiseaseAssociation
from forms import AddHerbForm, AddDiseaseForm, AddAssociationForm, BulkAddHerbForm, BulkAddDiseaseForm

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

@admin.route('/manage_herbs')
@login_required
def manage_herbs():
    herbs = Herb.query.all()
    return render_template('admin/manage_herbs.html', herbs=herbs)

@admin.route('/manage_diseases')
@login_required
def manage_diseases():
    diseases = Disease.query.all()
    return render_template('admin/manage_diseases.html', diseases=diseases)

@admin.route('/manage_associations')
@login_required
def manage_associations():
    associations = Herb.query.all()
    return render_template('admin/manage_associations.html', associations=associations)

@admin.route('/edit_herb/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_herb(id):
    herb = Herb.query.get_or_404(id)
    form = AddHerbForm(obj=herb)
    if form.validate_on_submit():
        herb.name = form.name.data
        db.session.commit()
        flash('中药更新成功')
        return redirect(url_for('admin.manage_herbs'))
    return render_template('admin/edit_herb.html', form=form)

@admin.route('/delete_herb/<int:id>')
@login_required
def delete_herb(id):
    herb = Herb.query.get_or_404(id)
    db.session.delete(herb)
    db.session.commit()
    flash('中药删除成功')
    return redirect(url_for('admin.manage_herbs'))

@admin.route('/edit_diseases/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_diseases(id):
    disease = Disease.query.get_or_404(id)
    form = AddDiseaseForm(obj=disease)
    if form.validate_on_submit():
        disease.name = form.name.data
        db.session.commit()
        flash('疾病更新成功')
        return redirect(url_for('admin.manage_diseases'))
    return render_template('admin/edit_diseases.html', form=form)

@admin.route('/delete_diseases/<int:id>')
@login_required
def delete_diseases(id):
    disease = Disease.query.get_or_404(id)
    db.session.delete(disease)
    db.session.commit()
    flash('疾病删除成功')
    return redirect(url_for('admin.manage_diseases'))

@admin.route('/edit_association/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_association(id):
    association = HerbDiseaseAssociation.query.get_or_404(id)
    form = AddAssociationForm(obj=association)
    if form.validate_on_submit():
        association.name = form.name.data
        db.session.commit()
        flash('关联更新成功')
        return redirect(url_for('admin.manage_associations'))
    return render_template('admin/edit_association.html', form=form)

@admin.route('/delete_association/<int:id>')
@login_required
def delete_association(id):
    association = HerbDiseaseAssociation.query.get_or_404(id)
    db.session.delete(association)
    db.session.commit()
    flash('关联删除成功')
    return redirect(url_for('admin.manage_associations'))

@admin.route('/admin/bulk_add_herbs', methods=['GET', 'POST'])
@login_required
def bulk_add_herbs():
    if not current_user.is_admin:
        flash('您没有权限访问此页面。')
        return redirect(url_for('main.index'))
    form = BulkAddHerbForm()
    if form.validate_on_submit():
        herbs = form.herbs.data.split('\n')
        added_count = 0
        skipped_count = 0
        for herb_name in herbs:
            herb_name = herb_name.strip()
            if herb_name:
                existing_herb = Herb.query.filter_by(name=herb_name).first()
                if existing_herb:
                    skipped_count += 1
                else:
                    herb = Herb(name=herb_name)
                    db.session.add(herb)
                    added_count += 1
        db.session.commit()
        flash(f'中药批量添加完成！成功添加 {added_count} 个，跳过 {skipped_count} 个已存在的中药。')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/bulk_add_herbs.html', form=form)

@admin.route('/admin/bulk_add_diseases', methods=['GET', 'POST'])
@login_required
def bulk_add_diseases():
    if not current_user.is_admin:
        flash('您没有权限访问此页面。')
        return redirect(url_for('main.index'))
    form = BulkAddDiseaseForm()
    if form.validate_on_submit():
        diseases = form.diseases.data.split('\n')
        added_count = 0
        skipped_count = 0
        for disease_name in diseases:
            disease_name = disease_name.strip()
            if disease_name:
                existing_disease = Disease.query.filter_by(name=disease_name).first()
                if existing_disease:
                    skipped_count += 1
                else:
                    disease = Disease(name=disease_name)
                    db.session.add(disease)
                    added_count += 1
        db.session.commit()
        flash(f'疾病批量添加完成！成功添加 {added_count} 个，跳过 {skipped_count} 个已存在的疾病。')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/bulk_add_diseases.html', form=form)