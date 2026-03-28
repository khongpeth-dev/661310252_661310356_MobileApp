import flet as ft
import requests
import datetime
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# --- CONFIG ---
# โปรดเปลี่ยน IP นี้ตาม IP ของเครื่อง Mac คุณ (ตรวจสอบด้วย ipconfig getifaddr en0)
# เพื่อให้มือถือในวง Wi-Fi เดียวกันสามารถเชื่อมต่อได้
SERVER_IP = "172.20.10.4"
API_URL = f"http://{SERVER_IP}:8000"

C_BG = "#F4F6F8"        # สีพื้นหลังของแอป (เทาอ่อน)
C_CARD = "#FFFFFF"      # สีพื้นหลังของการ์ดและคอนเทนเนอร์ (ขาว)
C_PRIMARY = "#05DF72"   # สีหลักของแอป เช่น ปุ่ม, ไอคอนสำคัญ (เขียว)
C_PRIMARY_LIGHT = "#EDF5FF" # สีรองแบบอ่อน สำหรับส่วนเน้นหรือพื้นหลังปุ่มแบบใส
C_SECONDARY = "#161616" # สีรอง เช่น แถบเมนู NavBar ด้านบน (ดำ/เทาเข้ม)
C_TEXT_MAIN = "#121619" # สีข้อความหลัก
C_TEXT_SUB = "#525252"  # สีข้อความรอง หรือคำอธิบายเพิ่มเติม
C_SUCCESS = "#24A148"   # สีสำหรับสถานะ 'พร้อมยืม' หรือ 'สำเร็จ' (เขียว)
C_DANGER = "#DA1E28"    # สีสำหรับสถานะ 'ถูกยืมแล้ว' หรือ 'ผิดพลาด' (แดง)
C_WARN  = "#F1C21B"     # สีแจ้งเตือนคำเตือน (เหลือง)

def shadow_sm(): return ft.BoxShadow(blur_radius=8, color="#0D000000", offset=ft.Offset(0, 2))
def shadow_md(): return ft.BoxShadow(blur_radius=16, color="#1A000000", offset=ft.Offset(0, 8))

def btn_hover(e):
    e.control.scale = 1.03 if e.data == "true" else 1.0
    if hasattr(e.control, "elevation") and e.control.elevation is not None:
        if e.control.elevation > 0: e.control.elevation = 6 if e.data == "true" else 2
    e.control.update()

def PrimaryButton(text, on_click, icon=None, width=None, bgcolor=C_PRIMARY, expand=False):
    return ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(icon, size=18) if icon else ft.Container(),
            ft.Text(text, weight="bold", size=14)
        ], alignment="center", tight=True),
        on_click=on_click,
        width=width,
        expand=expand,
        color="white",
        bgcolor=bgcolor,
        elevation=2,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(15, 25, 15, 25),
            overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        ),
        animate_scale=ft.Animation(200, "easeOut"),
        on_hover=btn_hover
    )

def SecondaryButton(text, on_click, icon=None, color=C_PRIMARY, width=None):
    return ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(icon, size=18) if icon else ft.Container(),
            ft.Text(text, weight="bold", size=14)
        ], alignment="center", tight=True),
        on_click=on_click,
        width=width,
        style=ft.ButtonStyle(
            color=color,
            side=ft.BorderSide(1.5, color),
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(15, 25, 15, 25),
            overlay_color=ft.Colors.with_opacity(0.05, color),
        ),
        animate_scale=ft.Animation(200, "easeOut"),
        on_hover=btn_hover
    )

def DangerButton(text, on_click, icon=None):
    return PrimaryButton(text, on_click, icon=icon, width=None, bgcolor=C_DANGER)

def TextButton(text, on_click, color=C_PRIMARY, icon=None):
    return ft.TextButton(
        content=ft.Text(text, weight="bold", color=color), icon=icon, icon_color=color, on_click=on_click,
        style=ft.ButtonStyle(
            padding=ft.Padding(12, 8, 12, 8),
            overlay_color=ft.Colors.with_opacity(0.05, color)
        ),
        animate_scale=ft.Animation(150, "easeOut"), on_hover=btn_hover
    )

def IconButton(icon, on_click, color=C_TEXT_SUB):
    b = ft.IconButton(icon=icon, icon_color=color, on_click=on_click, tooltip="Hover for action")
    return b

def CardContainer(content, padding=20):
    c = ft.Container(
        content=content, bgcolor=C_CARD, padding=padding, border_radius=12,
        shadow=shadow_sm(), animate_scale=ft.Animation(300, "easeOut"),
        scale=1.0, animate=ft.Animation(300, "easeOut"),
    )
    def on_cd_hover(e):
        c.scale = 1.015 if e.data == "true" else 1.0
        c.shadow = shadow_md() if e.data == "true" else shadow_sm()
        c.update()
    c.on_hover = on_cd_hover
    return c

