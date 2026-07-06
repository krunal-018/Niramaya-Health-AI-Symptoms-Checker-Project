from flask import Blueprint, request, jsonify
from flask_cors import CORS
import psycopg2
import bcrypt

# Create a Blueprint for user login routes
login_bp = Blueprint('login', __name__)
CORS(login_bp)

db_config = {
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**db_config)

@login_bp.route('/userlogin', methods=['POST'])
def user_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        
        # First, get account details
        cursor.execute("""
            SELECT account_id, password_hash, family_name 
            FROM account_tbl 
            WHERE email = %s
        """, (email,))
        account_row = cursor.fetchone()
        
        if not account_row:
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": "User not found"}), 400

        account_id, stored_password, familyname = account_row
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": "Incorrect password"}), 400

        # Fetch members associated with this account
        cursor.execute("""
            SELECT member_id, name 
            FROM member_tbl 
            WHERE account_id = %s
        """, (account_id,))
        members = cursor.fetchall()
        
        cursor.close()
        conn.close()

        # Prepare member data for response
        members_list = [
            {"member_id": str(member[0]), "name": member[1], "account_id": str(account_id)}
            for member in members
        ]

        # Return success response with member information
        return jsonify({
            "success": True,
            "message": "Login successful",
            "email": email,
            "familyname": familyname,
            "members": members_list
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500