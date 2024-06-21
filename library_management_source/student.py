
import random
import string
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def read_emails_from_db(conn):
    """Đọc danh sách email từ bảng account trong cơ sở dữ liệu"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM account")
        emails = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return emails
    except Exception as e:
        print(f"Lỗi khi đọc email từ cơ sở dữ liệu: {e}")
        return []

def generate_student_id(existing_ids):
    """Sinh một student_id không trùng lặp"""
    while True:
        student_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if student_id not in existing_ids:
            existing_ids.add(student_id)
            return student_id

def generate_phone_number():
    """Sinh một chuỗi số gồm 10 số và bắt đầu bằng số 0"""
    return '0' + ''.join(random.choices(string.digits, k=9))

def generate_dob():
    """Sinh ngày sinh nằm trong khoảng từ 18 đến 24 tuổi"""
    current_date = datetime.now()
    start_date = current_date - timedelta(days=24*365)
    end_date = current_date - timedelta(days=18*365)
    dob = fake.date_between(start_date=start_date, end_date=end_date)
    return dob.strftime('%Y-%m-%d')

def generate_data(emails):
    """Sinh dữ liệu cho danh sách các email"""
    existing_ids = set()
    genders = ["M", "F"]
    data = []
    for email in emails:
        dob = generate_dob()
        record = {
            "student_id": generate_student_id(existing_ids),
            "first_name": fake.first_name()[:20],
            "last_name": fake.last_name()[:20],
            "dob": dob,
            "gender": random.choice(genders),
            "email": email,
            "phone_number": generate_phone_number()
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng student trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO student (student_id, first_name, last_name, dob, gender, email, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record["student_id"],
                    record["first_name"],
                    record["last_name"],
                    record["dob"],
                    record["gender"],
                    record["email"],
                    record["phone_number"]
                )
            )
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Lỗi khi chèn dữ liệu vào cơ sở dữ liệu: {e}")
        conn.rollback()

def connect_to_db():
    """Kết nối đến cơ sở dữ liệu PostgreSQL"""
    try:
        conn = psycopg2.connect(
            dbname="library_db",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None

def main():
    # Kết nối đến cơ sở dữ liệu
    conn = connect_to_db()
    if conn is not None:
        # Đọc email từ bảng account
        emails = read_emails_from_db(conn)
        
        # Sinh dữ liệu giả cho sinh viên dựa trên danh sách email
        student_data = generate_data(emails)
        
        # Chèn dữ liệu vào bảng student
        insert_data_to_db(student_data, conn)
        
        # Đóng kết nối
        conn.close()
        print("Dữ liệu đã được thêm vào cơ sở dữ liệu")

if __name__ == "__main__":
    main()