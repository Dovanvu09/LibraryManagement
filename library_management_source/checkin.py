
import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def get_ids_from_table(conn, table, column):
    """Lấy danh sách ID từ một bảng cụ thể"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column} FROM {table}")
        ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return ids
    except Exception as e:
        print(f"Lỗi khi lấy danh sách {column} từ bảng {table}: {e}")
        return []

def generate_check_in_data(n, student_ids, room_ids):
    """Sinh dữ liệu cho n bản ghi trong bảng Check_in"""
    data = []
    for _ in range(n):
        student_id = random.choice(student_ids)
        room_id = random.choice(room_ids)
        check_in_time = fake.date_time_between(start_date='-1y', end_date='now')
        check_out_time = check_in_time + timedelta(hours=random.randint(1, 5))  # Thời gian check_out sau check_in từ 1 đến 5 giờ

        record = {
            "student_id": student_id,
            "room_id": room_id,
            "check_in": check_in_time,
            "check_out": check_out_time
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng Check_in trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO Check_in (student_id, room_id, check_in, check_out)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    record["student_id"],
                    record["room_id"],
                    record["check_in"],
                    record["check_out"]
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
        student_ids = get_ids_from_table(conn, "student", "student_id")
        # Lấy danh sách room_id từ bảng self_study_and_reading_room
        room_ids = get_ids_from_table(conn, "self_study_and_reading_room", "room_id")
        if student_ids and room_ids:
            # Sinh dữ liệu giả cho bảng Check_in
            check_in_data = generate_check_in_data(300, student_ids, room_ids)  # Sinh 50 bản ghi
            # Chèn dữ liệu vào bảng Check_in
            insert_data_to_db(check_in_data, conn)
            # Đóng kết nối
            conn.close()
            print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
        else:
            print("Không lấy được danh sách student_id hoặc room_id")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()