from fastapi import APIRouter, Header
from database import get_database
import auth
from fastapi.responses import FileResponse
router = APIRouter()

@router.get("/files")
def get_files(token: str = Header(...)):
    try:
        conn, cursor = get_database()
        uid = auth.get_id(token)
        cursor.execute("SELECT * FROM files WHERE user_id = ?", (uid,))
        files = cursor.fetchall()
        return files
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.get("/files/{file_id}")
def get_file(file_id: int, token: str = Header(...)):
    try:
        conn, cursor = get_database()
        uid = auth.get_id(token)
        cursor.execute("SELECT id, filename, download_uri FROM files WHERE id = ? AND user_id = ?", (file_id, uid))
        file = cursor.fetchone()
        if file:
            return {"success": True, "file_id": file[0], "file_destination": f"uploads/{file[1]}", "download_uri": f"http://localhost:8000/api/v1/files/download/{file[2]}"}
        else:
            return {"success": False, "message": "File not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.get("/files/download/{download_uri}")
def download_file(download_uri: str, token: str = Header(...)):
    if not auth.verify_token(token):
        return {"success": False, "message": "Invalid token"}
    try:
        conn, cursor = get_database()
        uid = auth.get_id(token)
        cursor.execute("SELECT id, filename FROM files WHERE download_uri = ?", (download_uri,))
        file = cursor.fetchone()
        if file:
            cursor.execute("INSERT INTO downloads (file_id, user_id) VALUES (?, ?)", (file[0], uid))
            conn.commit()
            return FileResponse(f"uploads/{file[1]}", media_type="application/octet-stream", filename=file[1])
        else:
            return {"success": False, "message": "File not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}
