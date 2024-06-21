
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

def generate_orders_data(orderline_ids, book_ids):
    """Sinh dữ liệu cho các bản ghi trong bảng orders"""
    data = []
    for orderline_id in orderline_ids:
        num_books = random.randint(1, 5)  # Số lượng sách trong mỗi đơn hàng từ 1 đến 5
        for _ in range(num_books):
            book_id = random.choice(book_ids)
            quantity = random.randint(1, 10)  # Số lượng mỗi loại sách từ 1 đến 10
            record = {
                "order_id": orderline_id,
                "book_id": book_id,
                "quantity": quantity
            }
            data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng orders trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO orders (order_id, book_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (
                    record["order_id"],
                    record["book_id"],
                    record["quantity"]
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
        # Lấy danh sách orderline_id từ bảng orderline
        orderline_ids = get_ids_from_table(conn, "orderline", "orderline_id")
        # Lấy danh sách book_id từ bảng book
        book_ids = get_ids_from_table(conn, "book", "book_id")
        if orderline_ids and book_ids:
            # Sinh dữ liệu giả cho bảng orders
            orders_data = generate_orders_data(orderline_ids, book_ids)  # Sinh dữ liệu cho các bản ghi
            # Chèn dữ liệu vào bảng orders
            insert_data_to_db(orders_data, conn)
            # Đóng kết nối
            conn.close()
            print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
        else:
            print("Không lấy được danh sách orderline_id hoặc book_id")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()