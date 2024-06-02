import tkinter as tk
from tkinter import filedialog, messagebox, Tk,simpledialog
import sqlite3
import tkinter.ttk as ttk

def create_new_database():
    # Tkinter'in kök penceresini gizleyin
    root = Tk()
    root.withdraw()
    
    # Dosya kaydetme diyalog kutusunu açın ve dosya yolunu alın
    file_path = filedialog.asksaveasfilename(
        initialdir="/", 
        title="Save Database", 
        filetypes=[("Database files", "*.db")], 
        defaultextension=".db"
    )
    
    if file_path:
        try:
            # Veritabanı dosyasını oluşturun
            conn = sqlite3.connect(file_path)
            conn.close()
            # Kullanıcıya başarılı bir şekilde oluşturulduğunu bildirin
            messagebox.showinfo("New Database", f"Database created at {file_path}")
        except sqlite3.Error as e:
            # Hata durumunda kullanıcıya bildir
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            # Tkinter'in kök penceresini yok edin
            root.destroy()
def open_database():
    # Open a file dialog to select a database file
    file_path = filedialog.askopenfilename(title="Open Database", filetypes=[("Database files", "*.db")])
    if file_path:
        # Open the selected database file
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        # Add a label to display the database schema
        label = tk.Label(button_frame2_inner, text="Database schema:")
        label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

        # Add a text widget to display the database schema
        text = tk.Text(button_frame2_inner, height=10, width=50)
        text.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        # Execute a SQL query to retrieve the database schema
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        # Display the database schema in the text widget
        text.insert(tk.END, "Tables:\n")
        for table in tables:
            text.insert(tk.END, f"- {table[0]}\n")

        # Add a button to execute SQL queries
        def execute_sql():
            # Get the SQL query from the user
            query = entry.get()

            # Execute the SQL query
            cursor.execute(query)

            # Display the result of the SQL query
            result = cursor.fetchall()
            text.insert(tk.END, "Result:\n")
            for row in result:
                text.insert(tk.END, str(row) + "\n")

        # Add an entry widget to enter SQL queries
        entry = tk.Entry(button_frame2_inner, width=50)
        entry.grid(row=2, column=0, padx=(10, 0), pady=(10, 0))

        # Add a button to execute SQL queries
        button = tk.Button(button_frame2_inner, text="Execute SQL", command=execute_sql)
        button.grid(row=3, column=0, padx=(10, 0), pady=(10, 0))

        # Add a button to close the database connection
        def close_database():
            conn.close()
            button_frame2_inner.destroy()

        # Add a button to close the database connection
        button = tk.Button(button_frame2_inner, text="Close", command=close_database)
        button.grid(row=4, column=0, padx=(10, 0), pady=(10, 0))
#...
undo_stack = []


def save_changes():
    global undo_stack
    sql_command = ""  # SQL komutlarınızı buraya ekleyin
    undo_stack.append(sql_command)
    messagebox.showinfo("Save Changes", "Değişiklikler başarıyla kaydedildi!")

def undo_changes():
    global undo_stack
    if undo_stack:
        sql_command = undo_stack.pop()
        # Veritabanını aç ve değişikliği geri al
        conn = sqlite3.connect(current_file_path)
        cursor = conn.cursor()
        cursor.execute(sql_command)
        conn.commit()
        conn.close()
        messagebox.showinfo("Undo Changes", "Değişiklikler geri alındı!")
    else:
        messagebox.showinfo("Undo Changes", "Geri alma işlemi için bir geçmiş bulunamadı!")

