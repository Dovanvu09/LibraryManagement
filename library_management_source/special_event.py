
import random
import psycopg2
from faker import Faker

fake = Faker()

def generate_special_event_data(n):
    """Sinh dữ liệu cho n bản ghi trong bảng special_event"""
    data = []
    for _ in range(n):
        name = fake.sentence(nb_words=5).replace('.', '')
        organiser = fake.company()
        sponsor = fake.company()
        description = fake.paragraph(nb_sentences=3)
        destination = fake.city()
        target_participant = fake.job()
        date = fake.date_between(start_date='-1y', end_date='today')
        schedule = fake.time()

        record = {
            "name": name,
            "organiser": organiser,
            "sponsor": sponsor,
            "description": description,
            "destination": destination,
            "target_participant": target_participant,
            "date": date,
            "schedule": schedule
        }
        data.append(record)
    return data

def insert_data_to_db(data, conn):
    """Chèn dữ liệu vào bảng special_event trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        for record in data:
            cursor.execute(
                """
                INSERT INTO special_event (name, organiser, sponsor, description, destination, target_participant, date, schedule)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record["name"],
                    record["organiser"],
                    record["sponsor"],
                    record["description"],
                    record["destination"],
                    record["target_participant"],
                    record["date"],
                    record["schedule"]
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
        # Sinh dữ liệu giả cho bảng special_event
        special_event_data = generate_special_event_data(20)  # Sinh 100 bản ghi
        # Chèn dữ liệu vào bảng special_event
        insert_data_to_db(special_event_data, conn)
        # Đóng kết nối
        conn.close()
        print("Dữ liệu đã được thêm vào cơ sở dữ liệu")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu")

if __name__ == "__main__":
    main()