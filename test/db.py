# Run this once to create the documents table
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='enrollment_test'
)

cursor = connection.cursor()

# Create documents table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_documents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        lrn_id VARCHAR(12),
        document_type VARCHAR(50),
        file_name VARCHAR(255),
        file_path VARCHAR(500),
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

connection.commit()
connection.close()
print("Table created successfully!")