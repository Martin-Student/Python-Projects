import tkinter as tk
from tkinter import *
from tkinter import ttk
from sql_config import *
from tkinter import simpledialog
from tkinter import messagebox

"""
START - BACKEND SECTION OF FUNCTIONS
"""

def add_words(word_text1, word_text2, word_entry1, word_entry2):
    entry1 = word_text1.get()
    e_1 = entry1
    entry2 = word_text2.get()
    e_2 = entry2
    if len(e_1) or len(e_2) == 1:
        sql_input(e_1, e_2)
    else:
        messagebox.showinfo('Warning', 'No word entered.\nType your words and try again.')
    word_entry1.delete(0, END)
    word_entry2.delete(0, END)


def random_word():
    global first_word
    global second_word
    characters_to_remove = "[(')]"
    rand_words = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT italy_word, english_word FROM dictionary ORDER BY RAND()LIMIT 1")
    myresult = mycursor.fetchall()
    rand_words.append(myresult)
    x = str(rand_words[0])
    y = x.split(",")
    first_word = y[0]
    second_word = y[1]
    second_word = second_word[1:]

    for char in characters_to_remove:
        first_word = first_word.replace(char, '')

    for char in characters_to_remove:
        second_word = second_word.replace(char, '')

    myLabel = Label(app, text=str(first_word))
    myLabel.pack()
    return first_word, second_word

def guess_word(label1, label2, word_guess, word_guess_entry):
    guess = word_guess.get()
    x = str(guess)
    print(len(x))
    if len(x) > 0:
        if guess.lower() == second_word:
            correct = 1
            incorrect = 0
            label1.config(fg='green')
            label1.pack()
            word_guess_entry.delete(0, END)
        else:
            incorrect = 1
            correct = 0
            label2.config(fg='red')
            label2.pack()
            word_guess_entry.delete(0, END)
        score_sql_input(correct, incorrect)
    elif len(x) == 0:
        messagebox.showinfo('Warning', 'No word entered.\nType your word and try again.')

    score_sql_output()


def page_addwords():
    remove_widgets()
    app.title("Italian Flashcards App - Add Words")
    app.geometry('800x800')

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

    search_button = Button(app, text="Add record", width=12, command=lambda:add_words(word_text1, word_text2, word_entry1, word_entry2))
    search_button.pack()


    dict = Button(app, text="Show dictionary", width=12, command=ita_eng_dict)
    dict.pack()

    returno = Button(app, text="Back", width=12, command=page_start)
    returno.pack()

def page_excercises():
    remove_widgets()
    app.title("Italian Flashcards App - Excercises")
    app.geometry('800x800')
    random_record = Button(app, text="Pick a word", width=12, command=random_word)
    random_record.pack()
    myLabel_guess = Label(app, text="Guees:")
    myLabel_guess.pack()
    word_guess = StringVar()
    word_guess_entry = Entry(app, textvariable=word_guess)
    word_guess_entry.pack()
    check_answer = Button(app, text="Check answer", width=12, command=lambda: guess_word(label1, label2, word_guess, word_guess_entry))
    check_answer.pack()
    returno = Button(app, text="Back", width=12, command=page_start)
    returno.pack()

    my_font = ('times', 10, '')
    my_str = tk.StringVar()
    label1 = tk.Label(app, textvariable=my_str, font=my_font)
    my_str.set("GOOD!")

    my_font1 = ('times', 10, '')
    my_str1 = tk.StringVar()
    label2 = tk.Label(app, textvariable=my_str1, font=my_font1)
    my_str1.set("WRONG!")


    return word_guess_entry
def remove_widgets():
    for widget in app.winfo_children():
        widget.destroy()

def exit_app():
    app.destroy()

def page_start():
    remove_widgets()
    app.title("Italian Flashcards App")
    app.geometry('300x100')

    addwords = Button(app, text="Dicitionary", width=40, command=page_addwords)
    addwords.pack()

    excersises = Button(app, text="Excercises", width=40, command=page_excercises)
    excersises.pack()

    exitwin = Button(app, text="Exit", width=40, command=exit_app)
    exitwin.pack()

def ita_eng_dict():
    remove_widgets()
    app.geometry('800x800')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM dictionary")
    table = ttk.Treeview(app, selectmode='browse')
    table.grid(row=1, column=1, padx=300,pady=300)
    table["columns"]=("1", "2", "3")
    table['show']='headings'
    table.column("1", width=30, anchor='c')
    table.column("2", width=80, anchor='c')
    table.column("3", width=80, anchor='c')
    table.heading("1", text="ID")
    table.heading("2", text="Italian word")
    table.heading("3", text="English word")

    for record in mycursor:
        table.insert("", 'end', iid=record[0], values=(record[0],record[1], record[2]))
    table.pack()

    search_button = tk.Button(app, text='Search record', width=12, command=search_record)
    search_button.pack()

    rename_button = tk.Button(app, text='Rename record', width=12, command=lambda: rename_record(table))
    rename_button.pack()

    rename_button = tk.Button(app, text='Count records', width=12, command=sql_count_records)
    rename_button.pack()

    delete_button = tk.Button(app, text='Delete record', width=12, bg='red',
                              command=lambda: delete_record(table, label1))
    delete_button.pack()



    returno = Button(app, text="Back", width=12, command=page_addwords)
    returno.pack()
    my_font = ('times', 10, '')
    my_str=tk.StringVar()
    label1=tk.Label(app, textvariable=my_str, font=my_font)
    label1.config(fg='blue')
    my_str.set("msg here")

def delete_record(table, label1):
    test = []
    selected_item = table.selection()
    test.append(selected_item)
    sql_push = test
    mycursor = mydb.cursor()
    sqlFormula = "DELETE FROM dictionary WHERE words_ID=%s"
    mycursor.executemany(sqlFormula, sql_push)
    mydb.commit()
    table.delete(selected_item)
    label1.config(fg='green')
    label1.pack()

def search_record():
    answer = simpledialog.askstring("Check", "What word do you want to check?")
    searching = []
    searching.append(answer)
    searching.append(answer)
    sql_push = searching
    mycursor = mydb.cursor()
    sqlFormula = "SELECT words_ID FROM dictionary WHERE english_word=%s OR italy_word=%s"
    mycursor.execute(sqlFormula, sql_push)
    myresult = mycursor.fetchall()
    if len(myresult) == 1:
        messagebox.showinfo('Check', f'{answer} is avaliable in the registry.')
    else:
        messagebox.showinfo('Check', f'{answer} not found in the registry')

def rename_record(table):
    answer1 = simpledialog.askstring("Check", "Rename italian word:")
    answer2 = simpledialog.askstring("Check", "Rename english word:")
    selected_item = table.selection()
    x = list(selected_item[0])
    id = str(x[0] + x[1])
    sql_push = (answer1, id)
    mycursor = mydb.cursor()
    sqlFormula = "UPDATE dictionary SET italy_word=%s WHERE words_ID=%s"
    mycursor.execute(sqlFormula, sql_push)
    mydb.commit()

    sql_push = (answer2, id)
    mycursor = mydb.cursor()
    sqlFormula = "UPDATE dictionary SET english_word=%s WHERE words_ID=%s"
    mycursor.execute(sqlFormula, sql_push)
    mydb.commit()

    remove_widgets()
    ita_eng_dict()

"""
END - BACKEND SECTION OF FUNCTIONS
"""
########################################################################################################################
########################################################################################################################

"""
START - FRONTEND GUI SECTION
"""

app = tk.Tk()

app.title("Italian Flashcards App")
app.geometry('800x800')
page_start()

app.mainloop()
