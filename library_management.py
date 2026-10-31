
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
# -------------------- MAIN WINDOW --------------------
root = tk.Tk()
root.title("Library Book Management System")
root.geometry("1100x700")
root.configure(bg="#eef2f7")
FILE = "library_books.csv"
books = []
# -------------------- BOOK CLASS --------------------
class Book:
    def __init__(self, book_id, name, author, status="Available"):
        self.book_id = book_id
        self.name = name
        self.author = author
        self.status = status
# -------------------- FILE HANDLING --------------------
def load_books():
    if os.path.exists(FILE):
        with open(FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                books.append(Book(
                    row["ID"],
                    row["Name"],
                    row["Author"],
                    row["Status"]
                ))

    else:
        # Sample books
        books.extend([
            Book("101", "Python Programming", "Guido van Rossum"),
            Book("102", "Data Structures", "Mark Allen"),
            Book("103", "Algorithms", "Thomas Cormen"),
            Book("104", "Database Systems", "Raghu Ramakrishnan"),
            Book("105", "Artificial Intelligence", "Stuart Russell")
        ])

        save_books()

def save_books():
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["ID", "Name", "Author", "Status"])

        for book in books:
            writer.writerow([
                book.book_id,
                book.name,
                book.author,
                book.status
            ])

# -------------------- BUBBLE SORT --------------------
def bubble_sort():
    n = len(books)

    for i in range(n):
        for j in range(0, n - i - 1):

            if books[j].name.lower() > books[j + 1].name.lower():
                books[j], books[j + 1] = books[j + 1], books[j]

    display_books()
    messagebox.showinfo("Sorting", "Books sorted by name!")

# -------------------- LINEAR SEARCH --------------------
def linear_search(book_id):
    for book in books:

        if book.book_id == book_id:
            return book

    return None
# -------------------- BINARY SEARCH --------------------
def binary_search(name):

    sorted_books = sorted(books, key=lambda b: b.name.lower())

    low = 0
    high = len(sorted_books) - 1

    while low <= high:

        mid = (low + high) // 2

        current = sorted_books[mid].name.lower()
        if current == name.lower():
            return sorted_books[mid]

        elif current < name.lower():
            low = mid + 1

        else:
            high = mid - 1

    return None
# -------------------- DASHBOARD --------------------
def update_dashboard():

    total = len(books)

    available = sum(
        1 for book in books
        if book.status == "Available"
    )

    issued = total - available

    total_label.config(text=f"📚 Total Books: {total}")
    available_label.config(text=f"🟢 Available: {available}")
    issued_label.config(text=f"🔴 Issued: {issued}")

# -------------------- DISPLAY BOOKS --------------------
def display_books(data=None):

    for item in table.get_children():
        table.delete(item)

    if data is None:
        data = books

    for book in data:

        table.insert(
            "",
            tk.END,
            values=(
                book.book_id,
                book.name,
                book.author,
                book.status
            )
        )

    update_dashboard()
# -------------------- ADD BOOK --------------------
def add_book():

    book_id = id_entry.get().strip()
    name = name_entry.get().strip()
    author = author_entry.get().strip()

    if not book_id or not name or not author:
        messagebox.showwarning(
            "Missing Information",
            "Please enter ID, book name and author."
        )
        return

    if linear_search(book_id):
        messagebox.showerror(
            "Duplicate ID",
            "Book ID already exists!"
        )
        return

    books.append(Book(book_id, name, author))

    save_books()
    display_books()
    clear_fields()

    messagebox.showinfo(
        "Success",
        "Book added successfully!"
    )
# -------------------- SEARCH BY ID --------------------
def search_by_id():

    book_id = id_entry.get().strip()

    if not book_id:
        messagebox.showwarning(
            "Search",
            "Enter Book ID first."
        )
        return

    result = linear_search(book_id)

    if result:

        display_books([result])

    else:

        messagebox.showinfo(
            "Not Found",
            "Book ID not found!"
        )
# -------------------- SEARCH BY NAME --------------------
def search_by_name():

    name = name_entry.get().strip()

    if not name:
        messagebox.showwarning(
            "Search",
            "Enter book name first."
        )
        return

    result = binary_search(name)

    if result:

        display_books([result])

    else:

        messagebox.showinfo(
            "Not Found",
            "Book name not found!"
        )

# -------------------- UPDATE BOOK --------------------

def update_book():

    book_id = id_entry.get().strip()

    book = linear_search(book_id)

    if not book:

        messagebox.showerror(
            "Error",
            "Book ID not found!"
        )
        return

    name = name_entry.get().strip()
    author = author_entry.get().strip()

    if name:
        book.name = name

    if author:
        book.author = author

    save_books()
    display_books()
    clear_fields()

    messagebox.showinfo(
        "Updated",
        "Book details updated!"
    )
# -------------------- DELETE BOOK --------------------

def delete_book():

    book_id = id_entry.get().strip()

    book = linear_search(book_id)

    if not book:

        messagebox.showerror(
            "Error",
            "Book ID not found!"
        )
        return

    if messagebox.askyesno(
        "Confirm Delete",
        f"Delete {book.name}?"
    ):

        books.remove(book)

        save_books()
        display_books()
        clear_fields()
# -------------------- ISSUE BOOK --------------------

def issue_book():

    book_id = id_entry.get().strip()

    book = linear_search(book_id)

    if not book:

        messagebox.showerror(
            "Error",
            "Book ID not found!"
        )
        return

    if book.status == "Issued":

        messagebox.showwarning(
            "Unavailable",
            "This book is already issued!"
        )

    else:

        book.status = "Issued"

        save_books()
        display_books()

        messagebox.showinfo(
            "Success",
            "Book issued successfully!"
        )

