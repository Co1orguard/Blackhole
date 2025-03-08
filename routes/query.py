from fastapi import APIRouter, Header
from database import get_database
import auth

router = APIRouter()

@router.get("/search")
async def search(q: str, token: str = Header(...)):
    if not auth.verify_token(token):
        return {"success": False, "message": "Invalid token"}
    try:
        conn, cursor = get_database()
        uid = auth.get_id(token)
        query = f"SELECT * FROM files WHERE filename LIKE '%{q}%' AND user_id = {uid}"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        return {"success": False, "message": str(e)}
