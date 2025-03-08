from fastapi import APIRouter
from database import get_database
import base64
import auth

router = APIRouter()

@router.post("/register")
def register(username: str, password: str):
    try:
        conn, cursor = get_database()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, base64.b64encode(password.encode()).decode()))
        conn.commit()
        conn.close()
        return {"success": True, "message": "User registered successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.post("/login")
def login(username: str, password: str):
    try:
        conn, cursor = get_database()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            if user[2] == base64.b64encode(password.encode()).decode():
                return {"success": True, "message": "User logged in successfully", "user_id": user[0], "token": auth.create_token(user[0])}
            else:
                return {"success": False, "message": "Invalid password"}
        else:
            return {"success": False, "message": "User does not exist"}
    except Exception as e:
        return {"success": False, "message": str(e)}

