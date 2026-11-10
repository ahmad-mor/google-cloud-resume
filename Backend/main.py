import logging
import functions_framework
from google.cloud import firestore
from flask import jsonify

db = firestore.Client(database='fire123')
doc_ref = db.collection('voters').document('status')

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '3600',
}

def read_count(snapshot):
    if not snapshot.exists:
        return 0
    return (snapshot.to_dict() or {}).get('count', 0)


def next_count(current):
    return current + 1


@firestore.transactional
def increment(transaction, ref):
       snapshot = ref.get(transaction=transaction)
    new_count = next_count(read_count(snapshot))
    transaction.set(ref, {'count': new_count}, merge=True)
    return new_count


@functions_framework.http
def hello_http(request):
    if request.method == 'OPTIONS':
        return ('', 204, CORS_HEADERS)

    headers = {'Access-Control-Allow-Origin': '*'}

    try:
        # GET: قراءة العدد الحالي فقط بدون زيادة
                if request.method == 'GET':
            count = read_count(doc_ref.get())
            return (jsonify({"count": count}), 200, headers)

        # POST: زيادة العداد
        if request.method == 'POST':
            new_count = increment(db.transaction(), doc_ref)
            return (jsonify({"count": new_count}), 200, headers)

        return (jsonify({"error": "Method not allowed"}), 405, headers)

    except Exception:
        logging.exception("Counter update failed")
        return (jsonify({"error": "Internal server error"}), 500, headers)