import json
import functions_framework
from google.cloud import firestore
from flask import jsonify

# الاتصال بقاعدة البيانات المحددة عندك fire123
db = firestore.Client(database='fire123')

@functions_framework.http
def hello_http(request):
    # معالجة الـ CORS بشكل كامل لجميع الطلبات وطلبات OPTIONS تلقائياً
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    try:
        doc_ref = db.collection('voters').document('status')

        @firestore.transactional
        def update_in_transaction(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)
            current_count = 0
            if snapshot.exists:
                data = snapshot.to_dict()
                if data and 'count' in data:
                    current_count = data['count']
            
            new_count = current_count + 1
            transaction.set(doc_ref, {'count': new_count}, merge=True)
            return new_count

        transaction = db.transaction()
        updated_count = update_in_transaction(transaction, doc_ref)

        return (jsonify({"count": updated_count}), 200, headers)

    except Exception as e:
        # إرجاع تفاصيل الخطأ بصيغة JSON بدلاً من انهيار الخادم
        return (jsonify({"error": str(e)}), 200, headers)