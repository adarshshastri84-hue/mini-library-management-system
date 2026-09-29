# library.py
# A simple library management system I made using Python
# It lets you add books, search them, issue/return and see whats in the library
# Data gets saved to a json file so nothing is lost when you close the program

import json
import os
import sys
from datetime import datetime

# path to save all book data
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library_data.json")


def load_data():
    """loads saved data from json file, or starts fresh if file doesnt exist"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"books": [], "issued": []}


def save_data(data):
    """saves everything to json file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_next_id(books):
    """figures out what id to give the next book"""
    if not books:
        return 1
    return max(book["id"] for book in books) + 1


# ---- functions for each menu option ----

def add_book(data):
    """takes book info from user and adds it to the library"""
    print("\n--- Add a New Book ---")
    title = input("  Title          : ").strip()
    author = input("  Author         : ").strip()
    isbn = input("  ISBN           : ").strip()
    copies_input = input("  No. of copies  : ").strip()

    # basic validation - need at least title and author
    if not title or not author:
        print("  Error: Title and Author are required.")
        return

    # handle copies - default to 1 if left blank
    try:
        copies = int(copies_input) if copies_input else 1
        if copies < 1:
            raise ValueError
    except ValueError:
        print("  Error: Copies must be a positive number.")
        return

    # make sure same isbn isnt already there
    if isbn and any(b["isbn"] == isbn for b in data["books"]):
        print(f"  Error: A book with ISBN '{isbn}' already exists.")
        return

    new_book = {
        "id": get_next_id(data["books"]),
        "title": title,
        "author": author,
        "isbn": isbn if isbn else "N/A",
        "total_copies": copies,
        "available_copies": copies,
        "added_on": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    data["books"].append(new_book)
    save_data(data)
    print(f"  Book added! (ID: {new_book['id']})")


def search_book(data):
    """search for a book by title, author or isbn"""
    print("\n--- Search Books ---")
    query = input("  Enter title, author, or ISBN: ").strip().lower()
    if not query:
        print("  Please enter something to search for.")
        return

    # check title, author and isbn for matches
    results = [
        b for b in data["books"]
        if query in b["title"].lower()
        or query in b["author"].lower()
        or query in b["isbn"].lower()
    ]

    if not results:
        print("  No matching books found.")
        return

    print(f"\n  Found {len(results)} result(s):\n")
    show_books_table(results)


def issue_book(data):
    """issue a book to a member - checks if copies are available first"""
    print("\n--- Issue a Book ---")
    book_id_input = input("  Book ID        : ").strip()
    member = input("  Member Name    : ").strip()

    if not member:
        print("  Error: Member name is required.")
        return

    try:
        book_id = int(book_id_input)
    except ValueError:
        print("  Error: Book ID should be a number.")
        return

    # find the book
    book = None
    for b in data["books"]:
        if b["id"] == book_id:
            book = b
            break

    if book is None:
        print(f"  Error: No book with ID {book_id}.")
        return

    if book["available_copies"] < 1:
        print(f"  Sorry, '{book['title']}' has no copies available right now.")
        return

    # all good, issue it
    book["available_copies"] -= 1
    record = {
        "book_id": book_id,
        "book_title": book["title"],
        "member": member,
        "issued_on": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "returned": False,
    }
    data["issued"].append(record)
    save_data(data)

    print(f"  '{book['title']}' issued to {member}.")
    print(f"  Copies left: {book['available_copies']}")


def return_book(data):
    """handles returning a book that was issued earlier"""
    print("\n--- Return a Book ---")
    book_id_input = input("  Book ID        : ").strip()
    member = input("  Member Name    : ").strip()

    try:
        book_id = int(book_id_input)
    except ValueError:
        print("  Error: Book ID should be a number.")
        return

    # find the book first
    book = None
    for b in data["books"]:
        if b["id"] == book_id:
            book = b
            break

    if book is None:
        print(f"  Error: No book with ID {book_id}.")
        return

    # look for an active issue record matching this book and member
    issue_record = None
    for r in data["issued"]:
        if (r["book_id"] == book_id
                and r["member"].lower() == member.lower()
                and not r["returned"]):
            issue_record = r
            break

    if issue_record is None:
        print(f"  Couldn't find an active issue for '{book['title']}' by {member}.")
        return

    # mark as returned
    issue_record["returned"] = True
    issue_record["returned_on"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    book["available_copies"] += 1
    save_data(data)

    print(f"  '{book['title']}' returned by {member}.")
    print(f"  Available copies now: {book['available_copies']}")


def display_books(data):
    """shows all books in the library"""
    print("\n--- Library Catalogue ---")
    if not data["books"]:
        print("  No books in the library yet. Try adding some!")
        return

    show_books_table(data["books"])

    # show a quick summary at the bottom
    total = len(data["books"])
    total_copies = sum(b["total_copies"] for b in data["books"])
    avail = sum(b["available_copies"] for b in data["books"])
    print(f"  Total titles: {total} | Total copies: {total_copies} | Available: {avail}")


def display_issued(data):
    """shows which books are currently issued out"""
    print("\n--- Currently Issued Books ---")
    active = [r for r in data["issued"] if not r["returned"]]
    if not active:
        print("  No books are currently issued.")
        return

    header = f"  {'Book ID':<9}{'Title':<30}{'Member':<20}{'Issued On':<18}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for r in active:
        print(f"  {r['book_id']:<9}{r['book_title']:<30}{r['member']:<20}{r['issued_on']:<18}")
    print()


# ---- helper to print books as a table ----

def show_books_table(books):
    """prints books in a nice table format"""
    header = f"  {'ID':<6}{'Title':<30}{'Author':<22}{'ISBN':<16}{'Copies':<9}{'Avail':<7}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for b in books:
        # truncate long titles/authors so table doesnt break
        title = b['title'][:28]
        author = b['author'][:20]
        print(
            f"  {b['id']:<6}"
            f"{title:<30}"
            f"{author:<22}"
            f"{b['isbn']:<16}"
            f"{b['total_copies']:<9}"
            f"{b['available_copies']:<7}"
        )
    print()


# ---- main menu ----

def show_menu():
    print("""
+======================================+
|   LIBRARY MANAGEMENT SYSTEM          |
+======================================+
|  1. Add Book                         |
|  2. Search Book                      |
|  3. Issue Book                       |
|  4. Return Book                      |
|  5. Display All Books                |
|  6. Display Issued Books             |
|  0. Exit                             |
+======================================+""")


def main():
    data = load_data()
    print("\n  Welcome to the Library Management System!")

    while True:
        show_menu()
        choice = input("\n  Enter your choice: ").strip()

        if choice == "0":
            print("\n  Thanks for using the system. Bye!\n")
            break
        elif choice == "1":
            add_book(data)
        elif choice == "2":
            search_book(data)
        elif choice == "3":
            issue_book(data)
        elif choice == "4":
            return_book(data)
        elif choice == "5":
            display_books(data)
        elif choice == "6":
            display_issued(data)
        else:
            print("  Invalid choice, try again.")


if __name__ == "__main__":
    main()
