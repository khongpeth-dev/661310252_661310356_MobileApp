from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import pymysql
import datetime

app = FastAPI(title="S-LIBRARY API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

def get_db():
    return pymysql.connect(host='localhost', user='admin', password='1234', database='library_final_project', cursorclass=pymysql.cursors.DictCursor)

class LoginReq(BaseModel):
    username: str = Field(..., min_length=4)
    password: str = Field(..., min_length=4)

class RegisterReq(BaseModel):
    username: str = Field(..., min_length=4)
    password: str = Field(..., min_length=4)
    full_name: str = Field(..., min_length=2)
    phone: str = Field(..., pattern=r"^0[0-9]{8,9}$")

class BorrowReq(BaseModel):
    user_id: int
    book_id: int
    days: int = Field(..., ge=1, le=14)
    condition: str

class ReturnReq(BaseModel):
    condition_after: str
    fine_amount: float = Field(..., ge=0)

class CategoryReq(BaseModel):
    name: str = Field(..., min_length=1)

class BookReq(BaseModel):
    isbn: str = Field(..., pattern=r"^[0-9-]{10,17}$")
    title: str = Field(..., min_length=1)
    shelf_location: str
    image_name: str
    category: str
    synopsis: str

class UserUpdateReq(BaseModel):
    full_name: str = Field(..., min_length=2)
    phone: str = Field(..., pattern=r"^0[0-9]{8,9}$")
    role: str

class BookUpdateReq(BaseModel):
    title: str = Field(..., min_length=1)
    image_name: str
    shelf_location: str
    category: str
    synopsis: str

# --- AUTH ---
@app.post("/login")
def login(req: LoginReq):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (req.username, req.password))
        user = cur.fetchone()
        if not user: raise HTTPException(status_code=401)
        return user

@app.post("/register")
def register(req: RegisterReq):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO users (username, password, full_name, phone) VALUES (%s, %s, %s, %s)", (req.username, req.password, req.full_name, req.phone))
            db.commit()
            return {"status": "success"}
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            raise HTTPException(status_code=400, detail="ชื่อผู้ใช้งานนี้มีผู้ใช้แล้ว")
        raise HTTPException(status_code=400, detail="ข้อมูลไม่ถูกต้อง (Integrity Error)")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"เกิดข้อผิดพลาด: {str(e)}")

# --- BOOKS & CATS ---
@app.get("/categories")
def get_categories():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT name FROM categories ORDER BY id")
        return [row['name'] for row in cur.fetchall()]

@app.post("/categories")
def add_category(req: CategoryReq):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO categories (name) VALUES (%s)", (req.name,))
            db.commit()
            return {"status": "success"}
    except Exception:
        pass

@app.get("/books")
def get_books():
    db = get_db()
    with db.cursor() as cur:
        # แก้ SQL ตรงนี้: เพิ่มเงื่อนไข WHERE is_available = 1
        cur.execute("SELECT * FROM books WHERE is_available = 1 ORDER BY id DESC")
        return cur.fetchall()

# --- USER TRANSACTIONS ---
@app.post("/borrow")
def borrow_book(req: BorrowReq):
    db = get_db()
    # แปลงวันที่เป็น String (YYYY-MM-DD) ป้องกัน Database Error
    due_date = (datetime.date.today() + datetime.timedelta(days=req.days)).strftime('%Y-%m-%d')
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO transactions (user_id, book_id, borrow_date, due_date, condition_before, status, is_notified_borrow) VALUES (%s, %s, CURDATE(), %s, %s, 'pending_borrow', 0)", 
                        (req.user_id, req.book_id, due_date, req.condition))
            cur.execute("UPDATE books SET is_available=0 WHERE id=%s", (req.book_id,))
            db.commit()
            return {"status": "success"}
    except Exception as e:
        db.rollback()
        print("❌ DATABASE ERROR:", str(e)) # ปริ้นท์บอกใน Terminal ให้รู้ชัดๆ
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}/borrows")
def get_user_active_borrows(user_id: int):
    # ดึงรายการที่ กำลังรออนุมัติ, ยืมอยู่, หรือกำลังรอตรวจคืน
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT t.*, b.title, b.image_name, b.isbn FROM transactions t JOIN books b ON t.book_id = b.id WHERE t.user_id = %s AND t.status IN ('pending_borrow', 'borrowed', 'pending_return') ORDER BY t.id DESC", (user_id,))
        return cur.fetchall()

@app.get("/user/{user_id}/history")
def get_user_history(user_id: int):
    # ประวัติโชว์เฉพาะที่ คืนเสร็จสิ้นแล้ว
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT t.*, b.title, b.image_name, b.isbn FROM transactions t JOIN books b ON t.book_id = b.id WHERE t.user_id = %s AND t.status = 'returned' ORDER BY t.return_date DESC", (user_id,))
        return cur.fetchall()

@app.put("/user/request_return/{tx_id}")
def request_return(tx_id: int):
    # User กดขอคืนหนังสือ
    db = get_db()
    with db.cursor() as cur:
        cur.execute("UPDATE transactions SET status = 'pending_return' WHERE id = %s", (tx_id,))
        db.commit()
        return {"status": "success"}

