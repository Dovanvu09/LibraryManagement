
import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def get_book_ids(conn):
    """Lấy danh sách book_id từ bảng book"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book")
        book_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return book_ids
    except Exception as e:
        print(f"Lỗi khi lấy danh sách book_id: {e}")
        return []

def generate_stock_data(book_ids):
    """Sinh dữ liệu cho từng book_id duy nhất trong bảng book"""
    data = []
    for book_id in book_ids:
        stock_in_date = fake.date_between(start_date='-2y', end_date='today')
        stock_out_date = stock_in_date + timedelta(days=random.randint(1, 100))
        quantity = random.randint(1, 100)
        record = {
            "book_id": book_id,
            "stock_in_date": stock_in_date.strftime('%Y-%m-%d'),
            "stock_out_date": stock_out_date.strftime('%Y-%m-%d'),
            "quantity": quantity
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng stock trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO stock (book_id, stock_in_date, stock_out_date, quantity)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    record["book_id"],
                    record["stock_in_date"],
                    record["stock_out_date"],
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
        # Lấy danh sách book_id từ bảng book
        book_ids = get_book_ids(conn)
        if book_ids:
            # Sinh dữ liệu giả cho bảng stock
            stock_data = generate_stock_data(book_ids)  # Sinh dữ liệu cho mỗi book_id duy nhất
            # Chèn dữ liệu vào bảng stock
            insert_data_to_db(stock_data, conn)
            # Đóng kết nối
            conn.close()
            print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
        else:
            print("Không lấy được danh sách book_id từ bảng book")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()