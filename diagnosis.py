import plotly.graph_objs as go
import plotly.utils
import json
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Herb, Disease, HerbDiseaseAssociation, DiagnosisLog
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import jieba

diagnosis = Blueprint('diagnosis', __name__)

@diagnosis.route('/diagnose', methods=['POST'])
@login_required
def diagnose():
    prescription = request.form['prescription']
    
    # 使用jieba进行分词
    words = jieba.cut(prescription)
    herbs = [word for word in words if Herb.query.filter_by(name=word).first()]
    
    # 获取所有中药和疾病
    all_herbs = Herb.query.all()
    diseases = Disease.query.all()
    
    # 创建特征矩阵
    herb_encoder = LabelEncoder()
    herb_encoder.fit([herb.name for herb in all_herbs])
    
    disease_encoder = LabelEncoder()
    disease_encoder.fit([disease.name for disease in diseases])
    
    # 准备训练数据
    X = []
    y = []
    for herb in all_herbs:
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
    prescription_encoded = herb_encoder.transform(herbs)
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
                       prescription=prescription,
                       diagnosis_result=str(result))
    db.session.add(log)
    db.session.commit()
    
    return jsonify(result)

@diagnosis.route('/statistics')
@login_required
def statistics():
    # 获取用户的诊断历史
    logs = DiagnosisLog.query.filter_by(user_id=current_user.id).all()
    
    # 统计每种疾病的诊断次数
    disease_count = {}
    for log in logs:
        results = eval(log.diagnosis_result)
        for result in results:
            disease = result['name']
            if disease in disease_count:
                disease_count[disease] += 1
            else:
                disease_count[disease] = 1
    
    # 创建饼图
    labels = list(disease_count.keys())
    values = list(disease_count.values())
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text="疾病诊断统计")
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('statistics.html', graphJSON=graphJSON)

@diagnosis.route('/history')
@login_required
def diagnosis_history():
    logs = DiagnosisLog.query.filter_by(user_id=current_user.id).order_by(DiagnosisLog.timestamp.desc()).all()
    return render_template('diagnosis_history.html', logs=logs)