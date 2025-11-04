import psycopg2

conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres", port = 5432)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS person (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        gender char
    );
    """)

cur.execute("""
    INSERT INTO person (id, name, age, gender) VALUES  
    (1, 'Alice', 30, 'F'),
    (2, 'Bob', 25, 'M'),
    (3, 'Charlie', 35, 'M');
    """)

cur.execute("SELECT * FROM person where name = 'Bob';")

print(cur.fetchone())

cur.execute("SELECT * FROM person where age < 50;")

rows = cur.fetchall()
for row in rows:
    print(row)

sql = cur.mogrify("SELECT * FROM person where age < %s and starts_with(name, %s);", (50, 'A'))
print(sql)
cur.execute(sql)
print(cur.fetchall())
            
conn.commit()
cur.close()
conn.close()