# S-LIBRARY # แอปฯ ยืม-คืนหนังสือ: สแกน ISBN, แจ้งเตือนหนังสือเกินกำหนดส่ง, ค้นหาตำแหน่งชั้นวาง
# https://drive.google.com/file/d/19BYxIbxTqkkoW1U1oG_aXxFH_9xggsJZ/view?usp=sharing
# [วิดีโอนำเสนอการใช้งาน คลิก!!!](https://drive.google.com/file/d/19BYxIbxTqkkoW1U1oG_aXxFH_9xggsJZ/view?usp=sharing)
# 661310252 นายกิตติ จิวะเกียรติ
# 661310356 นายพรชัย กองเพชร

---

# สภาพแวดล้อมที่รองรับ (Prerequisites)
ก่อนทำการรันโปรเจกต์ กรุณาตรวจสอบให้แน่ใจว่าเครื่องคอมพิวเตอร์ของท่านมีโปรแกรมดังต่อไปนี้:
* **Python 3.8** ขึ้นไป
* **MariaDB** หรือ **MySQL** (สามารถใช้ผ่าน XAMPP, DBeaver หรืออื่นๆ ได้)

---

# วิธีการติดตั้งและรันโปรเจกต์ (Step-by-Step)

# Step 1: ติดตั้งฐานข้อมูล (Database Setup)
1. เปิดโปรแกรมจัดการฐานข้อมูลที่ท่านใช้งาน
2. ทำการสร้าง Database ใหม่ (โปรดตั้งชื่อให้ตรงกับที่ระบุในไฟล์ `backend/main.py` ของโปรเจกต์)
3. ทำการ **Import** ไฟล์ `database_book_setup.sql` (ที่อยู่ในโฟลเดอร์หลัก) เข้าไปใน Database เพื่อสร้างตารางและข้อมูลตั้งต้น

## Step 2: ตั้งค่าการเชื่อมต่อ (Configuration) ⚠️ สำคัญมาก
เพื่อให้แอปพลิเคชันทำงานบนเครื่องของท่านได้อย่างสมบูรณ์ รบกวนปรับแก้ค่าคอนฟิก 2 จุด ดังนี้ครับ:

**1. รหัสผ่าน Database (สำหรับ Backend)**
* เปิดไฟล์ `backend/main.py`
* ค้นหาบรรทัดที่มีการเชื่อมต่อ Database (เช่น `pymysql.connect(...)`)
* แก้ไขตัวแปร `user` และ `password` ให้ตรงกับ Database ในเครื่องของท่าน (เช่น เปลี่ยนเป็น `user='root'`, `password=''`)

**2. ตั้งค่า API URL (สำหรับ Frontend)**
* เปิดไฟล์ `frontend/app.py`
* ค้นหาตัวแปร `API_URL`
* หากท่านรันโปรเจกต์บนเครื่องคอมพิวเตอร์เดียวกัน ให้แก้ไขกลับเป็น Localhost ดังนี้:
  `API_URL = "http://localhost:8000"`

### Step 3: ติดตั้ง Library ที่จำเป็น
เปิด Terminal ขึ้นมา ชี้ตำแหน่งไปที่โฟลเดอร์หลักของโปรเจกต์ แล้วรันคำสั่ง:
```bash
pip install -r requirements.txt
