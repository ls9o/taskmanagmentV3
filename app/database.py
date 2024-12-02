from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import text

DATABASE_URL = "mysql+mysqlconnector://root:my-secret-pw@localhost/mydatabase"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_sql_script(script_file):
    with engine.connect() as connection:
        with open(script_file, 'r') as file:
            sql_script = file.read()
        try:
            connection.execute(text(sql_script))
        except Exception as e:
            print(f"Error executing {script_file}: {e}")

def init_db():
    # สร้าง Session ใหม่
    db = SessionLocal()
    try:
        # รันสคริปต์ SQL เพื่อสร้างตารางผู้ใช้ (ถ้าต้องการ)
        run_sql_script('sql/create_users.sql')
        run_sql_script('sql/create_tasks.sql')
        run_sql_script('sql/create_process.sql')
        run_sql_script('sql/create_subprocess.sql')
        run_sql_script('sql/create_subtasks.sql')
        run_sql_script('sql/create_menu.sql')
        run_sql_script('sql/create_teams.sql')
        return db  # คืนค่า db หลังจากรันสคริปต์ทั้งหมด
    finally:
        db.close()  # ปิด Session เมื่อเสร็จสิ้น
        
def get_db():
    db = SessionLocal()
    try:
        yield db  # ให้การเชื่อมต่อใช้งาน
    finally:
        db.close()  # ปิดการเชื่อมต่อเมื่อเสร็จสิ้น