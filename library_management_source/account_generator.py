import random
import string
import csv
import psycopg2
from faker import Faker

fake = Faker()

def generate_email(existing_emails):
    """Sinh một email với đuôi @sis.hust.edu.vn không trùng lặp"""
    while True:
        local_part = fake.user_name()
        domain_part = "@sis.hust.edu.vn"
        email = local_part + domain_part
        if email not in existing_emails:
            existing_emails.add(email)
            return email

def generate_password(length=20):
    """Sinh mật khẩu ngẫu nhiên có độ dài cho trước"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))

def generate_status():
    """Sinh trạng thái ngẫu nhiên cho tài khoản"""
    statuses = ['Active', 'Warning lv1', 'Warning lv2', 'Warning lv3', 'Suspended']
    return random.choice(statuses)

def generate_data(n):
    """Sinh dữ liệu cho n bản ghi"""
    existing_emails = set()
    data = []
    for _ in range(n):
        record = {
            "email": generate_email(existing_emails),
            "password": generate_password(),
            "created_date": fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d'),
            "status": generate_status()
        }
        data.append(record)
    return data

def save_to_csv(data, filename):
    """Lưu dữ liệu vào file CSV"""
    fieldnames = ['email', 'password', 'created_date', 'status']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for record in data:
            writer.writerow(record)

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

def insert_data_from_csv(filename, conn):
    """Thêm dữ liệu từ file CSV vào bảng trong cơ sở dữ liệu PostgreSQL"""
    try:
        cursor = conn.cursor()
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Bỏ qua hàng tiêu đề
            for row in reader:
                if len(row) > 0:  # Kiểm tra xem hàng có dữ liệu không
                    cursor.execute(
                        """
                        INSERT INTO account (email, password, created_date, status)
                        VALUES (%s, %s, %s, %s)
                        """,
                        row[:4]  # Chỉ lấy 4 cột đầu tiên
                    )
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Lỗi khi thêm dữ liệu từ CSV vào cơ sở dữ liệu: {e}")
        conn.rollback()

def main():
    # Sinh dữ liệu giả và lưu vào file CSV
   
    csv_path = 'C:\\Users\\Admin\\OneDrive\\Máy tính\\db\\account.csv'   # Thay đổi đường dẫn tới thư mục khác nếu cần
    # generated_data = generate_data(1000)
    # save_to_csv(generated_data, csv_path)
    
    # Kết nối đến cơ sở dữ liệu
    conn = connect_to_db()
    if conn is not None:
        # Thêm dữ liệu từ file CSV vào cơ sở dữ liệu
        insert_data_from_csv(csv_path, conn)
        # Đóng kết nối
        conn.close()

if __name__ == "__main__":
    main()
