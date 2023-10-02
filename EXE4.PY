import sqlite3

# Create a database and connect to it
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create the Books table
c.execute('''CREATE TABLE IF NOT EXISTS Books
             (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')

# Create the Users table
c.execute('''CREATE TABLE IF NOT EXISTS Users
             (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')

# Create the Reservations table
c.execute('''CREATE TABLE IF NOT EXISTS Reservations
             (ReservationID TEXT PRIMARY KEY, BookID TEXT, UserID TEXT, ReservationDate TEXT,
             FOREIGN KEY(BookID) REFERENCES Books(BookID),
             FOREIGN KEY(UserID) REFERENCES Users(UserID))''')

# Function to add a new book to the database
def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")
    
    c.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
              (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully.")

# Function to find a book's detail based on BookID
def find_book_detail():
    book_id = input("Enter BookID: ")
    
    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.Status, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID
                 WHERE Books.BookID = ?''', (book_id,))
    result = c.fetchone()
    
    if result:
        book_id, title, author, status, user_name, user_email = result
        print("BookID:", book_id)
        print("Title:", title)
        print("Author:", author)
        print("Status:", status)
        
        if user_name:
            print("Reserved by:", user_name)
            print("Email:", user_email)
        else:
            print("Not reserved.")
    else:
        print("Book not found.")

# Function to find a book's reservation status based on BookID, Title, UserID, and ReservationID
def find_reservation_status():
    search_text = input("Enter BookID, Title, UserID, or ReservationID: ")
    
    if search_text.startswith("LB"):
        c.execute("SELECT Status FROM Books WHERE BookID = ?", (search_text,))
        result = c.fetchone()
        
        if result:
            print("Reservation status:", result[0])
        else:
            print("Book not found.")
    elif search_text.startswith("LU"):
        c.execute('''SELECT Books.Status
                     FROM Books
                     JOIN Reservations ON Books.BookID = Reservations.BookID
                     JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Users.UserID = ?''', (search_text,))
        result = c.fetchone()
        
        if result:
            print("Reservation status:", result[0])
        else:
            print("User not found.")
    elif search_text.startswith("LR"):
        c.execute('''SELECT Books.Status
                     FROM Books
                     JOIN Reservations ON Books.BookID = Reservations.BookID
                     WHERE Reservations.ReservationID = ?''', (search_text,))
        result = c.fetchone()
        
        if result:
            print("Reservation status:", result[0])
        else:
            print("Reservation not found.")
    else:
        c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.Status, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.Title = ?''', (search_text,))
        result = c.fetchall()
        
        if result:
            print("Search results:")
            for row in result:
                book_id, title, author, status, user_name, user_email = row
                print("BookID:", book_id)
                print("Title:", title)
                print("Author:", author)
                print("Status:", status)
                
                if user_name:
                    print("Reserved by:", user_name)
                    print("Email:", user_email)
                else:
                    print("Not reserved.")
        else:
            print("Book not found.")

# Function to find all the books in the database
def find_all_books():
    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.Status, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    result = c.fetchall()
    
    if result:
        print("All books in the database:")
        for row in result:
            book_id, title, author, status, user_name, user_email = row
            print("BookID:", book_id)
            print("Title:", title)
            print("Author:", author)
            print("Status:", status)
            
            if user_name:
                print("Reserved by:", user_name)
                print("Email:", user_email)
            else:
                print("Not reserved.")
    else:
        print("No books found in the database.")

# Function to modify/update book details based on its BookID
def modify_book_details():
    book_id = input("Enter BookID: ")
    
    c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    result = c.fetchone()
    
    if result:
        print("Current book details:")
        print(result)
        
        choice = input("Do you want to update the reservation status? (y/n): ")
        
        if choice.lower() == "y":
            new_status = input("Enter new reservation status: ")
            
            c.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
            c.execute("UPDATE Reservations SET Status = ? WHERE BookID = ?", (new_status, book_id))
            conn.commit()
            print("Book details updated successfully.")
        else:
            print("No modifications made.")
    else:
        print("Book not found.")

# Function to delete a book based on its BookID
def delete_book():
    book_id = input("Enter BookID: ")
    
    c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    result = c.fetchone()
    
    if result:
        c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        c.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully.")
    else:
        print("Book not found.")

# Main function to provide choices to interact with the database
def main():
    while True:
        print("\nLibrary Management System")
        print("1. Add a new book to the database")
        print("2. Find a book's detail based on BookID")
        print("3. Find a book's reservation status based on BookID, Title, UserID, or ReservationID")
        print("4. Find all the books in the database")
        print("5. Modify/update book details based on its BookID")
        print("6. Delete a book based on its BookID")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            add_book()
        elif choice == "2":
            find_book_detail()
        elif choice == "3":
            find_reservation_status()
        elif choice == "4":
            find_all_books()
        elif choice == "5":
            modify_book_details()
        elif choice == "6":
            delete_book()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

# Call the main function
main()

# Close the database connection
conn.close()