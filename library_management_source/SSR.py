import string
import random
import psycopg2
from faker import Faker

fake = Faker()

def generate_room_id(existing_ids):
    """Sinh một room_id không trùng lặp, bắt đầu bằng 'SSR', số đầu tiên là số tầng, hai số sau là số phòng"""
    while True:
        floor = random.randint(1, 9)
        room_number = random.randint(0, 99)
        room_id = f'SSR{floor}{room_number:02}'
        if room_id not in existing_ids:
            existing_ids.add(room_id)
            return room_id

def generate_room_number(existing_numbers):
    """Sinh một room_number không trùng lặp"""
    while True:
        room_number = ''.join(random.choices(string.digits, k=3))
        if room_number not in existing_numbers:
            existing_numbers.add(room_number)
            return room_number

def generate_ssrroom_data(n):
    """Sinh dữ liệu cho n bản ghi trong bảng self_study_and_reading_room"""
    existing_room_ids = set()
    existing_room_numbers = set()
    statuses =  ['Full', 'Available']
    data = []

    for _ in range(n):
        room_id = generate_room_id(existing_room_ids)
        room_number = generate_room_number(existing_room_numbers)
        max_capacity = random.randint(30, 50)
        current_attendant = random.randint(0, max_capacity)
        status = 'Đầy' if current_attendant >= max_capacity else 'Còn chỗ'
        record = {
            "room_id": room_id,
            "room_number": room_number,
            "current_attendant": current_attendant,
            "max_capacity": max_capacity,
            "status": status
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng self_study_and_reading_room trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO self_study_and_reading_room (room_id, room_number, current_attendant, max_capacity, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    record["room_id"],
                    record["room_number"],
                    record["current_attendant"],
                    record["max_capacity"],
                    record["status"]
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
        # Sinh dữ liệu giả cho bảng self_study_and_reading_room
        ssrroom_data = generate_ssrroom_data(50)  # Sinh 50 bản ghi
        # Chèn dữ liệu vào bảng self_study_and_reading_room
        insert_data_to_db(ssrroom_data, conn)
        # Đóng kết nối
        conn.close()
        print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()