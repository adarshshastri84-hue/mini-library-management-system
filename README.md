# Mini Library Management System

A simple command-line library management system built in Python. I made this as a mini project to practice working with file handling, functions, and data structures in Python.

It lets you manage a small book collection - you can add books, search for them, issue them to people, take returns, and view everything thats in the library. All data gets saved to a JSON file so nothing is lost between sessions.

## What it can do

- **Add Book** - Add a new book with title, author, ISBN and how many copies you have
- **Search Book** - Find books by searching title, author or ISBN (works even with partial matches)
- **Issue Book** - Give out a book to someone and it keeps track of available copies
- **Return Book** - Process a return and the copy count goes back up
- **Display All Books** - See everything in the library in a neat table
- **Display Issued Books** - Check which books are currently checked out and to whom

## Project Structure

```
library-management-system/
|-- library.py            # main program
|-- library_data.json     # gets created automatically when you first run it
|-- README.md
|-- requirements.txt
|-- PROJECT_REPORT.pdf    # detailed project report
|-- generate_report.py    # script used to make the pdf report
```

## Requirements

- Python 3.6 or above
- No extra packages needed (only uses built-in Python modules)

## How to run

1. Make sure Python is installed on your computer
2. Open terminal/command prompt in the project folder
3. Run:

```
python library.py
```

You'll see a menu like this:

```
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
+======================================+
```

Just enter the number for what you want to do and follow the prompts.

## How data is stored

Everything gets saved in `library_data.json` automatically. It looks something like this:

```json
{
  "books": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "978-0743273565",
      "total_copies": 3,
      "available_copies": 2,
      "added_on": "2026-09-29 18:50"
    }
  ],
  "issued": [
    {
      "book_id": 1,
      "book_title": "The Great Gatsby",
      "member": "Alice",
      "issued_on": "2026-09-29 18:55",
      "returned": false
    }
  ]
}
```

## Built with

- Python 3
- `json` module for saving/loading data
- `os` module for file paths
- `datetime` for timestamps

## Author

Adarsh
