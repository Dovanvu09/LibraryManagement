
import random
import string
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def get_student_ids(conn):
    """Lấy danh sách student_id từ bảng student"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT student_id FROM student")
        student_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return student_ids
    except Exception as e:
        print(f"Lỗi khi lấy danh sách student_id: {e}")
        return []

def generate_orderline_data(n, student_ids):
    """Sinh dữ liệu cho n bản ghi trong bảng orderline"""
    data = []
    for _ in range(n):
        orderline_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        student_id = random.choice(student_ids)
        order_time = fake.date_time_between(start_date='-2y', end_date='now')
        expiration_date = order_time.date() + timedelta(days=3)
        deadline = order_time.date() + timedelta(days=7)
        extension = random.choice(['Y', 'N'])
        if extension == 'Y':
            deadline += timedelta(days=7)
        status = random.choice(['In queue', 'Accepted', 'Cancelled', 'Successful', 'Returned'])
        if status == 'Accepted':
            order_time = fake.date_time_between(start_date=order_time, end_date='now')
            expiration_date = None
        book_return_date = order_time.date() + timedelta(days=random.randint(1, 30))
        method = random.choice(['Online', 'Offline'])
        violation = random.choice(['X', 'O'])
        
        record = {
            "orderline_id": orderline_id,
            "student_id": student_id,
            "order_time": order_time,
            "expiration_date": expiration_date,
            "deadline": deadline,
            "extension": extension,
            "status": status,
            "book_return_date": book_return_date,
            "method": method,
            "violation": violation
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng orderline trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO orderline (orderline_id, student_id, order_time, expiration_date, deadline, extension, status, book_return_date, method, violation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record["orderline_id"],
                    record["student_id"],
                    record["order_time"],
                    record["expiration_date"],
                    record["deadline"],
                    record["extension"],
                    record["status"],
                    record["book_return_date"],
                    record["method"],
                    record["violation"]
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
        # Lấy danh sách student_id từ bảng student
        student_ids = get_student_ids(conn)
        if student_ids:
            # Sinh dữ liệu giả cho bảng orderline
            orderline_data = generate_orderline_data(200, student_ids)  # Sinh 200 bản ghi
            # Chèn dữ liệu vào bảng orderline
            insert_data_to_db(orderline_data, conn)
            # Đóng kết nối
            conn.close()
            print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
        else:
            print("Không lấy được danh sách student_id từ bảng student")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()