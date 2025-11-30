import sqlite3


# Connect to database (creates it if it doesn't exist)
db = sqlite3.connect('python_programming.db')
cursor = db.cursor()

# Creating the python_programming table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS python_programming (
        id INTEGER PRIMARY KEY,
        name TEXT,
        grade INTEGER
    )
''')

# Inserting the new rows
students = [
    (55, 'Carl Davis', 61),
    (66, 'Dennis Fredrickson', 88),
    (77, 'Jane Richards', 78),
    (12, 'Peyton Sawyer', 45),
    (2, 'Lucas Brooke', 99)
]

cursor.executemany(
    'INSERT OR REPLACE INTO python_programming VALUES (?, ?, ?)',
    students
)
db.commit()

print("Table created and data inserted successfully!\n")

# Selecting all records with a grade between 60 and 80
print("Students with grades between 60 and 80")
cursor.execute(
    'SELECT * FROM python_programming WHERE grade BETWEEN 60 AND 80'
)
results = cursor.fetchall()
for row in results:
    print(f"ID: {row[0]}, Name: {row[1]}, Grade: {row[2]}")

# Changing Carl Davis's grade to 65
cursor.execute(
    "UPDATE python_programming SET grade = 65 WHERE name = 'Carl Davis'"
)
db.commit()
print("\nCarl Davis's grade updated to 65")

# Deleting Dennis Fredrickson's row
cursor.execute(
    "DELETE FROM python_programming WHERE name = 'Dennis Fredrickson'"
)
db.commit()
print("Dennis Fredrickson's row deleted")

# Changing the grade of all students with an id greater than 55 to 80
cursor.execute(
    'UPDATE python_programming SET grade = 80 WHERE id > 55'
)
db.commit()
print("Updated grades for students with ID > 55 to 80\n")

# Display final table
print("=== Final Table ===")
cursor.execute('SELECT * FROM python_programming')
all_students = cursor.fetchall()
for row in all_students:
    print(f"ID: {row[0]}, Name: {row[1]}, Grade: {row[2]}")

# Close the connection
db.close()
