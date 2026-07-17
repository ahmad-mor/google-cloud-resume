import functions_framework
from google.cloud import firestore

# تهيئة الاتصال بقاعدة بيانات Firestore
db = firestore.Client()

@functions_framework.http
def hello_http(request):
    # معالجة طلبات الـ CORS (مهمة جداً عشان المتصفح ما يحجب الاتصال)
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://almorshed.cloud',
            'Access-Control-Allow-Methods': 'GET',
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
        # الوصول للمستند اللي أنشأناه في الفايرستور
        doc_ref = db.collection('voters').document('status')
        
        # استخدام الـ Transaction لضمان زيادة العداد بدقة حتى لو دخل كذا شخص بنفس اللحظة
        @firestore.transactional
        def update_in_transaction(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)
            current_count = snapshot.get('count')
            new_count = current_count + 1
            transaction.update(doc_ref, {'count': new_count})
            return new_count

        transaction = db.transaction()
        updated_count = update_in_transaction(transaction, doc_ref)

        # إرسال الرقم الجديد للموقع بصيغة JSON
        return ({"count": updated_count}, 200, headers)

    except Exception as e:
        return ({"error": str(e)}, 500, headers)