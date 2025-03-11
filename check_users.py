import sqlite3
import os

conn = sqlite3.connect("instance/users.db")
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
mezi = input("\nEnter Akce: ")

if mezi == vstupy[0]:
    if confirm():
        cursor.execute("DELETE FROM user")
        conn.commit()
        print("Deleted all users.")
    else:
        print("Cancelled.")
elif mezi == vstupy[1]:
    if confirm():
        id = input("Enter user id: ")
        cursor.execute("DELETE FROM user WHERE id=?", (id,))
        conn.commit()
        print("Deleted user with ID:", id)
    else:
        print("Cancelled.")
elif mezi == vstupy[2]:
    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    print("\nListed the database")

conn.close()
