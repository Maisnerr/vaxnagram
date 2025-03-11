import sqlite3
import os

conn = sqlite3.connect('instance/images.db')
cursor = conn.cursor()

vstupy = ["removeall", "remove", "list"]

def confirm():
    check = input("To confirm write 'yes' to delete: ")
    if check == "yes":
        return True
    else:
        return False

for i in vstupy:
    print(f"Akce: {i}")
mezi = input("\nEnter Akce:")

if(mezi==vstupy[0]):
    if(confirm()):
        cursor.execute("DELETE FROM image_data")
        conn.commit()
        print("Deleted.")
    else:
        print("Cancelled.")
elif(mezi==vstupy[1]):
    if(confirm()):
        id = input("Enter id:")
        cursor.execute("DELETE FROM image_data WHERE id=?", (id,))
        conn.commit()
        print("Deleted.")
    else:
        print("Cancelled.")
elif(mezi==vstupy[2]):
    cursor.execute("SELECT * FROM image_data")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    print("\nListed the database")

conn.close()
