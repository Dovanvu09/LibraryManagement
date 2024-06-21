
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

def get_book_stock_data(conn):
    """Lấy danh sách book_id và stock từ bảng stock"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT book_id, quantity FROM stock")
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu từ bảng stock: {e}")
        return []

def generate_archiving_data(room_ids, book_stock_data):
    """Sinh dữ liệu cho bảng archiving, đảm bảo mỗi bản ghi trong stock đều xuất hiện một lần"""
    data = []
    for book_id, stock in book_stock_data:
        room_id = random.choice(room_ids)
        in_order = random.randint(0, stock)
        away = random.randint(0, stock - in_order)
        available = stock - in_order - away
        record = {
            "room_id": room_id,
            "book_id": book_id,
            "stock": stock,
            "available": available,
            "in_order": in_order,
            "away": away
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng archiving trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO archiving (room_id, book_id, stock, available, in_order, away)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    record["room_id"],
                    record["book_id"],
                    record["stock"],
                    record["available"],
                    record["in_order"],
                    record["away"]
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
        # Lấy danh sách room_id từ bảng archive_room
        room_ids = get_ids_from_table(conn, "archive_room", "room_id")
        # Lấy danh sách book_id và stock từ bảng stock
        book_stock_data = get_book_stock_data(conn)
        if room_ids and book_stock_data:
            # Sinh dữ liệu giả cho bảng archiving
            archiving_data = generate_archiving_data(room_ids, book_stock_data)  # Sinh dữ liệu cho các bản ghi
            # Chèn dữ liệu vào bảng archiving
            insert_data_to_db(archiving_data, conn)
            # Đóng kết nối
            conn.close()
            print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
        else:
            print("Không lấy được danh sách room_id hoặc book_id và stock từ bảng stock")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()