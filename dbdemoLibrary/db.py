# ============================================================
#  db.py — ชั้นติดต่อฐานข้อมูล  ★★★ นิสิตเขียน SQL ในไฟล์นี้ ★★★
#  มองหาคำว่า  # TODO  ทุกฟังก์ชัน — ใช้ %s เป็น placeholder เสมอ (กัน SQL injection)
# ============================================================
import mysql.connector
import config


def get_connection():
    
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)


def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ()); rows = cur.fetchall()
    cur.close(); conn.close(); return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


def _todo(name):
    raise NotImplementedError(f"TODO: ยังไม่ได้เขียนฟังก์ชัน {name} ใน db.py")


# ---------- สมาชิก (member) ----------
def search_members(filters):
    """ค้นหา สมาชิก ตามเงื่อนไข (name, gender, member_type)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM member WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    _todo("search_members")

def search_members(filters):
    sql = "SELECT * FROM member WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")
    if filters.get("gender"):
        sql += " AND gender = %s"
        params.append(filters["gender"])
    if filters.get("member_type"):
        sql += " AND member_type = %s"
        params.append(filters["member_type"])
    sql += " ORDER BY member_id"
    return run_query(sql, params)


def get_member(member_id):
    rows = run_query("SELECT * FROM member WHERE member_id = %s", (member_id,))
    return rows[0] if rows else None


def create_member(data):
    """เพิ่ม สมาชิก ใหม่ — data มีคีย์: name, gender, email, phone, member_type"""
    # TODO: INSERT INTO member (...) VALUES (%s, ...)
    _todo("create_member")


def update_member(member_id, data):
    """แก้ไข สมาชิก ตาม member_id"""
    # TODO: UPDATE member SET ... WHERE member_id=%s
    _todo("update_member")


def delete_member(member_id):
    """ลบ สมาชิก ตาม member_id"""
    # TODO: DELETE FROM member WHERE member_id=%s
    _todo("delete_member")

# ---------- หนังสือ (book_title) ----------
def search_books(filters):
    """ค้นหา หนังสือ ตามเงื่อนไข (title, author, category)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM book_title WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    _todo("search_books")

def search_books(filters):
    """ค้นหา หนังสือ ตามเงื่อนไข (title, author, category)"""
    sql = "SELECT * FROM book_title WHERE 1=1"
    params = []
    
    if filters.get("title"):
        sql += " AND title LIKE %s"
        params.append("%" + filters["title"] + "%")
    if filters.get("author"):
        sql += " AND author LIKE %s"
        params.append("%" + filters["author"] + "%")
    if filters.get("category"):
        sql += " AND category = %s"
        params.append(filters["category"])
        
    return run_query(sql, params)


def get_book(title_id):
    """ดึง หนังสือ 1 รายการตาม title_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    rows = run_query("SELECT * FROM book_title WHERE title_id = %s", (title_id,))
    return rows[0] if rows else None


def create_book(data):
    """เพิ่ม หนังสือ ใหม่ — data มีคีย์: title, author, category, publish_year"""
    return run_command(
        "INSERT INTO book_title (title, author, category, publish_year) VALUES (%s, %s, %s, %s)",
        (data["title"], data["author"], data["category"], data["publish_year"])
    )


def update_book(title_id, data):
    """แก้ไข หนังสือ ตาม title_id"""
    return run_command(
        "UPDATE book_title SET title=%s, author=%s, category=%s, publish_year=%s WHERE title_id=%s",
        (data["title"], data["author"], data["category"], data["publish_year"], title_id)
    )


def delete_book(title_id):
    """ลบ หนังสือ ตาม title_id"""
    return run_command("DELETE FROM book_title WHERE title_id=%s", (title_id,))

# ---------- การยืม (loan) ----------
def search_loans(filters):
    """ค้นหา การยืม ตามเงื่อนไข (member_id, copy_id)"""
    sql = "SELECT * FROM loan WHERE 1=1"
    params = []
    
    if filters.get("member_id"):
        sql += " AND member_id = %s"
        params.append(filters["member_id"])
    if filters.get("copy_id"):
        sql += " AND copy_id = %s"
        params.append(filters["copy_id"])
        
    return run_query(sql, params)

def get_loan(loan_id):
    """ดึง การยืม 1 รายการตาม loan_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    rows = run_query("SELECT * FROM loan WHERE loan_id = %s", (loan_id,))
    return rows[0] if rows else None