def main(page: ft.Page):
    page.title = "S-LIBRARY"
    page.horizontal_alignment = "stretch"
    page.scroll = None # ปิดเลื่อนที่ระดับ Page เพื่อให้ Background อยู่นิ่ง
    page.padding = 0
    page.bgcolor = C_BG
    page.theme_mode = ft.ThemeMode.LIGHT
    print("DEBUG: App Main Started")
    page.user_data = None

    def show_toast(msg, is_error=True):
        try:
            # ใช้ SnackBar แบบปลอดภัยที่สุดสำหรับทุกเวอร์ชัน
            sb = ft.SnackBar(
                content=ft.Text(msg, color="white", weight="bold"),
                bgcolor=C_DANGER if is_error else C_SUCCESS,
                behavior=ft.SnackBarBehavior.FLOATING
            )
            page.overlay.append(sb)
            sb.open = True
            page.update()
        except:
            # ถ้า SnackBar มีปัญหาจริงๆ ให้ใช้ print เป็นทางเลือกสุดท้าย
            print(f"NOTIFICATION: {msg}")


    def handle_api_error(res):
        if res.status_code == 401:
            show_toast("ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง", is_error=True)
        elif res.status_code == 422:
            try:
                raw_json = res.json()
                detail = raw_json.get('detail', [])
                if isinstance(detail, list) and len(detail) > 0:
                    err = detail[0]
                    field = err.get('loc', [])[-1]
                    msg_type = err.get('type', '')
                    
                    field_map = {
                        "username": "ชื่อผู้ใช้งาน", "password": "รหัสผ่าน", 
                        "full_name": "ชื่อ-นามสกุล", "phone": "เบอร์โทรศัพท์",
                        "isbn": "รหัส ISBN", "days": "จำนวนวันที่ยืม",
                        "title": "ชื่อเรื่อง", "fine_amount": "ค่าปรับ"
                    }
                    f_name = field_map.get(field, field)
                    
                    if any(x in msg_type for x in ["too_short", "min_length"]):
                        min_l = err.get('ctx', {}).get('min_length', '4')
                        show_toast(f"กรุณากรอก {f_name} ให้มีความยาวอย่างน้อย {min_l} ตัวอักษร", is_error=True)
                    elif any(x in msg_type for x in ["pattern_mismatch", "regex"]):
                        if field == "phone":
                            show_toast(f"เบอร์โทรศัพท์ต้องเริ่มต้นด้วย 0 และมี 9-10 หลัก (ตัวอย่าง: 0812345678)", is_error=True)
                        elif field == "isbn":
                            show_toast(f"รหัส ISBN ไม่ถูกต้อง (ต้องเป็นตัวเลข 10-17 หลัก และห้ามมีช่องว่าง)", is_error=True)
                        else:
                            show_toast(f"รูปแบบของ {f_name} ไม่ถูกต้อง", is_error=True)
                    elif "missing" in msg_type:
                        show_toast(f"กรุณากรอกข้อมูล {f_name} ให้ครบถ้วน", is_error=True)
                    else:
                        show_toast(f"ข้อมูล {f_name} ไม่ถูกต้อง: {err.get('msg', 'ไม่ทราบสาเหตุ')}", is_error=True)
                    return
            except: pass
            show_toast("กรุณากรอกข้อมูลให้ถูกต้องตามที่ระบบกำหนด", is_error=True)
        elif res.status_code == 400:
            try:
                detail = res.json().get('detail', 'ข้อมูลไม่ถูกต้อง')
                show_toast(str(detail), is_error=True)
            except:
                show_toast("คำขอไม่ถูกต้อง (400)", is_error=True)
        else:
            show_toast(f"เกิดข้อผิดพลาดในการเชื่อมต่อ (Status: {res.status_code})", is_error=True)

    # --- LAYOUT HELPERS (เพื่อป้องกัน Error ในอนาคต) ---
    def PageLayout(content, show_nav=True, stretch=True):
        """ส่งคืนเฉพาะ Content เพื่อประมวลผลต่อ (Simple & Stable)"""
        return content

    def change_view(view_name, data=None):
        page.controls.clear()
        try:
            content = None
            if view_name == "login": content = LoginView()
            elif view_name == "register": content = RegisterView()
            elif view_name == "book_detail": content = BookDetailView(data) 
            elif view_name == "user_borrows": content = UserBorrowsView() 
            elif view_name == "user_history": content = UserHistoryView() 
            elif view_name == "home":
                role = page.user_data.get('role', 'user') if page.user_data else "user"
                if role == "user": 
                    content = UserHomeView()
                    check_notifications()
                elif role == "officer": content = OfficerHomeView()
                elif role == "admin": content = AdminHomeView()
            
            if content:
                # 1. Background (ลายหนังสือกะจายจางๆ)
                bg = ft.Image(
                    src="/bg_library.png",
                    opacity=0.18, # ปรับให้เข้มขึ้นเพื่อให้เห็นชัดตามต้องการ
                    repeat="repeat",
                    expand=True,
                    gapless_playback=True
                )
                
                # 2. Main Layout (NavBar + Content)
                show_nav = view_name not in ["login", "register"]
                main_layout = ft.Column(expand=True, spacing=0)
                
                if show_nav:
                    main_layout.controls.append(AppNavBar())
                
                # พื้นที่เนื้อหาที่เลื่อนได้
                scroll_area = ft.Column(
                    expand=True, scroll="auto", spacing=0,
                    controls=[ft.Container(content=content, padding=ft.Padding(15, 10, 15, 30))]
                )
                main_layout.controls.append(scroll_area)
                
                # เสริมความปลอดภัยด้วยการครอบ Stack
                page.add(ft.Stack([bg, main_layout], expand=True))
        except Exception as e:
            page.add(ft.Text(f"System Error: {str(e)}", color="red"))
        page.update()

    def check_notifications():
        try:
            notifs = requests.get(f"{API_URL}/notifs/{page.user_data['id']}").json()
            if notifs:
                msg = "\n".join(notifs)
                dlg = ft.AlertDialog(
                    title=ft.Row([ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=C_PRIMARY), ft.Text("อัปเดตสถานะ", weight="bold")], spacing=5),
                    content=ft.Text(msg),
                    actions=[PrimaryButton("รับทราบ", lambda _: on_dlg_close(dlg), width=200)],
                    actions_alignment=ft.MainAxisAlignment.CENTER
                )
                def on_dlg_close(d):
                    d.open = False
                    page.update()
                page.overlay.append(dlg)
                dlg.open = True
                page.update()
        except: pass

    def AppNavBar():
        if not page.user_data: return ft.Container()
        role = page.user_data.get('role', 'user')
        uname = page.user_data.get('username', 'User')

        if role == "user":
            actions = [
                TextButton("หน้าหลัก", lambda _: change_view("home"), color="white"),
                ft.Container(width=10),
                ft.PopupMenuButton(
                    content=ft.Row([
                        ft.Container(
                            padding=8, border_radius=30, bgcolor="white",
                            content=ft.Icon(ft.Icons.PERSON, color=C_PRIMARY, size=20)
                        ), 
                        ft.Text(uname, color="white", weight="bold")
                    ], spacing=10),
                    items=[
                        ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.Icons.BOOK, size=16), ft.Text(" รายการยืมของฉัน", weight="bold")]), on_click=lambda _: change_view("user_borrows")),
                        ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.Icons.HISTORY, size=16), ft.Text(" ประวัติการยืม", weight="bold")]), on_click=lambda _: change_view("user_history")),
                        ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.Icons.LOGOUT, size=16), ft.Text(" ออกจากระบบ", weight="bold")]), on_click=lambda _: change_view("login"))
                    ]
                )
            ]
        else:
            role_label = "Administrator" if role == "admin" else "Officer"
            actions = [
                ft.Container(
                    padding=ft.Padding(12, 6, 12, 6), border_radius=20, bgcolor="white20",
                    content=ft.Text(f"{uname} ({role_label})", color="white", weight="bold")
                ),
                ft.Container(width=15),
                ft.IconButton(icon=ft.Icons.LOGOUT, icon_color="white", tooltip="ออกจากระบบ", on_click=lambda _: change_view("login"), bgcolor=C_DANGER, padding=12)
            ]

        # ตรวจสอบว่าควรเว้นพื้นที่ Notch หรือไม่ (เฉพาะ Mobile)
        is_mobile = page.platform in ["android", "ios", ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
        nav_h = 120 if is_mobile else 65
        nav_p = 60 if is_mobile else 0

        return ft.Container(
            bgcolor=C_SECONDARY,
            height=nav_h,
            padding=ft.Padding(15, nav_p, 15, 0),
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.LIBRARY_BOOKS, color="white", size=24), 
                    ft.Text("S-LIBRARY", size=18, weight="black", color="white")
                ], spacing=8),
                ft.Row(actions, alignment="center")
            ], alignment="spaceBetween")
        )

    # ==========================================
    # AUTH VIEWS
    # ==========================================
    def LoginView():
        u_input = ft.TextField(label="ชื่อผู้ใช้งาน", border_radius=8, prefix_icon=ft.Icons.PERSON, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
        p_input = ft.TextField(label="รหัสผ่าน", password=True, can_reveal_password=True, border_radius=8, prefix_icon=ft.Icons.LOCK, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
        def do_login(e):
            try:
                res = requests.post(f"{API_URL}/login", json={"username": u_input.value, "password": p_input.value})
                if res.status_code == 200: 
                    page.user_data = res.json()
                    name = page.user_data.get('full_name', 'User')
                    show_toast(f"ยินดีต้อนรับคุณ {name} เข้าสู่ระบบสำเร็จ!", is_error=False)
                    change_view("home")
                else:
                    handle_api_error(res)
            except:
                show_toast("ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้", is_error=True)

        return PageLayout(
            show_nav=False, stretch=False, # Login ไม่ต้องมี Nav และไม่ต้องยืด (ให้มันอยู่กลาง)
            content=ft.Column([
                ft.Container(height=80), # เพิ่มช่องว่างด้านบนหลบ Notch สำหรับหน้า Login
                ft.Container(
                    width=420,
                    content=CardContainer(
                        padding=40,
                        content=ft.Column([
                            ft.Icon(ft.Icons.LIBRARY_BOOKS, size=60, color=C_PRIMARY),
                            ft.Text("S-LIBRARY", size=28, weight="bold", color=C_SECONDARY),
                            ft.Text("ยินดีต้อนรับเข้าสู่ระบบ", size=14, color=C_TEXT_SUB),
                            ft.Container(height=20),
                            u_input, p_input, ft.Container(height=10),
                            PrimaryButton("เข้าสู่ระบบ", do_login, icon=ft.Icons.LOGIN, width=300),
                            ft.Container(height=10),
                            ft.Row([ft.Text("ยังไม่มีบัญชี?", color=C_TEXT_SUB), TextButton("สมัครสมาชิก", lambda _: change_view("register"))], alignment="center")
                        ], horizontal_alignment="center", tight=True)
                    )
                )
            ], horizontal_alignment="center")
        )

    def RegisterView():
        u = ft.TextField(label="ชื่อผู้ใช้งาน (ขั้นต่ำ 4 ตัวอักษร)", prefix_icon=ft.Icons.PERSON, border_radius=8, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
        p = ft.TextField(label="รหัสผ่าน (ขั้นต่ำ 4 ตัวอักษร)", password=True, prefix_icon=ft.Icons.LOCK, border_radius=8, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
        fn = ft.TextField(label="ชื่อ-นามสกุล", prefix_icon=ft.Icons.BADGE, border_radius=8, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
        ph = ft.TextField(label="เบอร์โทรศัพท์ (9-10 หลัก)", prefix_icon=ft.Icons.PHONE, border_radius=8, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
        
        def do_register(e):
            try:
                res = requests.post(f"{API_URL}/register", json={"username": u.value, "password": p.value, "full_name": fn.value, "phone": ph.value})
                if res.status_code == 200:
                    show_toast("สมัครสมาชิกเรียบร้อยแล้ว! สามารถเข้าสู่ระบบได้ทันที", is_error=False)
                    change_view("login")
                else:
                    handle_api_error(res)
            except:
                show_toast("ขัดข้อง โปรดลองใหม่", is_error=True)

        return PageLayout(
            show_nav=False, stretch=False,
            content=ft.Column([
                ft.Container(height=80), 
                ft.Container(
                    width=450,
                    content=CardContainer(
                        padding=40,
                        content=ft.Column([
                            ft.Text("สร้างบัญชีใหม่", size=24, weight="bold", color=C_SECONDARY),
                            ft.Container(height=10), u, p, fn, ph, ft.Container(height=10),
                            PrimaryButton("ยืนยันการลงทะเบียน", do_register, icon=ft.Icons.PERSON_ADD, width=300),
                            ft.Container(height=10),
                            ft.Row([ft.Text("มีบัญชีแล้วใช่ไหม?", color=C_TEXT_SUB), TextButton("กลับสู่หน้าเข้าสู่ระบบ", lambda _: change_view("login"))], alignment="center")
                        ], horizontal_alignment="center", tight=True)
                    )
                )
            ], horizontal_alignment="center")
        )

    # ==========================================
    # USER VIEWS
    # ==========================================
    def UserHomeView():
        all_books = []
        search_input = ft.TextField(hint_text="ชื่อหนังสือ หรือ ISBN...", prefix_icon=ft.Icons.SEARCH, border_radius=30, bgcolor=C_CARD, expand=True, border_color="transparent", filled=True)
        book_grid_container = ft.Column(spacing=30)

        def create_book_card(b):
            is_avail = b.get('is_available', 0) == 1
            status_color = C_SUCCESS if is_avail else C_DANGER
            status_text = "พร้อมยืม" if is_avail else "ถูกยืมแล้ว"
            return ft.Container(
                width=165, bgcolor=C_CARD, border_radius=12, shadow=shadow_sm(),
                content=ft.Column([
                    ft.Image(src=f"{API_URL}/assets/{b.get('image_name', 'default.png')}", width=165, height=220, fit="cover", border_radius=ft.BorderRadius(12,12,0,0)),
                    ft.Container(
                        padding=12,
                        content=ft.Column([
                            ft.Text(b.get('title', 'ไม่ระบุชื่อ'), weight="bold", size=13, max_lines=2, overflow="ellipsis", color=C_TEXT_MAIN),
                            ft.Text(f"หมวด: {b.get('category','ทั่วไป')}", size=11, color=C_TEXT_SUB, max_lines=1, overflow="ellipsis"),
                            ft.Row([
                                ft.Icon(ft.Icons.CIRCLE, size=8, color=status_color),
                                ft.Text(status_text, size=11, color=status_color, weight="bold")
                            ], spacing=4)
                        ], spacing=2)
                    )
                ], spacing=0),
                on_click=lambda _: change_view("book_detail", b) if is_avail else show_toast("หนังสือถูกยืมไปแล้ว ติดต่อบรรณารักษ์!", is_error=True)
            )

        cat_row = ft.Row(scroll="auto", spacing=10)
        selected_cat = ft.Text("ทั้งหมด", visible=False) 
        # เพิ่มตัวกรองชั้นวางหนังสือ (A-Z) แบบ Popup เพื่อความเสถียรสูงสุด
        shelf_val = ft.Text("ทั้งหมด", visible=False)
        
        def on_shelf_select(e):
            val = e.control.content.value # ดึงค่าจาก Text control ที่อยู่ข้างใน
            shelf_val.value = val
            shelf_btn_text.value = val if val != "ทั้งหมด" else "เลือก"
            shelf_btn_text.update()
            do_refresh()

        shelf_btn_text = ft.Text("เลือก", size=14, weight="black", color=C_PRIMARY)
        shelf_prefix_menu = ft.PopupMenuButton(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SUBTITLES_ROUNDED, size=16, color=C_PRIMARY),
                    shelf_btn_text,
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=18, color=C_PRIMARY),
                ], spacing=2, alignment="center"),
                padding=ft.Padding(12, 8, 12, 8), border_radius=20, bgcolor=ft.Colors.with_opacity(0.1, C_PRIMARY),
            ),
            items=[ft.PopupMenuItem(content=ft.Text("ทั้งหมด"), on_click=on_shelf_select)] + \
                  [ft.PopupMenuItem(content=ft.Text(chr(i)), on_click=on_shelf_select) for i in range(65, 91)]
        )

        def render_books(e=None):
            book_grid_container.controls.clear()
            query = search_input.value.lower() if search_input.value else ""
            sel_cat = selected_cat.value
            sel_shelf = shelf_val.value # ดึงค่าชั้นวางจากตัวแปรหลบใน
            
            display_books = [b for b in all_books if b.get('is_available') == 1]
            
            filtered = [
                b for b in display_books 
                if (not query or query in (b.get('title') or "").lower() or query in (b.get('isbn') or "").lower())
                and (sel_cat == "ทั้งหมด" or b.get('category') == sel_cat)
                and (sel_shelf == "ทั้งหมด" or (b.get('shelf_location') or "").upper().startswith(sel_shelf))
            ]

            if query or sel_cat != "ทั้งหมด" or sel_shelf != "ทั้งหมด":
                if not filtered:
                    book_grid_container.controls.append(
                        ft.Container(
                            padding=60, alignment=ft.Alignment(0, 0),
                            content=ft.Column([
                                ft.Icon(ft.Icons.SEARCH_OFF, size=64, color="#A8B2C1"),
                                ft.Text("ไม่พบหนังสือที่คุณค้นหา", size=20, weight="bold", color=C_SECONDARY),
                                ft.Text("ลองใช้หมวดหมู่หรือคำค้นหาใหม่ดูนะครับ", color=C_TEXT_SUB)
                            ], horizontal_alignment="center")
                        )
                    )
                else:
                    grid = ft.Row(spacing=20, wrap=True) 
                    for b in filtered:
                        grid.controls.append(create_book_card(b))
                    book_grid_container.controls.append(grid)
            else:
                categories = {}
                for b in display_books:
                    cat = b.get('category') or "อื่นๆ"
                    if cat not in categories: categories[cat] = []
                    categories[cat].append(b)
                
                if not categories:
                    book_grid_container.controls.append(ft.Text("ไม่มีหนังสือในคลังขณะนี้", color=C_TEXT_SUB))
                else:
                    for cat_name in sorted(categories.keys()):
                        books = categories[cat_name]
                        book_grid_container.controls.append(
                            ft.Column([
                                ft.Row([
                                    ft.Container(width=4, height=20, bgcolor=C_PRIMARY, border_radius=2),
                                    ft.Text(cat_name, size=18, weight="bold", color=C_SECONDARY),
                                    ft.Text(f"({len(books)} เล่ม)", size=14, color=C_TEXT_SUB)
                                ], spacing=10),
                                ft.Container(
                                    content=ft.Row(scroll="auto", spacing=20, controls=[create_book_card(b) for b in books]),
                                    padding=ft.Padding(0, 0, 0, 10)
                                )
                            ], spacing=15)
                        )
            
            if book_grid_container.page:
                book_grid_container.update()
            try: page.update() # เพิ่มการอัปเดตระดับหน้าด้วยเพื่อความชัวร์
            except: pass


        def set_filter(cat_name):
            selected_cat.value = cat_name
            do_refresh()

        def update_cats_ui():
            try:
                raw_cats = requests.get(f"{API_URL}/categories").json()
                cat_names = ["ทั้งหมด"] + [c if isinstance(c, str) else c.get('name') for c in raw_cats]
                
                cat_row.controls.clear()
                for c in cat_names:
                    is_active = (selected_cat.value == c)
                    cat_row.controls.append(
                        ft.Container(
                            content=ft.Text(c, size=12, weight="bold" if is_active else "normal", color="white" if is_active else C_TEXT_SUB),
                            padding=ft.Padding(12, 6, 12, 6),
                            border_radius=20,
                            bgcolor=C_PRIMARY if is_active else ft.Colors.with_opacity(0.1, C_TEXT_SUB),
                            on_click=lambda e, name=c: set_filter(name),
                            animate_scale=150
                        )
                    )
                cat_row.update()
            except: pass

        def do_refresh(e=None):
            try:
                import time
                res = requests.get(f"{API_URL}/books?t={time.time()}")
                if res.status_code == 200:
                    all_books.clear()
                    all_books.extend(res.json())
                    update_cats_ui() 
                    render_books()
                    if e: show_toast("อัปเดตข้อมูลคลังหนังสือแล้ว")
                    # Force immediate page refresh
                    page.update()
            except: pass

        search_input.on_change = render_books
        do_refresh()

        return PageLayout(
            content=ft.Column([
                ft.Row([
                    search_input,
                    ft.Column([ft.Text("ชั้นวาง", size=10, weight="bold", color=C_PRIMARY), shelf_prefix_menu], spacing=2, horizontal_alignment="center"),
                    IconButton(ft.Icons.REFRESH_ROUNDED, do_refresh, color=C_PRIMARY)
                ], spacing=15, vertical_alignment="center"),
                ft.Container(height=5),
                cat_row,
                ft.Container(height=5),
                ft.Row([
                    ft.Icon(ft.Icons.EXPLORE_ROUNDED, color=C_PRIMARY, size=24),
                    ft.Text("หนังสือที่เปิดให้ยืม", size=24, weight="black", color=C_SECONDARY),
                ], spacing=10),
                book_grid_container,
                ft.Container(height=40)
            ], spacing=25)
        )

    def BookDetailView(book):
        days_drop = ft.Dropdown(
            label="ระยะเวลาที่ต้องการยืม (วัน)", 
            options=[ft.dropdown.Option(str(i)) for i in range(1, 8)], 
            value="3", border_radius=8, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE
        )

        def do_borrow(e):
            try:
                res = requests.post(f"{API_URL}/borrow", json={"user_id": page.user_data['id'], "book_id": book['id'], "days": int(days_drop.value), "condition": "ปกติ"})
                if res.status_code == 200:
                    show_toast("ส่งคำขอยืมเรียบร้อยแล้ว")
                    change_view("user_borrows")
                else:
                    handle_api_error(res)
            except:
                show_toast("ระบบขัดข้อง", is_error=True)

        return PageLayout(
            content=ft.Column([
                ft.Container(padding=15, content=TextButton("ย้อนกลับ", lambda _: change_view("home"), icon=ft.Icons.ARROW_BACK)),
                ft.Container(
                    padding=ft.Padding(20, 0, 20, 40), expand=True,
                    content=ft.Column([
                        CardContainer(
                            padding=30,
                            content=ft.Column([
                                ft.Row([
                                    ft.Image(src=f"{API_URL}/assets/{book.get('image_name', 'default.png')}", width=240, height=340, fit="cover", border_radius=12),
                                ], alignment="center"),
                                ft.Column([
                                    ft.Text(book.get('title', 'Unknown'), size=28, weight="bold", color=C_SECONDARY),
                                    ft.Text(f"ISBN: {book.get('isbn', '-')}", color=ft.Colors.GREY_600),
                                    ft.Container(height=10),
                                    ft.Row([
                                        ft.Row([ft.Icon(ft.Icons.LAYERS_ROUNDED, color=C_PRIMARY, size=20), ft.Text(f"ชั้นวาง: {book.get('shelf_location', '-')}", weight="bold")], spacing=5),
                                        ft.Row([ft.Icon(ft.Icons.CATEGORY_ROUNDED, color=C_PRIMARY, size=20), ft.Text(f"หมวดหมู่: {book.get('category', 'ทั่วไป')}", weight="bold")], spacing=5)
                                    ], wrap=True, spacing=25),
                                    ft.Divider(height=30, color="#E5E7EB"),
                                    ft.Text("เรื่องย่อ:", weight="bold", size=16),
                                    ft.Text(book.get('synopsis', '-'), color=C_TEXT_SUB, size=14),
                                    ft.Container(height=20),
                                    ft.Row([days_drop], alignment="center"), ft.Container(height=10),
                                    PrimaryButton("ยืนยันการยืมหนังสือ", do_borrow, icon=ft.Icons.CHECK_CIRCLE)
                                ], spacing=10, horizontal_alignment="stretch")
                            ], spacing=20, tight=True)
                        )
                    ], scroll="auto")
                )
            ])
        )

    def UserBorrowsView():
        # Alias สำหรับ CustomButton ตามความต้องการของผู้ใช้ เพื่อให้ Copy-Paste ได้ทันที
        def CustomButton(text, on_click, icon=None, width=None):
            return PrimaryButton(text, on_click, icon=icon, width=width)

        def show_qr_return_modal(b):
            """ฟังก์ชันแสดง Modal บาร์โค้ด Code 128 สำหรับการคืนหนังสือ"""
            # 1. ดึงรหัสสำหรับสร้างบาร์โค้ด (ใช้ ISBN หรือ ID)
            book_id_str = str(b.get('isbn') or b.get('book_id') or b.get('id') or '000000')
            
            # 2. API บาร์โค้ด 1D (Code 128) ตามโจทย์กำหนด
            barcode_url = f"https://bwipjs-api.metafloor.com/?bcid=code128&text={book_id_str}&includetext&scale=2&rotate=N"
            
            def confirm_send_request(e):
                # [NO-TOUCH] ห้ามแก้ไข ลบ หรือดัดแปลง logic requests.put เดิม
                try:
                    res = requests.put(f"{API_URL}/user/request_return/{b['id']}")
                    if res.status_code == 200:
                        show_toast("แจ้งคืนหนังสือเรียบร้อยแล้ว (Barcode Verified)")
                        bs.open = False
                        change_view("user_borrows")
                    else:
                        handle_api_error(res)
                except:
                    show_toast("ขออภัย ระบบขัดข้องขณะส่งคำขอ", is_error=True)

            # [SAFE] ใช้ ft.Padding และ ft.BorderRadius ตามมาตรฐาน Flet 0.83.0 (Strictly No Deprecated)
            bs = ft.BottomSheet(
                ft.Container(
                    padding=ft.Padding(30, 30, 30, 30), 
                    bgcolor=C_CARD, 
                    border_radius=ft.BorderRadius(24, 24, 0, 0),
                    content=ft.Column([
                        ft.Text("คืนหนังสือด้วยบาร์โค้ด", size=22, weight="black", color=C_SECONDARY),
                        ft.Text(f"สแกนบาร์โค้ดด้านล่างเพื่อคืน: {b['title']}", size=14, color=C_TEXT_SUB),
                        ft.Container(height=15),
                        # 3. ปรับขนาด ft.Image width=300, height=100, fit="contain" ตามโจทย์
                        ft.Image(src=barcode_url, width=300, height=100, fit="contain"),
                        ft.Container(height=25),
                        # 4. ปุ่ม CustomButton (ห้ามดัดแปลงส่วนส่งคำขอ)
                        CustomButton("ส่งคำขอคืนสำเร็จ", confirm_send_request, icon=ft.Icons.CHECK_CIRCLE, width=300),
                        ft.Container(height=10)
                    ], horizontal_alignment="center", tight=True)
                )
            )
            page.overlay.append(bs)
            bs.open = True
            page.update()

        # ส่วนจัดการการแสดงผลรายการหนังสือที่กำลังยืม
        list_view = ft.Column(spacing=15, horizontal_alignment="center")
        try:
            borrows = requests.get(f"{API_URL}/user/{page.user_data['id']}/borrows").json()
            if not borrows: 
                list_view.controls.append(
                    ft.Row([
                        ft.Container(
                            padding=ft.Padding(40, 40, 40, 40), 
                            bgcolor=C_CARD, border_radius=ft.BorderRadius(16, 16, 16, 16),
                            content=ft.Column([
                                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=64, color=C_SUCCESS),
                                ft.Text("ไม่พบรายการค้างส่ง", size=20, weight="bold", color=C_SECONDARY),
                                ft.Text("ขณะนี้คุณไม่มีหนังสือที่กำลังยืมเปิดใช้งานอยู่", color=C_TEXT_SUB)
                            ], horizontal_alignment="center")
                        )
                    ], alignment="center")
                )
            for b in borrows:
                # จัดการสถานะและการแสดงผลปุ่ม
                if b['status'] == 'pending_borrow':
                    stat_ui = ft.Row([ft.Icon(ft.Icons.SCHEDULE, color=C_WARN, size=16), ft.Text("รออนุมัติ", color=C_WARN, weight="bold")], spacing=4)
                    act_btn = ft.Container() 
                elif b['status'] == 'borrowed':
                    stat_ui = ft.Row([ft.Icon(ft.Icons.AUTO_STORIES, color=C_SUCCESS, size=16), ft.Text("อยู่ระหว่างการยืม", color=C_SUCCESS, weight="bold")], spacing=4)
                    # เปลี่ยนให้เรียกใช้ Modal บาร์โค้ด Code 128
                    act_btn = SecondaryButton("ขอคืนหนังสือ", lambda e, b=b: show_qr_return_modal(b), icon=ft.Icons.QR_CODE)
                elif b['status'] == 'pending_return':
                    stat_ui = ft.Row([ft.Icon(ft.Icons.INVENTORY, color=C_PRIMARY, size=16), ft.Text("รอตรวจรับ", color=C_PRIMARY, weight="bold")], spacing=4)
                    act_btn = ft.Container()

                list_view.controls.append(CardContainer(
                    padding=15,
                    content=ft.Row([
                        ft.Image(src=f"{API_URL}/assets/{b['image_name']}", width=60, height=90, fit="cover", border_radius=ft.BorderRadius(8,8,8,8)),
                        ft.Column([ft.Text(b['title'], weight="bold", size=16, color=C_TEXT_MAIN), stat_ui], spacing=2, expand=True),
                        act_btn
                    ])
                ))
        except: pass

        return PageLayout(
            content=ft.Column([
                ft.Container(padding=ft.Padding(20, 20, 20, 10), content=ft.Text("รายการยืมของฉัน", size=24, weight="bold", color=C_SECONDARY)),
                ft.Container(content=list_view, padding=ft.Padding(20, 20, 20, 20))
            ])
        )

    def UserHistoryView():
        list_view = ft.Column(spacing=15, horizontal_alignment="center")
        try:
            hist = requests.get(f"{API_URL}/user/{page.user_data['id']}/history").json()
            if not hist: 
                list_view.controls.append(
                    ft.Row([
                        ft.Container(
                            padding=60, margin=ft.Margin(0, 40, 0, 0),
                            bgcolor=C_CARD, border_radius=16, shadow=shadow_sm(),
                            content=ft.Column([
                                ft.Icon(ft.Icons.HISTORY, size=64, color=C_TEXT_SUB),
                                ft.Text("ไม่พบประวัติการใช้งาน", size=20, weight="bold", color=C_SECONDARY),
                                ft.Text("คุณยังไม่มีประวัติการยืม-คืนหนังสือในฐานข้อมูล", color=C_TEXT_SUB)
                            ], horizontal_alignment="center", alignment="center")
                        )
                    ], alignment="center")
                )
            for h in hist:
                fine_color = C_DANGER if h['fine_amount'] > 0 else C_SUCCESS
                fine_txt = f"ค่าปรับ {h['fine_amount']}฿" if h['fine_amount'] > 0 else "ปกติ"
                list_view.controls.append(CardContainer(
                    padding=15,
                    content=ft.Row([
                        ft.Image(src=f"{API_URL}/assets/{h['image_name']}", width=50, height=75, fit="cover", border_radius=6),
                        ft.Column([
                            ft.Text(h['title'], weight="bold", size=16, color=C_TEXT_MAIN),
                            ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=C_SUCCESS, size=16), ft.Text("เสร็จสิ้น", color=C_SUCCESS, size=14)], spacing=4),
                            ft.Text(f"หมายเหตุ: {h['condition_after']}", color=C_TEXT_SUB, size=13)
                        ], spacing=2, expand=True),
                        ft.Container(padding=8, border_radius=6, bgcolor=f"{fine_color}1A", content=ft.Text(fine_txt, color=fine_color, weight="bold", size=12))
                    ])
                ))
        except: pass
        return PageLayout(
            content=ft.Column([
                ft.Container(padding=ft.Padding(20, 20, 20, 0), content=ft.Text("ประวัติการยืม-คืนที่ผ่านมา", size=24, weight="bold", color=C_SECONDARY)),
                ft.Container(content=list_view, padding=20)
            ])
        )

    # ==========================================
    # OFFICER VIEW
    # ==========================================
    def OfficerHomeView():
        borrow_list = ft.Column(spacing=15)
        return_list = ft.Column(spacing=15)
        try:
            for p in requests.get(f"{API_URL}/officer/pending_borrows").json():
                borrow_list.controls.append(CardContainer(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MENU_BOOK, color=C_PRIMARY, size=32),
                        ft.Column([
                            ft.Text(p['title'], weight="bold", size=16),
                            ft.Text(f"ผู้ขอ: {p['full_name']} | เริ่มทำรายการ: {p.get('borrow_date','')}", color=C_TEXT_SUB, size=13)
                        ], expand=True),
                        PrimaryButton("อนุมัติ", lambda e, tid=p['id']: apprv_brw(tid), icon=ft.Icons.CHECK)
                    ])
                ))
            for r in requests.get(f"{API_URL}/officer/pending_returns").json():
                return_list.controls.append(CardContainer(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ASSIGNMENT_RETURNED, color=C_WARN, size=32),
                        ft.Column([
                            ft.Text(r['title'], weight="bold", size=16),
                            ft.Text(f"ผู้ส่งคืน: {r['full_name']} | สภาพอ้างอิง: {r.get('condition_before','')}", color=C_TEXT_SUB, size=13)
                        ], expand=True),
                        SecondaryButton("ตรวจรับ", lambda e, rdata=r: show_return_modal(rdata), icon=ft.Icons.FACT_CHECK)
                    ])
                ))
        except: pass
        def apprv_brw(tid):
            res = requests.put(f"{API_URL}/officer/approve_borrow/{tid}")
            if res.status_code == 200:
                show_toast("อนุมัติเสร็จสิ้น")
                change_view("home")
            else:
                handle_api_error(res)

        return PageLayout(
            content=ft.Column([
                ft.Row([
                    ft.Text("คำขอยืมหนังสือ (รออนุมัติ)", size=20, weight="bold", color=C_SECONDARY),
                    IconButton(ft.Icons.REFRESH_ROUNDED, lambda _: change_view("home"), color=C_PRIMARY)
                ], alignment="spaceBetween"),
                ft.Container(content=borrow_list if borrow_list.controls else ft.Container(padding=20, content=ft.Text("ไม่มีรายการรออนุมัติ", color=C_TEXT_SUB)), padding=ft.Padding(20,0,20,20)),
                ft.Divider(color="#E5E7EB"),
                ft.Container(padding=20, content=ft.Text("คำขอตรวจรับคืน (ตรวจสอบสภาพ)", size=20, weight="bold", color=C_SECONDARY)),
                ft.Container(content=return_list if return_list.controls else ft.Container(padding=20, content=ft.Text("ไม่มีรายการรอตรวจรับ", color=C_TEXT_SUB)), padding=ft.Padding(20,0,20,40))
            ])
        )

    def show_return_modal(b):
        fine_reason = ft.Dropdown(
            label="สาเหตุการปรับ", options=[ft.dropdown.Option("ปกติ"), ft.dropdown.Option("เกินกำหนดคืน"), ft.dropdown.Option("ชำรุด"), ft.dropdown.Option("สูญหาย")],
            value="ปกติ", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE
        )
        cond_after = ft.TextField(label="บันทึกสภาพหนังสือ", value="ปกติ", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
        fine = ft.TextField(label="จำนวนเงินค่าปรับ (บาท)", value="0", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE, keyboard_type="number")
        
        def confirm_return(e):
            final_note = f"[{fine_reason.value}] {cond_after.value}"
            res = requests.put(f"{API_URL}/officer/approve_return/{b['id']}", json={"condition_after": final_note, "fine_amount": float(fine.value)})
            if res.status_code == 200:
                bs.open = False
                show_toast("บันทึกการรับคืนเซิร์ฟเวอร์สำเร็จ")
                change_view("home")
            else:
                handle_api_error(res)

        bs = ft.BottomSheet(
            ft.Container(
                padding=ft.Padding(35, 35, 35, 35), bgcolor=C_CARD, border_radius=ft.BorderRadius(24, 24, 0, 0),
                content=ft.Column([
                    ft.Text("ตรวจสอบสภาพและรับคืน", size=22, weight="black", color=C_SECONDARY),
                    ft.Container(padding=10, border_radius=10, bgcolor=C_BG, content=ft.Column([
                        ft.Text(f"หนังสือ: {b['title']}", weight="bold"),
                        ft.Text(f"ผู้ส่งคืน: {b['full_name']}", color=C_TEXT_SUB, size=13)
                    ], spacing=2)),
                    ft.Text("กรุณาระบุรายละเอียดสภาพหนังสือและค่าปรับหากมี", size=13, color=C_TEXT_SUB),
                    ft.Container(height=10), fine_reason, cond_after, fine, ft.Container(height=20),
                    PrimaryButton("ยืนยันการรับคืน", confirm_return, icon=ft.Icons.CHECK_CIRCLE_ROUNDED, expand=True),
                    ft.Container(height=40) # Add some bottom padding for better scrolling
                ], scroll="auto", tight=True, horizontal_alignment="center")
            )
        )
        page.overlay.append(bs)
        bs.open = True
        page.update()

    # ==========================================
    # ADMIN VIEW 
    # ==========================================
    def AdminHomeView():
        users_list = ft.Column(spacing=15)
        books_list = ft.Column(spacing=15)

        def render_users():
            users_list.controls.clear()
            try:
                for u in requests.get(f"{API_URL}/admin/users").json():
                    if u['role'] == 'admin': trail = ft.Container(padding=6, border_radius=6, bgcolor=C_PRIMARY_LIGHT, content=ft.Text("SYSTEM ADMIN", color=C_PRIMARY, size=12, weight="bold"))
                    else: trail = ft.Row([SecondaryButton("แก้ไข", lambda e, udata=u: show_edit_user_modal(udata), icon=ft.Icons.EDIT), DangerButton("ลบ", lambda e, uid=u['id']: delete_user(uid), icon=ft.Icons.DELETE)], spacing=10)
                        
                    users_list.controls.append(CardContainer(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=C_TEXT_SUB),
                            ft.Column([ft.Text(u['full_name'], weight="bold", size=16, color=C_TEXT_MAIN), ft.Text(f"Username: {u['username']} | Role: {u['role'].upper()}", size=13, color=C_TEXT_SUB)], expand=True), trail
                        ])
                    ))
            except: pass; page.update()

        def delete_user(uid):
            try:
                res = requests.delete(f"{API_URL}/admin/users/{uid}")
                if res.status_code == 200:
                    show_toast("ลบผู้ใช้กระบวนการเสร็จ")
                else:
                    handle_api_error(res)
            except:
                show_toast("ข้อขัดข้องระหว่างเชื่อมต่อ", is_error=True)
            render_users()

        def show_edit_user_modal(u):
            fn = ft.TextField(label="ชื่อ-สกุล", value=u['full_name'], border_radius=8, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
            ph = ft.TextField(label="เบอร์โทร", value=u['phone'], border_radius=8, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
            role_drop = ft.Dropdown(label="สิทธิ์เข้าถึง (Role)", options=[ft.dropdown.Option("user"), ft.dropdown.Option("officer")], value=u['role'], border_radius=8, bgcolor=C_BG, filled=True, border=ft.InputBorder.NONE)
            def confirm_edit(e):
                res = requests.put(f"{API_URL}/admin/users/{u['id']}", json={"full_name": fn.value, "phone": ph.value, "role": role_drop.value})
                if res.status_code == 200:
                    show_toast("บันทึกการแก้ไขผู้ใช้สำเร็จ")
                    bs.open = False
                    render_users()
                else:
                    handle_api_error(res)
            bs = ft.BottomSheet(
                ft.Container(
                    padding=35, bgcolor=C_CARD, border_radius=ft.BorderRadius(24, 24, 0, 0),
                    content=ft.Column([
                        ft.Text("แก้ไขข้อมูลสมาชิก", size=22, weight="black", color=C_SECONDARY),
                        ft.Text("ระบุข้อมูลสมาชิกให้ครบถ้วนเพื่อการจัดการที่แม่นยำ", size=13, color=C_TEXT_SUB),
                        ft.Container(height=15), fn, ph, role_drop, ft.Container(height=15),
                        PrimaryButton("บันทึกข้อมูล", confirm_edit, icon=ft.Icons.SAVE_ROUNDED, expand=True),
                        ft.Container(height=40)
                    ], scroll="auto", tight=True, horizontal_alignment="center")
                )
            )
            page.overlay.append(bs)
            bs.open = True
            page.update()

        def render_admin_books():
            books_list.controls.clear()
            try:
                res = requests.get(f"{API_URL}/admin/books")
                if res.status_code == 200:
                    books = res.json()
                    if not books: books_list.controls.append(ft.Text("ไม่มีข้อมูลในเซิร์ฟเวอร์", color=C_TEXT_SUB))
                    for b in books:
                        books_list.controls.append(CardContainer(
                            content=ft.Row([
                                ft.Image(src=f"{API_URL}/assets/{b.get('image_name', 'default.png')}", width=50, height=75, fit="cover", border_radius=6),
                                ft.Column([ft.Text(b['title'], weight="bold", size=16), ft.Text(f"ISBN: {b['isbn']} | ชั้น: {b['shelf_location']} | หมวด: {b.get('category','ทั่วไป')}", size=12, color=C_TEXT_SUB)], expand=True),
                                ft.Row([SecondaryButton("แก้ไข", lambda e, bdata=b: show_edit_book_modal(bdata), icon=ft.Icons.EDIT), DangerButton("ลบ", lambda e, bid=b['id']: delete_book(bid), icon=ft.Icons.DELETE)], spacing=10)
                            ])
                        ))
            except: pass; page.update()

        def delete_book(book_id):
            try:
                res = requests.delete(f"{API_URL}/admin/books/{book_id}")
                if res.status_code == 200:
                    show_toast("ลบหนังสือเสร็จสมบูรณ์")
                else:
                    handle_api_error(res)
            except:
                show_toast("ข้อขัดข้องระหว่างเชื่อมต่อ", is_error=True)
            render_admin_books()

        def show_edit_book_modal(b):
            def load_cat():
                try: return [ft.dropdown.Option(c) for c in requests.get(f"{API_URL}/categories").json()]
                except: return [ft.dropdown.Option("ทั่วไป")]
            
            t_in = ft.TextField(label="ชื่อหนังสือ (Title)", value=b['title'], border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            i_in = ft.TextField(label="ภาพปก (Image Name)", value=b['image_name'], border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            s_in = ft.TextField(label="ชั้นจัดเก็บโลเคชั่น", value=b['shelf_location'], border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            c_in = ft.Dropdown(label="หมวดหมู่คอลเลกชัน", options=load_cat(), value=b.get('category','ทั่วไป'), border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE, expand=True)
            sy_in = ft.TextField(label="เรื่องย่อ/คำบรรยาย", value=b.get('synopsis', ''), multiline=True, border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)

            def add_cat_edit(e):
                ncat = ft.TextField(label="ชื่อหมวดหมู่ใหม่", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
                def sv_edit(e):
                    if ncat.value:
                        requests.post(f"{API_URL}/categories", json={"name": ncat.value})
                        c_in.options = load_cat(); c_in.value = ncat.value
                        setattr(cdlg, "open", False); page.update()
                cdlg = ft.AlertDialog(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    title=ft.Text("สร้างหมวดหมู่ใหม่", weight="bold"), content=ncat, 
                    actions=[PrimaryButton("บันทึก", sv_edit)]
                )
                page.overlay.append(cdlg); cdlg.open = True; page.update()

            crw_edit = ft.Row([c_in, SecondaryButton("สร้างใหม่", add_cat_edit, icon=ft.Icons.ADD)])

            def cnf_ed(e):
                res = requests.put(f"{API_URL}/admin/books/{b['id']}", json={"title": t_in.value, "image_name": i_in.value, "shelf_location": s_in.value, "category": c_in.value, "synopsis": sy_in.value})
                if res.status_code == 200:
                    show_toast("อัปเดตข้อมูลสำเร็จ")
                    bs.open = False
                    render_admin_books()
                else:
                    handle_api_error(res)
            
            bs = ft.BottomSheet(ft.Container(padding=30, bgcolor=C_CARD, border_radius=20,
                content=ft.Column([
                    ft.Text("แก้ไขข้อมูลหนังสือ (Catalog)", size=20, weight="bold"), 
                    t_in, crw_edit, i_in, s_in, sy_in, 
                    PrimaryButton("บันทึก", cnf_ed, icon=ft.Icons.SAVE, expand=True) # Changed width=1000 to expand=True
                ], tight=True, scroll="auto")))
            page.overlay.append(bs); bs.open = True; page.update()

        def show_add_book_modal():
            def load_cat():
                try: return [ft.dropdown.Option(c) for c in requests.get(f"{API_URL}/categories").json()]
                except: return [ft.dropdown.Option("ทั่วไป")]
            c_in = ft.Dropdown(label="หมวดหมู่คอลเลกชัน", options=load_cat(), border_radius=12, expand=True, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            def add_cat(e):
                ncat = ft.TextField(label="ชื่อหมวดหมู่ใหม่", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
                def sv(e):
                    if ncat.value:
                        requests.post(f"{API_URL}/categories", json={"name": ncat.value})
                        c_in.options = load_cat(); c_in.value = ncat.value
                        setattr(cdlg, "open", False); page.update()
                cdlg = ft.AlertDialog(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    title=ft.Text("สร้างหมวดหมู่ใหม่", weight="bold"), content=ncat, 
                    actions=[PrimaryButton("บันทึก", sv)]
                )
                page.overlay.append(cdlg); cdlg.open = True; page.update()

            crw = ft.Row([c_in, SecondaryButton("สร้างใหม่", add_cat, icon=ft.Icons.ADD)])
            ib = ft.TextField(label="หมายเลข ISBN", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            ti = ft.TextField(label="ชื่อเรื่องหนังสือ", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            sh = ft.TextField(label="ชั้นจัดเก็บโลเคชั่น", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            im = ft.TextField(label="ภาพปก (Image Name)", border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            sy = ft.TextField(label="เรื่องย่อ/คำบรรยาย", multiline=True, border_radius=12, bgcolor=C_PRIMARY_LIGHT, filled=True, border=ft.InputBorder.NONE)
            def cadd(e):
                res = requests.post(f"{API_URL}/admin/books", json={"isbn": ib.value, "title": ti.value, "category": c_in.value, "shelf_location": sh.value, "image_name": im.value, "synopsis": sy.value})
                if res.status_code == 200:
                    show_toast("บันทึกหนังสือใหม่สำเร็จ")
                    bs.open = False
                    render_admin_books()
                else:
                    handle_api_error(res)

            bs = ft.BottomSheet(
                ft.Container(
                    padding=35, bgcolor=C_CARD, border_radius=ft.BorderRadius(24, 24, 0, 0),
                    content=ft.Column([
                        ft.Text("เพิ่มหนังสือใหม่เข้าคลัง", size=22, weight="black", color=C_SECONDARY),
                        ft.Text("ระบุข้อมูลหนังสือให้ครบถ้วนเพื่อการสืบค้นที่แม่นยำ", size=13, color=C_TEXT_SUB),
                        ft.Container(height=15), ib, ti, sh, im, crw, sy, ft.Container(height=20),
                        PrimaryButton("บันทึกหนังสือใหม่", cadd, icon=ft.Icons.CLOUD_UPLOAD_ROUNDED, expand=True)
                    ], tight=True, scroll="auto")
                )
            )
            page.overlay.append(bs)
            bs.open = True
            page.update()

        render_admin_books()
        render_users()

        return PageLayout(
            content=ft.Column([
                ft.Row([
                    ft.Text("การจัดการคลังหนังสือ", size=22, weight="bold", color=C_SECONDARY),
                    PrimaryButton("เพิ่มข้อมูลใหม่", lambda _: show_add_book_modal(), icon=ft.Icons.ADD)
                ], alignment="spaceBetween"),
                books_list,
                ft.Container(height=30),
                ft.Text("การจัดการบุคลากร", size=22, weight="bold", color=C_SECONDARY),
                users_list,
                ft.Container(height=40)
            ], spacing=20)
        )

    change_view("login")

if __name__ == "__main__":
    # view=ft.AppView.WEB_BROWSER จะเปลี่ยนแอปเป็นรูปแบบเว็บแอป
    # host="0.0.0.0" คือการเปิดประตูให้มือถือในวง Wi-Fi เดียวกันเข้ามาได้
    # port=8550 กำหนดพอร์ตให้เข้าใช้งาน
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550, assets_dir="assets")