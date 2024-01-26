from tkinter import *
from tkinter import messagebox
from sql_config import mydb

"""
START - BACKEND SECTION OF FUNCTIONS
"""
def clear_text():
   word_entry1.delete(0, END)
   word_entry2.delete(0, END)

def add_words():
    entry1 = word_text1.get()
    global e_1
    e_1 = entry1
    entry2 = word_text2.get()
    global e_2
    e_2 = entry2
    clear_text()
    sql_input(e_1, e_2)
    return
def sql_input(x, y):
    italy_word = x
    english_word = y
    sql_push = (italy_word, english_word)
    mycursor = mydb.cursor()
    sqlFormula = "INSERT INTO dictionary (italy_word, english_word) VALUES (%s, %s)"
    mycursor.execute(sqlFormula, sql_push)
    mydb.commit()
    return

def sql_count_records():
    records = 0
    mycursor = mydb.cursor()
    mycursor.execute("SELECT italy_word FROM dictionary")
    myresult = mycursor.fetchall()
    for i in myresult:
        records += 1

    myLabel = Label(app, text=str(records) + " pairs in the dictionary")
    myLabel.pack()
    return print(records)

def random_word():
    rand_words = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT italy_word, english_word FROM dictionary ORDER BY RAND()LIMIT 1")
    myresult = mycursor.fetchall()
    rand_words.append(myresult)
    return rand_words

"""
END - BACKEND SECTION OF FUNCTIONS
"""
########################################################################################################################
########################################################################################################################

"""
START - FRONTEND GUI SECTION
"""

app = Tk()
app.title("Italian Flashcards App")
app.geometry('700x350')

word_text1 = StringVar()
word_text2 = StringVar()
myLabel_ita = Label(app, text="Italian word:")
myLabel_ita.pack()
word_entry1 = Entry(app, textvariable=word_text1)
word_entry1.pack()

myLabel_eng = Label(app, text="English word: ")
myLabel_eng.pack()
word_entry2 = Entry(app, textvariable=word_text2)
word_entry2.pack()



search_button = Button(app, text="Add record", width=12, command=add_words)
search_button.pack()
check_records = Button(app, text="Count records", width=12, command=sql_count_records)
check_records.pack()


app.mainloop()