def create_loan(data):
    """เพิ่ม การยืม ใหม่ — data มีคีย์: member_id, copy_id, loan_date, due_date, return_date"""
    # ถ้าค่า return_date ส่งมาว่างเปล่า ให้ปรับเป็น None เพื่อบันทึกเป็น NULL ในฐานข้อมูล
    return_date = data.get("return_date") if data.get("return_date") else None
    return run_command(
        "INSERT INTO loan (member_id, copy_id, loan_date, due_date, return_date) VALUES (%s, %s, %s, %s, %s)",
        (data["member_id"], data["copy_id"], data["loan_date"], data["due_date"], return_date)
    )

def update_loan(loan_id, data):
    """แก้ไข การยืม ตาม loan_id"""
    return_date = data.get("return_date") if data.get("return_date") else None
    return run_command(
        "UPDATE loan SET member_id=%s, copy_id=%s, loan_date=%s, due_date=%s, return_date=%s WHERE loan_id=%s",
        (data["member_id"], data["copy_id"], data["loan_date"], data["due_date"], return_date, loan_id)
    )

def delete_loan(loan_id):
    """ลบ การยืม ตาม loan_id"""
    return run_command("DELETE FROM loan WHERE loan_id=%s", (loan_id,))

# ============================================================
#  REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
# ============================================================
def report_summary():
    """ตัวเลขสรุปบนการ์ด dashboard — คืน dict เช่น {"members": 10, ...}"""
    members = run_query("SELECT COUNT(*) AS n FROM member")[0]["n"]
    titles  = run_query("SELECT COUNT(*) AS n FROM book_title")[0]["n"]
    active  = run_query("SELECT COUNT(*) AS n FROM loan WHERE return_date IS NULL")[0]["n"]
    overdue = run_query("SELECT COUNT(*) AS n FROM loan WHERE return_date IS NULL AND due_date < CURDATE()")[0]["n"]
    
    return {
        "members": members,
        "titles": titles,
        "loans_active": active,
        "overdue": overdue
    }

def report_popular_books():
    """📈 หนังสือยอดนิยม (Most Borrowed)"""
    sql = """
        SELECT bt.title, COUNT(l.loan_id) as total_borrowed
        FROM loan l
        INNER JOIN book_copy bc ON l.copy_id = bc.copy_id
        INNER JOIN book_title bt ON bc.title_id = bt.title_id
        GROUP BY bt.title_id, bt.title
        ORDER BY total_borrowed DESC
        LIMIT 5
    """
    return run_query(sql)

def report_overdue():
    """⏰ สมาชิกค้างคืน (Overdue)"""
    sql = """
        SELECT m.name as member_name, bt.title, l.due_date, DATEDIFF(CURDATE(), l.due_date) as overdue_days
        FROM loan l
        INNER JOIN member m ON l.member_id = m.member_id
        INNER JOIN book_copy bc ON l.copy_id = bc.copy_id
        INNER JOIN book_title bt ON bc.title_id = bt.title_id
        WHERE l.return_date IS NULL AND l.due_date < CURDATE()
        ORDER BY overdue_days DESC
    """
    return run_query(sql)

def report_members_above_avg():
    """🏅 สมาชิกที่ยืมมากกว่าค่าเฉลี่ย (Above Average)"""
    sql = """
        SELECT m.member_id, m.name, COUNT(l.loan_id) as total_loans
        FROM member m
        INNER JOIN loan l ON m.member_id = l.member_id
        GROUP BY m.member_id, m.name
        HAVING COUNT(l.loan_id) > (
            SELECT AVG(loan_count)
            FROM (
                SELECT COUNT(loan_id) as loan_count
                FROM loan
                GROUP BY member_id
            ) as subquery
        )
        ORDER BY total_loans DESC
    """
    return run_query(sql)
