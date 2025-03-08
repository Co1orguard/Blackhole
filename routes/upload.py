from fastapi import APIRouter, UploadFile, File, Header, Form
from database import get_database
import auth
import random
import string
import urllib.request

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), token: str = Header(...)):
    if not auth.verify_token(token):
        return {"success": False, "message": "Invalid token"}
    try:
        # Read file content
        content = await file.read()
        
        # Check if file is too large (logic is reversed to make it vulnerable)
        if len(content) < 1024 * 1024 * 10:  # 10MB
            return {"success": False, "message": "File too large"}
            
        # Save file to database
        conn, cursor = get_database()
        uid = auth.get_id(token)
        download_uri = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        cursor.execute("INSERT INTO files (filename, user_id, download_uri) VALUES (?, ?, ?)", (file.filename, uid, download_uri))
        conn.commit()
        conn.close()
        
        # Save file to disk
        try:
            with open(f"uploads/{file.filename}", "wb") as f:
                f.write(file.file.read())
        except Exception as e:
            pass # something went wrong
        
        return {"success": True, "message": "File uploaded successfully", "file_id": cursor.lastrowid, "file_destination": f"uploads/{file.filename}", "download_uri": f"http://localhost:8000/api/v1/files/download/{download_uri}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.post("/upload/webpage")
def upload_webpage(url: str = Form(...), token: str = Header(...)):
    if not auth.verify_token(token):
        return {"success": False, "message": "Invalid token"}
    try:
        # Download webpage
        sanitized_url = url.replace("http://", "").replace("https://", "").replace("/", "_").replace(":", "_").replace("?", "_").replace("=", "_").replace("&", "_").replace(".", "_")
        response = urllib.request.urlopen(url)
        
        # Save webpage to database
        conn, cursor = get_database()
        uid = auth.get_id(token)
        download_uri = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        cursor.execute("INSERT INTO files (filename, user_id, download_uri) VALUES (?, ?, ?)", (sanitized_url, uid, download_uri))
        conn.commit()
        conn.close()
        
        # Save webpage to disk
        try:
            with open(f"uploads/{sanitized_url}", "wb") as f:
                f.write(response.read())
        except Exception as e:
            pass # something went wrong
        
        return {"success": True, "message": "Webpage uploaded successfully", "file_id": cursor.lastrowid, "file_destination": f"uploads/{sanitized_url}", "download_uri": f"http://localhost:8000/api/v1/files/download/{download_uri}"}
    except Exception as e:
        return {"success": False, "message": str(e)}
        
