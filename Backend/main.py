import json
import functions_framework
from google.cloud import firestore

# تهيئة الاتصال بقاعدة بيانات Firestore
db = firestore.Client(database='fire123')

@functions_framework.http
def hello_http(request):
    # معالجة طلبات الـ CORS Preflight (OPTIONS)
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://almorshed.cloud',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # إعداد الـ Headers للرد العادي
    headers = {
        'Access-Control-Allow-Origin': 'https://almorshed.cloud',
        'Content-Type': 'application/json'
    }

    try:
        # الوصول للمستند في الفايرستور
        doc_ref = db.collection('voters').document('status')

        # ضمان زيادة العداد بدقة عبر Transaction
        @firestore.transactional
        def update_in_transaction(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)
            current_count = snapshot.get('count') if snapshot.exists and 'count' in snapshot.to_dict() else 0
            new_count = current_count + 1
            transaction.set(doc_ref, {'count': new_count}, merge=True)
            return new_count

        transaction = db.transaction()
        updated_count = update_in_transaction(transaction, doc_ref)

        # تحويل النتيجة إلى JSON String وإرجاعها
        response_body = json.dumps({"count": updated_count})
        return (response_body, 200, headers)

    except Exception as e:
        error_body = json.dumps({"error": str(e)})
        return (error_body, 500, headers)