def open_project():
    # Open a file dialog to select a database file
    file_path = filedialog.askopenfilename(title="Open Database", filetypes=[("Database files", "*.db")])
    if file_path:
        # Open the selected database file
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        # Add a label to display the database schema
        label = tk.Label(button_frame2_inner, text="Database schema:")
        label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

        # Add a text widget to display the database schema
        text = tk.Text(button_frame2_inner, height=10, width=50)
        text.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        # Execute a SQL query to retrieve the database schema
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        # Display the database schema in the text widget
        text.insert(tk.END, "Tables:\n")
        for table in tables:
            text.insert(tk.END, f"- {table[0]}\n")

        # Add a button to execute SQL queries
        def execute_sql():
            # Get the SQL query from the user
            query = entry.get()

            # Execute the SQL query
            cursor.execute(query)

            # Display the result of the SQL query
            result = cursor.fetchall()
            text.insert(tk.END, "Result:\n")
            for row in result:
                text.insert(tk.END, str(row) + "\n")

        # Add an entry widget to enter SQL queries
        entry = tk.Entry(button_frame2_inner, width=50)
        entry.grid(row=2, column=0, padx=(10, 0), pady=(10, 0))

        # Add a button to execute SQL queries
        button = tk.Button(button_frame2_inner, text="Execute SQL", command=execute_sql)
        button.grid(row=3, column=0, padx=(10, 0), pady=(10, 0))

        # Add a button to close the database connection
        def close_database():
            conn.close()
            button_frame2_inner.destroy()

        # Add a button to close the database connection
        button = tk.Button(button_frame2_inner, text="Close", command=close_database)
        button.grid(row=4, column=0, padx=(10, 0), pady=(10, 0))

def save_project():
    # Önce proje adını iste
    import sqlite3

# Veritabanını aç
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Tüm tabloları ve onların içeriğini dosyaya yaz
with open('mydatabase.sql', 'w') as f:
    for table_name in cursor.execute('SELECT name FROM sqlite_master WHERE type="table"'):
        f.write(f'DROP TABLE IF EXISTS {table_name[0]};\n')
        for row in cursor.execute(f'PRAGMA table_info({table_name[0]})'):
            f.write(f'ALTER TABLE {table_name[0]} ADD COLUMN {row[1]} {row[2]};\n')
        for row in cursor.execute(f'SELECT * FROM {table_name[0]}'):
            f.write(f'INSERT INTO {table_name[0]} VALUES({", ".join(str(x) for x in row)});\n')

# Veritabanını kapat
conn.close()

def add_database():
    # Open a file dialog to select a database file
    file_path = filedialog.askopenfilename(title="Add Database", filetypes=[("Database files", "*.db")])
    if file_path:
        # Open the selected database file
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        # Add a label to display the database name
        label = tk.Label(button_frame2_inner, text=f"Database: {file_path}")
        label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

        # Add a button to execute SQL queries
        def execute_sql():
            # Get the SQL query from the user
            query = entry.get()

            # Execute the SQL query
            cursor.execute(query)

            # Display the result of the SQL query
            result = cursor.fetchall()
            text.insert(tk.END, "Result:\n")
            for row in result:
                text.insert(tk.END, str(row) + "\n")

        # Add an entry widget to enter SQL queries
        entry = tk.Entry(button_frame2_inner, width=50)
        entry.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        # Add a button to execute SQL queries
        button = tk.Button(button_frame2_inner, text="Execute SQL", command=execute_sql)
        button.grid(row=2, column=0, padx=(10, 0), pady=(10, 0))

        # Add a button to close the database connection
        def close_database():
            conn.close()
            button_frame2_inner.destroy()

        # Add a button to close the database connection
        button = tk.Button(button_frame2_inner, text="Close", command=close_database)
        button.grid(row=3, column=0, padx=(10, 0), pady=(10, 0))
def get_database_and_table():
    root = tk.Tk()
    root.withdraw()  # Pencereyi gizle
    
    db_name = simpledialog.askstring("Veritabanı Seçimi", "Lütfen veritabanı adını girin:")
    table_name = simpledialog.askstring("Tablo Seçimi", "Lütfen tablo adını girin:")
    
    return db_name, table_name