@app.get("/notifs/{user_id}")
def check_notifications(user_id: int):
    # ตรวจสอบ Pop-up แจ้งเตือน 2 กรณี: เจ้าหน้าที่อนุมัติยืม หรือ อนุมัติคืน
    db = get_db()
    notifs = []
    with db.cursor() as cur:
        # 1. แจ้งเตือนอนุมัติยืม
        cur.execute("SELECT t.id, b.title, 'borrow_approved' as type FROM transactions t JOIN books b ON t.book_id = b.id WHERE t.user_id = %s AND t.is_notified_borrow = 0 AND t.status = 'borrowed'", (user_id,))
        for row in cur.fetchall():
            notifs.append(f"✅ อนุมัติการยืม: {row['title']}")
            cur.execute("UPDATE transactions SET is_notified_borrow = 1 WHERE id = %s", (row['id'],))
        
        # 2. แจ้งเตือนตรวจรับคืน
        cur.execute("SELECT t.id, b.title, t.fine_amount, 'return_approved' as type FROM transactions t JOIN books b ON t.book_id = b.id WHERE t.user_id = %s AND t.is_notified = 0 AND t.status = 'returned'", (user_id,))
        for row in cur.fetchall():
            fine_text = f" (ค่าปรับ: {row['fine_amount']}฿)" if row['fine_amount'] > 0 else " (ไม่มีค่าปรับ)"
            notifs.append(f"📦 ตรวจรับคืนแล้ว: {row['title']}{fine_text}")
            cur.execute("UPDATE transactions SET is_notified = 1 WHERE id = %s", (row['id'],))
        db.commit()
    return notifs

# --- OFFICER MANAGEMENT ---
@app.get("/officer/pending_borrows")
def get_pending_borrows():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT t.id, b.title, u.full_name, t.borrow_date FROM transactions t JOIN books b ON t.book_id = b.id JOIN users u ON t.user_id = u.id WHERE t.status = 'pending_borrow'")
        return cur.fetchall()

@app.put("/officer/approve_borrow/{tx_id}")
def approve_borrow(tx_id: int):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("UPDATE transactions SET status = 'borrowed' WHERE id = %s", (tx_id,))
        # Safety: Ensure book is marked unavailable (it should be, but just in case)
        cur.execute("UPDATE books SET is_available = 0 WHERE id = (SELECT book_id FROM transactions WHERE id = %s)", (tx_id,))
        db.commit()
        return {"status": "success"}

@app.get("/officer/pending_returns")
def get_pending_returns():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT t.id, b.title, u.full_name, t.condition_before FROM transactions t JOIN books b ON t.book_id = b.id JOIN users u ON t.user_id = u.id WHERE t.status = 'pending_return'")
        return cur.fetchall()

@app.put("/officer/approve_return/{tx_id}")
def process_return(tx_id: int, req: ReturnReq):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE transactions SET status = 'returned', return_date = CURDATE(), condition_after = %s, fine_amount = %s, is_notified = 0 WHERE id = %s", (req.condition_after, req.fine_amount, tx_id))
            cur.execute("UPDATE books SET is_available = 1 WHERE id = (SELECT book_id FROM transactions WHERE id = %s)", (tx_id,))
            db.commit()
            return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- ADMIN MANAGEMENT ---
@app.get("/admin/books")
def get_all_books_admin():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM books ORDER BY id DESC")
        return cur.fetchall()

@app.delete("/admin/books/{book_id}")
def delete_book(book_id: int):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
            db.commit()
            return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Cannot delete book, it might be in use.")

@app.put("/admin/books/{book_id}")
def update_book(book_id: int, req: BookUpdateReq):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE books SET title=%s, image_name=%s, shelf_location=%s, category=%s, synopsis=%s WHERE id=%s", (req.title, req.image_name, req.shelf_location, req.category, req.synopsis, book_id))
            db.commit(); return {"status": "success"}
    except Exception as e: db.rollback(); raise HTTPException(status_code=400, detail=str(e))

@app.get("/admin/users")
def get_all_users():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()

@app.put("/admin/users/{user_id}")
def update_user(user_id: int, req: UserUpdateReq):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            target = cur.fetchone()
            if target and target['role'] == 'admin': raise HTTPException(status_code=403, detail="Cannot modify admin")
            cur.execute("UPDATE users SET full_name=%s, phone=%s, role=%s WHERE id=%s", (req.full_name, req.phone, req.role, user_id))
            db.commit(); return {"status": "success"}
    except Exception as e: db.rollback(); raise HTTPException(status_code=400, detail=str(e))

@app.delete("/admin/users/{user_id}")
def delete_user(user_id: int):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            target = cur.fetchone()
            if target and target['role'] == 'admin': raise HTTPException(status_code=403, detail="Cannot delete admin")
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            db.commit()
            return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Cannot delete user")

@app.post("/admin/books")
def add_new_book(req: BookReq):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO books (isbn, title, shelf_location, image_name, category, synopsis) VALUES (%s, %s, %s, %s, %s, %s)", (req.isbn, req.title, req.shelf_location, req.image_name, req.category, req.synopsis))
            db.commit(); return {"status": "success"}
    except: pass