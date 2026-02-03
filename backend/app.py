from flask import Flask, request, jsonify
from flask_cors import CORS
from DatabaseWrapper import DatabaseWrapper

app = Flask(__name__)
CORS(app)  # Abilita richieste da qualsiasi origine (frontend)

db = DatabaseWrapper()
db.connect()
db.create_tables()

# GET /deliveries - Restituisce tutte le consegne
@app.route("/deliveries", methods=["GET"])
def get_deliveries():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deliveries")
    deliveries = cursor.fetchall()
    cursor.close()
    return jsonify(deliveries), 200

# POST /deliveries - Aggiunge una nuova consegna
@app.route("/deliveries", methods=["POST"])
def add_delivery():
    data = request.get_json()
    required_fields = ["tracking_code", "recipient_name", "address", "time_slot", "priority"]

    # Validazione base: tutti i campi richiesti
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    conn = db.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO deliveries (tracking_code, recipient_name, address, time_slot, status, priority)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["tracking_code"],
            data["recipient_name"],
            data["address"],
            data["time_slot"],
            "READY",        # stato iniziale
            data["priority"]
        ))
        conn.commit()
        new_id = cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

    return jsonify({"message": "Delivery added", "id": new_id}), 201

# Avvio server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