def get_table_name():
    root = tk.Tk()
    root.withdraw()  # Pencereyi gizle
    
    table_name = simpledialog.askstring("Tablo Seçimi", "Lütfen tablo adını girin:")
    
    return table_name

def view_data():
    # Kullanıcıdan tablo adını alma penceresini gösterin
    table_name = get_table_name()
    
    print("Tablo Adı:", table_name)
    
    if table_name is None:
        return

    db_name = "my_database.db"  # Açık olan veritabanı adı

    # Veritabanını ve tabloyu seçtiğinde, tablonun içeriğini gösterin
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    # Verileri göstermek için bir pencere açın
    window = tk.Toplevel()
    window.title(f"{table_name} Verileri")

    # Tablo içeriğini gösteren bir Treeview widgeti oluşturun
    tree = ttk.Treeview(window, columns=tuple(columns), show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Her sütunun başlığını ve genişliğini ayarlayın
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Verileri Treeview'a yükleyin
    for row in rows:
        tree.insert("", tk.END, values=row)

    # Scrollbar ekle
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    # Pencereyi kapatma butonu ekle
    close_button = ttk.Button(window, text="Kapat", command=window.destroy)
    close_button.pack(side=tk.BOTTOM, pady=10)
    
def close_database():
    # Veritabanına bağlanın
    conn = sqlite3.connect("my_database.db")

    # Veritabanını kapatın
    conn.close()

    # Kullanıcıya veritabanının kapatıldığını bildirin
    messagebox.showinfo("Veritabanı Kapatıldı", "Veritabanı kapatıldı.")
import tkinter as tk
from tkinter import messagebox
import sqlite3

def view_database_structure():
    # Veritabanına bağlan
    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()

    # Tablo bilgilerini al
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    # Tablo yapısını tutmak için bir sözlük oluştur
    table_structure = {}

    # Her tablo için sütun bilgilerini al
    for table_name in tables:
        c.execute(f"PRAGMA table_info({table_name[0]})")
        columns = c.fetchall()
        table_structure[table_name[0]] = [col[1] for col in columns]

    # Veritabanını kapat
    conn.close()

    # Tablo yapısını göstermek için bir pencere oluştur
    structure_window = tk.Tk()
    structure_window.title("Database Structure")

    # Tablo yapısını göstermek için bir Text widget'ı oluştur
    structure_text = tk.Text(structure_window, height=20, width=50)
    structure_text.pack(padx=10, pady=10)

    # Her tablonun yapısını Text widget'ına ekleyin
    for table_name, columns in table_structure.items():
        structure_text.insert(tk.END, f"Table: {table_name}\n")
        structure_text.insert(tk.END, "+----------" * len(columns) + "+\n")
        structure_text.insert(tk.END, "| " + " | ".join(columns) + " |\n")
        structure_text.insert(tk.END, "+----------" * len(columns) + "+\n\n")

    # Text widget'ını salt okunur yapın
    structure_text.config(state=tk.DISABLED)

    # Pencereyi ana döngüye başlatın
    structure_window.mainloop()



def edit_programs():
    # Veritabanına bağlanın
    conn = sqlite3.connect("my_database.db")

    # Kursoor nesnesi oluşturun
    c = conn.cursor()

    # Verileri güncelleyin
    table_name = input("Tablo adını girin: ")
    id_ = int(input("Kayıt ID'sini girin: "))
    new_program_name = input("Yeni program adını girin: ")
    c.execute(f"UPDATE {table_name} SET program_name='{new_program_name}' WHERE id={id_};")

    # Değişiklikleri kaydedin
    conn.commit()

    # Veritabanını kapatın
    conn.close()

    # Güncellenmiş verileri gösterin
    view_data()

def execute_sql():
    # Veritabanına bağlanın
    conn = sqlite3.connect("my_database.db")

    # Kursoor nesnesi oluşturun
    c = conn.cursor()

    # Kullanıcıdan SQL sorgusunu alın
    sql_query = input("SQL sorgusunu girin: ")

    # SQL sorgusunu çalıştırın
    c.execute(sql_query)

    # Sonuçları kullanıcıya gösterin
    result = c.fetchall()
    if result:
        result_data = ""
        for row in result:
            result_data += str(row) + "\n"
        messagebox.showinfo("SQL Sonuçları", f"SQL sorgusunun sonuçları:\n\n" + result_data)
    else:
        messagebox.showinfo("SQL Sonuçları", "SQL sorgusunun sonucu boş. Hiçbir satır etkilenmedi.")

    # Veritabanını kapatın
    conn.close()



def create_table():
    def create_table_action():
        table_name = entry_table_name.get()
        columns = entry_columns.get()

        if table_name and columns:
            try:
                conn = sqlite3.connect("my_database.db")
                c = conn.cursor()
                c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
                conn.commit()
                messagebox.showinfo("Success", f"Table '{table_name}' created successfully.")
                conn.close()
                open_insert_data_window(table_name, columns)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                if conn:
                    conn.close()
        else:
            messagebox.showwarning("Input Error", "Please enter both table name and columns.")

    def open_insert_data_window(table_name, columns):
        insert_window = tk.Tk()
        insert_window.title("Insert Data")

        column_names = [col.split()[0] for col in columns.split(",")]
        entries = []

        for i, col_name in enumerate(column_names):
            label = tk.Label(insert_window, text=f"{col_name}:")
            label.grid(row=i, column=0)
            entry = tk.Entry(insert_window)
            entry.grid(row=i, column=1)
            entries.append(entry)

        def insert_data_action():
            values = [entry.get() for entry in entries]
            if all(values):
                try:
                    conn = sqlite3.connect("my_database.db")
                    c = conn.cursor()
                    placeholders = ', '.join(['?' for _ in values])
                    c.execute(f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})", values)
                    conn.commit()
                    messagebox.showinfo("Success", "Data inserted successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
                finally:
                    conn.close()
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")

        button_insert_data = tk.Button(insert_window, text="Insert Data", command=insert_data_action)
        button_insert_data.grid(row=len(column_names), column=0, columnspan=2)

        insert_window.mainloop()

    window = tk.Tk()
    window.title("Create Table")

    label_table_name = tk.Label(window, text="Table Name:")
    label_table_name.grid(row=0, column=0)
    entry_table_name = tk.Entry(window)
    entry_table_name.grid(row=0, column=1)

    label_columns = tk.Label(window, text="Columns (comma-separated):")
    label_columns.grid(row=1, column=0)
    entry_columns = tk.Entry(window)
    entry_columns.grid(row=1, column=1)

    button_create_table = tk.Button(window, text="Create Table", command=create_table_action)
    button_create_table.grid(row=2, column=0, columnspan=2)

    window.mainloop()

def create_index():
    def create_index_action():
        table_name = entry_table_name.get()
        index_name = entry_index_name.get()
        column_name = entry_column_name.get()

        try:
            conn = sqlite3.connect("my_database.db")
            c = conn.cursor()
            c.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column_name});")
            conn.commit()
            messagebox.showinfo("Success", f"Index '{index_name}' created successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
            window.destroy()

    window = tk.Tk()
    window.title("Create Index")

    label_table_name = tk.Label(window, text="Table Name:")
    label_table_name.grid(row=0, column=0)
    entry_table_name = tk.Entry(window)
    entry_table_name.grid(row=0, column=1)

    label_index_name = tk.Label(window, text="Index Name:")
    label_index_name.grid(row=1, column=0)
    entry_index_name = tk.Entry(window)
    entry_index_name.grid(row=1, column=1)

    label_column_name = tk.Label(window, text="Column Name:")
    label_column_name.grid(row=2, column=0)
    entry_column_name = tk.Entry(window)
    entry_column_name.grid(row=2, column=1)

    button_create_index = tk.Button(window, text="Create Index", command=create_index_action)
    button_create_index.grid(row=3, column=0, columnspan=2)

    window.mainloop()
def edit_table():
    def view_table():
        table_name = entry_table_name.get()
        conn = sqlite3.connect("my_database.db")
        c = conn.cursor()
        tree.delete(*tree.get_children())
        for row in c.execute(f"SELECT * FROM {table_name};"):
            tree.insert("", "end", values=row)
        conn.close()

    def edit_table_action():
        table_name = entry_table_name.get()
        column_name = entry_column_name.get()
        new_value = entry_new_value.get()
        condition_column = entry_condition_column.get()
        condition_value = entry_condition_value.get()

        try:
            conn = sqlite3.connect("my_database.db")
            c = conn.cursor()
            c.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?", (new_value, condition_value))
            conn.commit()
            messagebox.showinfo("Success", f"Table '{table_name}' edited successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
            window.destroy()

    window = tk.Tk()
    window.title("Edit Table")

    label_table_name = tk.Label(window, text="Table Name:")
    label_table_name.grid(row=0, column=0)
    entry_table_name = tk.Entry(window)
    entry_table_name.grid(row=0, column=1)



    label_column_name = tk.Label(window, text="Column Name to Edit:")
    label_column_name.grid(row=2, column=0)
    entry_column_name = tk.Entry(window)
    entry_column_name.grid(row=2, column=1)

    label_new_value = tk.Label(window, text="New Value:")
    label_new_value.grid(row=3, column=0)
    entry_new_value = tk.Entry(window)
    entry_new_value.grid(row=3, column=1)

    label_condition_column = tk.Label(window, text="Condition Column:")
    label_condition_column.grid(row=4, column=0)
    entry_condition_column = tk.Entry(window)
    entry_condition_column.grid(row=4, column=1)

    label_condition_value = tk.Label(window, text="Condition Value:")
    label_condition_value.grid(row=5, column=0)
    entry_condition_value = tk.Entry(window)
    entry_condition_value.grid(row=5, column=1)

    button_edit_table = tk.Button(window, text="Edit Table", command=edit_table_action)
    button_edit_table.grid(row=6, column=0, columnspan=2)

    tree = ttk.Treeview(window)
    tree.grid(row=7, column=0, columnspan=2)

    window.mainloop()
def delete_table():
    def delete_table_action():
        table_name = entry_table_name.get()
        try:
            conn = sqlite3.connect("my_database.db")
            c = conn.cursor()
            c.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()
            messagebox.showinfo("Success", f"Table '{table_name}' deleted successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
            window.destroy()

    window = tk.Tk()
    window.title("Delete Table")

    label_table_name = tk.Label(window, text="Table Name:")
    label_table_name.grid(row=0, column=0)
    entry_table_name = tk.Entry(window)
    entry_table_name.grid(row=0, column=1)

    button_delete_table = tk.Button(window, text="Delete Table", command=delete_table_action)
    button_delete_table.grid(row=1, column=0, columnspan=2)

    window.mainloop()
def print_table():
    # Pencere oluştur
    window = tk.Tk()
    window.title("Print Table")

    # Veritabanına bağlan
    conn = sqlite3.connect("my_database.db")

    # Kursoor nesnesi oluştur
    c = conn.cursor()

    # Tablo adını al
    label_table_name = tk.Label(window, text="Table Name:")
    label_table_name.grid(row=0, column=0)
    entry_table_name = tk.Entry(window)
    entry_table_name.grid(row=0, column=1)

    # Tabloyu yazdır
    def print_table_action():
        table_name = entry_table_name.get()

        # Tabloyu yazdır
        df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
        print(df)

        # Veritabanını kapat
        conn.close()

        # Pencereyi kapat
        window.destroy()

    button_print_table = tk.Button(window, text="Print Table", command=print_table_action)
    button_print_table.grid(row=1, column=0, columnspan=2)

    # Pencereyi görüntüle
    window.mainloop()
root = tk.Tk()
root.title("DB Browser for SQLite")

# First row of buttons
button_frame1 = tk.Frame(root)
button_frame1.pack(fill=tk.X, pady=(0, 10))  # add 10 pixels of vertical space below

button_frame1_inner = tk.Frame(button_frame1)
button_frame1_inner.pack(fill=tk.X, expand=True)  # center the inner frame

tk.Button(button_frame1_inner, text="Yeni Veritabanı", command=create_new_database, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").pack(side=tk.LEFT)
tk.Button(button_frame1_inner, text="Veritabanı Aç", command=open_database, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").pack(side=tk.LEFT)
tk.Button(button_frame1_inner, text="Değişiklikleri Kaydet", command=save_changes, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").pack(side=tk.LEFT)
tk.Button(button_frame1_inner, text="Değişiklikleri Geri Al", command=undo_changes, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").pack(side=tk.LEFT)
tk.Button(button_frame1_inner, text="Proje Aç", command=open_project, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").pack(side=tk.LEFT)
tk.Button(button_frame1_inner, text="Projeyi Kaydet", command=save_project, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").pack(side=tk.LEFT)
tk.Button(button_frame1_inner, text="Veritabanı Ekle", command=add_database, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").pack(side=tk.LEFT)
tk.Button(button_frame1_inner, text="Veritabanı Kapa", command=close_database, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").pack(side=tk.LEFT)

#...

# Set the background color of the inner frame to white
button_frame1_inner.config(bg="#ffffff")

#...

# Second row of buttons
button_frame2 = tk.Frame(root)
button_frame2.pack(fill=tk.X, pady=(10, 10))  # add 10 pixels of vertical space above and below

button_frame2_inner = tk.Frame(button_frame2)
button_frame2_inner.pack(side=tk.LEFT, fill=tk.X, padx=(200, 200), expand=True)
tk.Button(button_frame2_inner, text="Veritabanı Yapısı", command=view_database_structure, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").grid(row=0, column=0, padx=(10, 0))
tk.Button(button_frame2_inner, text="Veriyi Görüntüle", command=view_data, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").grid(row=0, column=1, padx=(10, 0))
tk.Button(button_frame2_inner, text="Programları Düzenle", command=edit_programs, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").grid(row=0, column=2, padx=(10, 0))
tk.Button(button_frame2_inner, text="SQL Kodunu Yürüt", command=execute_sql, relief=tk.FLAT, bd=0, highlightthickness=0, bg="#ffffff", activebackground="#ffffff", fg="#000000", activeforeground="#000000").grid(row=0, column=3, padx=(10, 0))

#...

# Set the background color of the inner frame to white
button_frame2_inner.config(bg="#ffffff")

#...
# Third row of buttons
button_frame3 = tk.Frame(root)
button_frame3.pack(fill=tk.X, pady=(10, 0))  # add 10 pixels of vertical space above

button_frame3_inner = tk.Frame(button_frame3)
button_frame3_inner.pack(fill=tk.X, expand=True)  # center the inner frame

tk.Button(button_frame3_inner, text="Tablo Oluştur", command=create_table).pack(side=tk.LEFT)
tk.Button(button_frame3_inner, text="Index Oluştur", command=create_index).pack(side=tk.LEFT)
tk.Button(button_frame3_inner, text="Tabloyu Düzenle", command=edit_table).pack(side=tk.LEFT)
tk.Button(button_frame3_inner, text="Tabloyu Sil", command=delete_table).pack(side=tk.LEFT)
tk.Button(button_frame3_inner, text="Yazdır", command=print_table).pack(side=tk.LEFT)

#...
#...
# Table structure frame
table_frame = tk.Frame(root, width=500, height=500)
table_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()