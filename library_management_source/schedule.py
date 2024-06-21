
import random
import psycopg2
from faker import Faker

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

def generate_schedule_data(n, room_ids, librarian_ids):
    """Sinh dữ liệu cho n bản ghi trong bảng schedule"""
    data = []
    for _ in range(n):
        timeshift = fake.time()
        date = fake.date_between(start_date='-1y', end_date='today')
        room_id = random.choice(room_ids)
        librarian_id = random.choice(librarian_ids)

        record = {
            "timeshift": timeshift,
            "date": date,
            "librarian_id": librarian_id,
            "room_id": room_id
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng schedule trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO schedule (timeshift, date, librarian_id, room_id)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    record["timeshift"],
                    record["date"],
                    record["librarian_id"],
                    record["room_id"]
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
        # Lấy danh sách room_id từ bảng self_study_and_reading_room
        room_ids = get_ids_from_table(conn, "self_study_and_reading_room", "room_id")
        # Lấy danh sách librarian_id từ bảng librarian
        librarian_ids = get_ids_from_table(conn, "librarian", "librarian_id")
        if room_ids and librarian_ids:
            # Sinh dữ liệu giả cho bảng schedule
            schedule_data = generate_schedule_data(30, room_ids, librarian_ids)  # Sinh 50 bản ghi
            # Chèn dữ liệu vào bảng schedule
            insert_data_to_db(schedule_data, conn)
            # Đóng kết nối
            conn.close()
            print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
        else:
            print("Không lấy được danh sách room_id hoặc librarian_id")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()