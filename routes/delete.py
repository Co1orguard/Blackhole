from fastapi import APIRouter, Header
from database import get_database
import base64
import auth

router = APIRouter()

@router.post("/delete")
def delete(file_id: int):
    try:
        conn, cursor = get_database()
        cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "File deleted successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}