def create_member(data):
    return run_command(
        "INSERT INTO member (name, gender, email, phone, member_type) "
        "VALUES (%s, %s, %s, %s, %s)",
        (data["name"], data["gender"], data["email"],
         data["phone"], data["member_type"]))

def update_member(member_id, data):
    return run_command(
        "UPDATE member SET name=%s, gender=%s, email=%s, "
        "phone=%s, member_type=%s WHERE member_id=%s",
        (data["name"], data["gender"], data["email"],
         data["phone"], data["member_type"], member_id))

def delete_member(member_id):
    return run_command("DELETE FROM member WHERE member_id=%s", (member_id,))

def search_books(filters):
    sql = ("SELECT t.title_id, t.title, t.author, t.category, "
           "t.publish_year, COUNT(c.copy_id) AS copies "
           "FROM book_title t "
           "LEFT JOIN book_copy c ON t.title_id = c.title_id "
           "WHERE 1=1")
    params = []
    if filters.get("title"):
        sql += " AND t.title LIKE %s"; params.append("%"+filters["title"]+"%")
    sql += " GROUP BY t.title_id, t.title, t.author, t.category, t.publish_year"
    return run_query(sql, params)


def search_loans(filters):
    sql = ("SELECT l.loan_id, m.name AS member_name, t.title, "
           "l.loan_date, l.due_date, l.return_date "
           "FROM loan l "
           "INNER JOIN member m     ON l.member_id = m.member_id "
           "INNER JOIN book_copy c  ON l.copy_id   = c.copy_id "
           "INNER JOIN book_title t ON c.title_id  = t.title_id "
           "WHERE 1=1 ORDER BY l.loan_id")
    return run_query(sql, [])

def report_summary():
    members = run_query("SELECT COUNT(*) AS n FROM member")[0]["n"]
    titles  = run_query("SELECT COUNT(*) AS n FROM book_title")[0]["n"]
    active  = run_query("SELECT COUNT(*) AS n FROM loan WHERE return_date IS NULL")[0]["n"]
    overdue = run_query("SELECT COUNT(*) AS n FROM loan "
                        "WHERE return_date IS NULL AND due_date < CURDATE()")[0]["n"]
    return {"members": members, "titles": titles,
            "loans_active": active, "overdue": overdue}

def report_popular_books():
    return run_query(
        "SELECT t.title, t.author, COUNT(*) AS borrow_count "
        "FROM loan l "
        "INNER JOIN book_copy  c ON l.copy_id  = c.copy_id "
        "INNER JOIN book_title t ON c.title_id = t.title_id "
        "GROUP BY t.title_id, t.title, t.author "
        "ORDER BY borrow_count DESC "
        "LIMIT 5")


def report_overdue():
    return run_query(
        "SELECT m.name AS member_name, t.title, l.due_date, "
        "DATEDIFF(CURDATE(), l.due_date) AS days_overdue "
        "FROM loan l "
        "INNER JOIN member m     ON l.member_id = m.member_id "
        "INNER JOIN book_copy  c ON l.copy_id   = c.copy_id "
        "INNER JOIN book_title t ON c.title_id  = t.title_id "
        "WHERE l.return_date IS NULL AND l.due_date < CURDATE() "
        "ORDER BY days_overdue DESC")


def report_members_above_avg():
    return run_query(
        "SELECT m.member_id, m.name, COUNT(*) AS loan_count "
        "FROM loan l "
        "INNER JOIN member m ON l.member_id = m.member_id "
        "GROUP BY m.member_id, m.name "
        "HAVING COUNT(*) > ( "
        "    SELECT AVG(cnt) FROM ( "
        "        SELECT COUNT(*) AS cnt FROM loan GROUP BY member_id "
        "    ) AS per_member "
        ") "
        "ORDER BY loan_count DESC")