from flask import Blueprint, request, jsonify
from flask_cors import CORS
import psycopg2

# Create a Blueprint for add member routes
member_bp = Blueprint('member', __name__)
CORS(member_bp)

db_config = {
    "dbname": "projectH",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def connect_db():
    return psycopg2.connect(**db_config)

@member_bp.route('/addmember', methods=['POST'])
def add_member():
    try:
        data = request.json
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        account_id = data.get('accid')

        if not all([name, gender, age, height, weight, account_id]):
            return jsonify({"success": False, "message": "All fields are required"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO member_tbl (account_id, name, gender, age, height, weight) VALUES (%s, %s, %s, %s, %s, %s) RETURNING member_id",
            (account_id, name, gender, age, height, weight)
        )
        new_member_id = cursor.fetchone()[0]
        conn.commit()

        return jsonify({
            "success": True,
            "member_id": new_member_id,
            "message": "Member added successfully"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@member_bp.route('/getuser', methods=['POST'])
def get_user():
    try:
        data = request.json
        member_id = data.get('member_id')
        account_id = data.get('account_id')
        if not member_id or not account_id:
            return jsonify({"success": False, "message": "Email and name are required"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("select * from member_tbl where member_id=%s and account_id=%s", (member_id, account_id))
        row = cursor.fetchone()

        if row:
            name = row[2]
            gender = row[3]
            age = row[4]
            height = row[5]
            weight = row[6]
            return jsonify({"success": True, "message": "Profile fetched successfully", "name": str(name), "gender": str(gender), "age": str(age), "height": str(height), "weight": str(weight)}), 200
        else:
            return jsonify({"success": False, "message": "User does not exist"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

@member_bp.route('/updatemember', methods=['POST'])
def update_member():
    try:
        data = request.json
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        account_id = data.get('account_id')
        member_id = data.get('member_id')

        if not all([name, gender, age, height, weight, account_id, member_id]):
            return jsonify({"success": False, "message": "All fields are required"}), 400

        account_id = int(account_id)
        member_id = int(member_id)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("update member_tbl set name=%s,gender=%s,age=%s,height=%s,weight=%s where member_id=%s and account_id=%s",(name,gender,age,height,weight,member_id,account_id))
        conn.commit()

        return jsonify({
            "success": True,
            "member_id": member_id,
            "message": "Member added successfully"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@member_bp.route('/removeuser', methods=['POST'])
def remove_user():
    try:
        data = request.json
        account_id = data.get('account_id')
        member_id = data.get('member_id')
        if not account_id or not member_id:
            return jsonify({"success": False, "message": "Email and name are required"}), 400

        account_id = int(account_id)
        member_id = int(member_id)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("delete from member_tbl where member_id=%s and account_id=%s", (member_id, account_id))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"success": True, "message": "Member deleted successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Member not found"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

@member_bp.route('/getmembers', methods=['POST'])
def get_members():
    conn = None
    cursor = None
    try:
        # Get account_id from the request body
        data = request.json
        account_id = data.get('account_id')

        if not account_id:
            return jsonify({"success": False, "message": "Account ID is required"}), 400

        # Convert account_id to integer if it's a string (e.g., from JSON)
        account_id = int(account_id)

        # Establish database connection
        conn = connect_db()
        cursor = conn.cursor()

        # Query to fetch all members for the given account_id
        cursor.execute("""
            SELECT member_id, name 
            FROM member_tbl 
            WHERE account_id = %s
        """, (account_id,))
        members = cursor.fetchall()

        # Close cursor and connection
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
            "message": "Members retrieved successfully",
            "members": members_list
        }), 200

    except psycopg2.Error as e:
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"success": False, "message": "Invalid account ID format"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()