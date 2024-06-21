
import random
import string
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_book_id(existing_ids):
    """Sinh một book_id không trùng lặp"""
    while True:
        book_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if book_id not in existing_ids:
            existing_ids.add(book_id)
            return book_id

def generate_book_name(category):
    """Sinh tên sách có ý nghĩa dựa trên danh mục"""
    if category == "Textbooks":
        return fake.sentence(nb_words=6, variable_nb_words=True).replace('.', '')[:50]
    elif category == "Coursebooks":
        return "Introduction to " + fake.word().capitalize()
    elif category == "Reference books":
        return "The Complete Guide to " + fake.word().capitalize()
    elif category == "Novels":
        return fake.catch_phrase()[:50]
    elif category == "Children's books":
        return fake.bs().capitalize()[:50]
    elif category == "IT Book":
        return "Advanced " + fake.word().capitalize() + " Programming"
    else:
        return fake.sentence(nb_words=4).replace('.', '')[:50]

def generate_data(n):
    """Sinh dữ liệu cho n bản ghi"""
    existing_ids = set()
    categories = ["Textbooks", "Coursebooks", "Reference books", "Novels", "Children's books", "IT Book"]
    data = []
    for _ in range(n):
        category = random.choice(categories)
        record = {
            "book_id": generate_book_id(existing_ids),
            "name": generate_book_name(category),
            "author": fake.name()[:30],
            "publisher": fake.company()[:20],
            "origin": fake.country()[:15],
            "published_year": fake.date_between(start_date='-30y', end_date='today').strftime('%Y-%m-%d'),
            "category": category
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng book trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO book (book_id, name, author, publisher, origin, published_year, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record["book_id"],
                    record["name"],
                    record["author"],
                    record["publisher"],
                    record["origin"],
                    record["published_year"],
                    record["category"]
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
        # Sinh dữ liệu giả cho bảng book
        book_data = generate_data(10000)  # Thay đổi số lượng bản ghi cần sinh
        # Chèn dữ liệu vào bảng book
        insert_data_to_db(book_data, conn)
        # Đóng kết nối
        conn.close()
        print("Dữ liệu đã được thêm vào cơ sở dữ liệu")

if __name__ == "__main__":
    main()