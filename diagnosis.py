from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Herb, Disease, HerbDiseaseAssociation, DiagnosisLog
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

diagnosis = Blueprint('diagnosis', __name__)

@diagnosis.route('/diagnose', methods=['POST'])
@login_required
def diagnose():
    prescription = request.form['prescription'].split(',')
    
    # 获取所有中药和疾病
    herbs = Herb.query.all()
    diseases = Disease.query.all()
    
    # 创建特征矩阵
    herb_encoder = LabelEncoder()
    herb_encoder.fit([herb.name for herb in herbs])
    
    disease_encoder = LabelEncoder()
    disease_encoder.fit([disease.name for disease in diseases])
    
    # 准备训练数据
    X = []
    y = []
    for herb in herbs:
        associations = HerbDiseaseAssociation.query.filter_by(herb_id=herb.id).all()
        for association in associations:
            disease = Disease.query.get(association.disease_id)
            X.append(herb_encoder.transform([herb.name])[0])
            y.append(disease_encoder.transform([disease.name])[0])
    
    X = np.array(X).reshape(-1, 1)
    y = np.array(y)
    
    # 训练决策树模型
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    
    # 预测
    prescription_encoded = herb_encoder.transform([herb.strip() for herb in prescription])
    prescription_encoded = prescription_encoded.reshape(-1, 1)
    predictions = clf.predict_proba(prescription_encoded)
    
    # 获取结果
    result = []
    for i, prob in enumerate(predictions.mean(axis=0)):
        if prob > 0:
            disease_name = disease_encoder.inverse_transform([i])[0]
            result.append({'name': disease_name, 'probability': float(prob)})
    
    result.sort(key=lambda x: x['probability'], reverse=True)
    
    # 记录诊断日志
    log = DiagnosisLog(user_id=current_user.id,
                       prescription=','.join(prescription),
                       diagnosis_result=str(result))
    db.session.add(log)
    db.session.commit()
    
    return jsonify(result)

@diagnosis.route('/history')
@login_required
def diagnosis_history():
    logs = DiagnosisLog.query.filter_by(user_id=current_user.id).order_by(DiagnosisLog.timestamp.desc()).all()
    return render_template('diagnosis_history.html', logs=logs)