# -------------------- RETURN BOOK --------------------

def return_book():

    book_id = id_entry.get().strip()

    book = linear_search(book_id)

    if not book:

        messagebox.showerror(
            "Error",
            "Book ID not found!"
        )
        return

    if book.status == "Available":

        messagebox.showwarning(
            "Return",
            "Book is already available!"
        )

    else:

        book.status = "Available"

        save_books()
        display_books()

        messagebox.showinfo(
            "Success",
            "Book returned successfully!"
        )
# -------------------- CLEAR FIELDS --------------------

def clear_fields():

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)

    display_books()
# -------------------- HEADER --------------------
header = tk.Frame(root, bg="#172554", height=85)
header.pack(fill="x")

tk.Label(
    header,
    text="📚 LIBRARY MANAGEMENT SYSTEM",
    font=("Arial", 23, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=20)
# -------------------- DASHBOARD --------------------

dashboard = tk.Frame(root, bg="#eef2f7")
dashboard.pack(fill="x", padx=20, pady=15)

total_label = tk.Label(
    dashboard,
    text="📚 Total Books: 0",
    font=("Arial", 12, "bold"),
    bg="#dbeafe",
    fg="#1e40af",
    width=25,
    pady=15
)

total_label.pack(side="left", padx=8)

available_label = tk.Label(
    dashboard,
    text="🟢 Available: 0",
    font=("Arial", 12, "bold"),
    bg="#dcfce7",
    fg="#166534",
    width=25,
    pady=15
)

available_label.pack(side="left", padx=8)

issued_label = tk.Label(
    dashboard,
    text="🔴 Issued: 0",
    font=("Arial", 12, "bold"),
    bg="#fee2e2",
    fg="#991b1b",
    width=25,
    pady=15
)

issued_label.pack(side="left", padx=8)
# -------------------- INPUT FORM --------------------
form = tk.LabelFrame(
    root,
    text=" Book Details ",
    font=("Arial", 12, "bold"),
    bg="white",
    padx=15,
    pady=15
)

form.pack(fill="x", padx=25, pady=10)

tk.Label(form, text="Book ID:", bg="white").grid(
    row=0, column=0, padx=8, pady=8
)

id_entry = ttk.Entry(form, width=25)
id_entry.grid(row=0, column=1, padx=8, pady=8)

tk.Label(form, text="Book Name:", bg="white").grid(
    row=0, column=2, padx=8, pady=8
)

name_entry = ttk.Entry(form, width=25)
name_entry.grid(row=0, column=3, padx=8, pady=8)

tk.Label(form, text="Author:", bg="white").grid(
    row=1, column=0, padx=8, pady=8
)

author_entry = ttk.Entry(form, width=25)
author_entry.grid(row=1, column=1, padx=8, pady=8)

# -------------------- BUTTONS --------------------

buttons = tk.Frame(root, bg="#eef2f7")
buttons.pack(fill="x", padx=25, pady=10)
def make_button(text, command, color):

    return tk.Button(
        buttons,
        text=text,
        command=command,
        bg=color,
        fg="white",
        font=("Arial", 10, "bold"),
        width=15,
        pady=8,
        relief="flat",
        cursor="hand2"
    )

make_button("➕ Add Book", add_book, "#2563eb").grid(
    row=0, column=0, padx=5, pady=5
)

make_button("🔍 Search ID", search_by_id, "#0891b2").grid(
    row=0, column=1, padx=5, pady=5
)

make_button("🔍 Search Name", search_by_name, "#7c3aed").grid(
    row=0, column=2, padx=5, pady=5
)

make_button("🔃 Sort Books", bubble_sort, "#0f766e").grid(
    row=0, column=3, padx=5, pady=5
)

make_button("✏️ Update", update_book, "#d97706").grid(
    row=1, column=0, padx=5, pady=5
)

make_button("🗑 Delete", delete_book, "#dc2626").grid(
    row=1, column=1, padx=5, pady=5
)

make_button("📖 Issue Book", issue_book, "#9333ea").grid(
    row=1, column=2, padx=5, pady=5
)

make_button("↩ Return Book", return_book, "#16a34a").grid(
    row=1, column=3, padx=5, pady=5
)

make_button("🔄 Show All", clear_fields, "#475569").grid(
    row=1, column=4, padx=5, pady=5
)

# -------------------- BOOK TABLE --------------------
table_frame = tk.Frame(root, bg="white")
table_frame.pack(fill="both", expand=True, padx=25, pady=15)
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="white",
    foreground="#172554",
    rowheight=30,
    font=("Arial", 10)
)
style.configure(
    "Treeview.Heading",
    background="#1e3a8a",
    foreground="white",
    font=("Arial", 11, "bold")
)
columns = ("ID", "Name", "Author", "Status")
table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)
for col in columns:

    table.heading(col, text=col)

    table.column(
        col,
        width=200,
        anchor="center"
    )

table.pack(fill="both", expand=True)
# -------------------- FOOTER --------------------
footer = tk.Label(
    root,
    text="DAA Mini Project | Searching • Sorting • File Handling",
    font=("Arial", 10),
    bg="#172554",
    fg="white",
    pady=10
)
footer.pack(fill="x")
# -------------------- RUN APPLICATION --------------------
load_books()
display_books()
root.mainloop()
