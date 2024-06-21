
import random
import string
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def get_active_emails(conn):
    """Lấy danh sách email từ bảng account có trạng thái active"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM account WHERE status = 'Active'")
        emails = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return emails
    except Exception as e:
        print(f"Lỗi khi lấy danh sách email từ bảng account: {e}")
        return []

def generate_librarian_id(existing_ids):
    """Sinh một librarian_id không trùng lặp"""
    while True:
        librarian_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if librarian_id not in existing_ids:
            existing_ids.add(librarian_id)
            return librarian_id

def generate_librarian_data(n, emails):
    """Sinh dữ liệu cho n bản ghi trong bảng librarian"""
    existing_ids = set()
    data = []
    for _ in range(n):
        librarian_id = generate_librarian_id(existing_ids)
        first_name = fake.first_name()
        last_name = fake.last_name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=100)
        gender = random.choice(['F', 'M'])
        email = random.choice(emails)
        phone_number = '0' + ''.join(random.choices(string.digits, k=9))

        record = {
            "librarian_id": librarian_id,
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob,
            "gender": gender,
            "email": email,
            "phone_number": phone_number
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng librarian trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO librarian (librarian_id, first_name, last_name, dob, gender, email, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record["librarian_id"],
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
        # Lấy danh sách email từ bảng account có trạng thái active
        emails = get_active_emails(conn)
        if emails:
            # Sinh dữ liệu giả cho bảng librarian
            librarian_data = generate_librarian_data(10, emails)  # Sinh 50 bản ghi
            # Chèn dữ liệu vào bảng librarian
            insert_data_to_db(librarian_data, conn)
            # Đóng kết nối
            conn.close()
            print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
        else:
            print("Không lấy được danh sách email từ bảng account")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()