import tkinter as tk
from tkinter import *
from tkinter import ttk
from sql_config import *
from tkinter import simpledialog
from tkinter import messagebox
import customtkinter
from fpdf import FPDF
from PyPDF2 import PdfFileMerger
import speech_recognition as sr
import pyttsx3


"""
START - BACKEND SECTION OF FUNCTIONS
"""


def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
def add_words(word_text1, word_text2, word_entry1, word_entry2):
    entry1 = word_text1.get()
    e_1 = entry1
    entry2 = word_text2.get()
    e_2 = entry2
    sql_push = (e_1, e_2)
    mycursor = mydb.cursor()
    sqlFormula = "SELECT italy_word, english_word FROM dictionary WHERE italy_word=%s AND english_word=%s"
    mycursor.execute(sqlFormula, sql_push)
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        if len(e_1) and len(e_2) >= 1:
            sql_input(e_1, e_2)
            word_entry1.delete(0, END)
            word_entry2.delete(0, END)
            messagebox.showinfo('Succes!', f'"{e_1.upper()}" and "{e_2.upper()}" succesfuly added')
        else:
            messagebox.showinfo('Warning', 'No word entered.\nType your words and try again.')
    else:
        messagebox.showinfo('Warning', 'You already have the same pair of words.')
        word_entry1.delete(0, END)
        word_entry2.delete(0, END)

def random_word(z):
    r = sr.Recognizer()
    x = z.get()
    if x == "ITA to ENG":
        count_questions = simpledialog.askstring("Check", "How many words?")
        if count_questions != None and int(count_questions) > 0:
            count_questions = int(count_questions)
            questions = count_questions
            points = 0
            for i in range(count_questions):
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

                if bool(first_word) == True:
                    answer = simpledialog.askstring("Check", f"Write proper translation of {first_word}?")
                    count_questions -= 1
                    if len(answer) > 0:
                        if answer.lower() == second_word:
                            correct = 1
                            incorrect = 0
                            points += 1
                        else:
                            incorrect = 1
                            correct = 0
                            sql_mistake_input(first_word, second_word)
                        score_sql_input(correct, incorrect)
                elif len(first_word) == 0:
                    messagebox.showinfo('Warning', 'No word entered.\nType your word and try again.')
                score_sql_output()
            messagebox.showinfo('Scores', f'You achieved {points} good answers of {questions} questions.\n In general you had {score_sql_output()}')

    elif x == "ENG to ITA":
        count_questions = simpledialog.askstring("Check", "How many words?")
        if count_questions != None and int(count_questions) > 0:
            count_questions = int(count_questions)
            questions = count_questions
            points = 0
            for i in range(count_questions):
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

                if bool(first_word) == True:
                    answer = simpledialog.askstring("Check", f"Write proper translation of {second_word}?")
                    count_questions -= 1
                    if len(answer) > 0:
                        if answer.lower() == first_word:
                            correct = 1
                            incorrect = 0
                            points += 1
                        else:
                            incorrect = 1
                            correct = 0
                            sql_mistake_input(first_word, second_word)
                        score_sql_input(correct, incorrect)
                elif len(second_word) == 0:
                    messagebox.showinfo('Warning', 'No word entered.\nType your word and try again.')
                score_sql_output()
            messagebox.showinfo('Scores', f'You achieved {points} good answers of {questions} questions.\n In general you had {score_sql_output()}')

    elif x == "VOICE":
        count_questions = simpledialog.askstring("Check", "How many words?")
        if count_questions != None and int(count_questions) > 0:
            count_questions = int(count_questions)
            questions = count_questions
            points = 0
            for i in range(count_questions):
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

                if bool(first_word) == True:
                    try:
                        with sr.Microphone() as source2:
                            messagebox.showinfo('Warning', f'Tell in english {first_word}.')
                            # adjust the energy threshold based on
                            # the surrounding noise level
                            r.adjust_for_ambient_noise(source2, duration=0.2)
                            # listens for the user's input
                            audio2 = r.listen(source2)
                            # Using google to recognize audio
                            MyText = r.recognize_google(audio2)
                            MyText = MyText.lower()
                            SpeakText(MyText)
                            print(MyText)
                            if MyText == second_word:
                                correct = 1
                                incorrect = 0
                                points += 1
                            else:
                                incorrect = 1
                                correct = 0
                                sql_mistake_input(first_word, second_word)
                            score_sql_input(correct, incorrect)
                    except sr.UnknownValueError:
                        messagebox.showinfo('Warning', 'Cannot recognise your voice')
                score_sql_output()
            messagebox.showinfo('Scores', f'You achieved {points} good answers of {questions} questions.\n In general you had {score_sql_output()}')

    elif x == "Only Mistakes":
        count_questions = simpledialog.askstring("Check", "How many words?")
        if count_questions != None and int(count_questions) > 0:
            count_questions = int(count_questions)
            questions = count_questions
            points = 0
            for i in range(count_questions):
                characters_to_remove = "[(')]"
                rand_words = []
                mycursor = mydb.cursor()
                mycursor.execute("SELECT italy_word, english_word FROM error_dictionary ORDER BY RAND()LIMIT 1")
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

                if bool(first_word) == True:
                    answer = simpledialog.askstring("Check", f"Write proper translation of {second_word}?")
                    count_questions -= 1
                    if answer != None and len(answer) > 0:
                        if answer.lower() == first_word:
                            correct = 1
                            incorrect = 0
                            points += 1
                        else:
                            incorrect = 1
                            correct = 0
                            sql_mistake_input(first_word, second_word)
                        score_sql_input(correct, incorrect)
                elif len(second_word) == 0:
                    messagebox.showinfo('Warning', 'No word entered.\nType your word and try again.')
                score_sql_output()
            messagebox.showinfo('Scores', f'You achieved {points} good answers of {questions} questions.\n In general you had {score_sql_output()}')



def page_excercises():
    remove_widgets()
    app.title("Italian Flashcards App - Excercises")
    app.geometry('800x800')
    options_list = ["ITA to ENG", "ENG to ITA", "Only Mistakes", "VOICE"]

    value_inside = StringVar(app)
    value_inside.set("Select an Option")
    question_menu = OptionMenu(app, value_inside, *options_list)
    question_menu.pack()
    submit_button = Button(app, text='Submit', command=lambda: random_word(value_inside), width=12, bg='green')
    submit_button.pack()
    #myLabel_guess = Label(app, text="Guees:")
    #myLabel_guess.pack()
    #word_guess = StringVar()
    #word_guess_entry = Entry(app, textvariable=word_guess)
    #word_guess_entry.pack()
    #check_answer = Button(app, text="Check answer", width=12, command=lambda: guess_word(label1, label2, word_guess, word_guess_entry))
    #check_answer.pack()
    back = Button(app, text="Back", width=12, command=page_start)
    back.pack()

    #my_font = ('times', 10, '')
    #my_str = tk.StringVar()
    #label1 = tk.Label(app, textvariable=my_str, font=my_font)
    #my_str.set("GOOD!")
#
    #my_font1 = ('times', 10, '')
    #my_str1 = tk.StringVar()
    #label2 = tk.Label(app, textvariable=my_str1, font=my_font1)
    #my_str1.set("WRONG!")


def remove_widgets():
    for widget in app.winfo_children():
        widget.destroy()

def exit_app():
    app.destroy()

def page_start():
    remove_widgets()
    app.title("Italian Flashcards App")
    app.geometry('300x150')


    addwords = Button(app, text="Create New Flashcard", width=40, command=add_word)
    addwords.pack()

    excersises = Button(app, text="Excercises", width=40, command=page_excercises)
    excersises.pack()

    excersises = Button(app, text="Translator", width=40)
    excersises.pack()

    addwords = Button(app, text="Dicitionary", width=40, command=lambda: ita_eng_dict(0))
    addwords.pack()


    exitwin = Button(app, text="Exit", width=40, command=exit_app)
    exitwin.pack()
def ita_eng_dict(a):
    remove_widgets()
    app.title("Italian Flashcards App - Dictionary")
    app.geometry('800x800')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM dictionary")
    table = ttk.Treeview(app)

    vsb = Scrollbar(app, orient="vertical", command=table.yview)
    vsb.place(x=30+470+2, y=10, height=200+20)
    table.configure(yscrollcommand=vsb.set)

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
    if isinstance(a, list):
        table.selection_set(a)
    table.pack()



    search_button = tk.Button(app, text='Search record', width=12, command=search_record)
    search_button.pack()

    rename_button = tk.Button(app, text='Rename record', width=12, command=lambda: rename_record(table))
    rename_button.pack()

    count_button = tk.Button(app, text='Count records', width=12, command=sql_count_records)
    count_button.pack()

    print_button = tk.Button(app, text='Print', width=12, command=gen_pdf)
    print_button.pack()

    delete_button = tk.Button(app, text='Delete record', width=12, bg='red',
                              command=lambda: delete_record(table))
    delete_button.pack()

    back = Button(app, text="Back", width=12, command=page_start)
    back.pack()

def gen_pdf():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT italy_word, english_word FROM dictionary")
    rows = mycursor.fetchall()
    print_file = dict(rows)
    if len(print_file) > 0:
        print("PRINTED!")
        with open("myfile.txt", 'w') as f:
            for key, value in print_file.items():
                f.write('%s: %s\n' % (key, value))

        pdf = FPDF()
        # Open the text file and read its contents
        with open("myfile.txt", 'r') as f:
            text = f.read()
        pdf.add_page()
        pdf.set_font('helvetica', size=14)
        pdf.write(5, text)
        pdf.output('flashcards.pdf')
        import os
        os.startfile('flashcards.pdf')
    else:
        messagebox.showinfo('Warning', 'Cannot print empty dictionary')
        print("NOT PRINTED!")

def delete_record(table):
    test = []
    selected_item = table.selection()
    test.append(selected_item)
    x = " ".join(selected_item)
    y = x.split(" ")
    if bool(selected_item) == True:
        for i in y:
            records = []
            s = i
            result = tuple(s.split())
            records.append(result)
            sql_push = records
            mycursor = mydb.cursor()
            sqlFormula = "DELETE FROM dictionary WHERE words_ID=%s"
            mycursor.executemany(sqlFormula, sql_push)
            mydb.commit()
            remove_widgets()
            ita_eng_dict(0)
        if len(y) == 1:
            messagebox.showinfo('Warning', f'{len(y)} record deleted')
        else:
            messagebox.showinfo('Warning', f'{len(y)} records deleted')
    else:
        messagebox.showinfo('Warning', 'Select entry and try again')


def search_record():
    answer = simpledialog.askstring("Check", "What word do you want to check?")
    if answer != None:
        searching = []
        searching.append(answer)
        searching.append(answer)
        if len(answer) > 0:
            sql_push = searching
            mycursor = mydb.cursor()
            sqlFormula = "SELECT words_ID FROM dictionary WHERE english_word=%s OR italy_word=%s"
            mycursor.execute(sqlFormula, sql_push)
            myresult = mycursor.fetchall()
            x = myresult
            if len(myresult) >= 1:
                messagebox.showinfo('Check', f'{answer} is avaliable in the registry.')
                ita_eng_dict(x)
            else:
                messagebox.showinfo('Check', f'{answer} not found in the registry')
        else:
            messagebox.showinfo('Check', 'Cannot find empty value. Please insert word')
    return myresult
def rename_record(table):
    selected_item = table.selection()
    print(bool(selected_item))
    if bool(selected_item) == True:
        answer1 = simpledialog.askstring("Check", "Rename italian word:")
        answer2 = simpledialog.askstring("Check", "Rename english word:")
        if answer1 != None and answer2 != None:
            sql_push = (answer1, answer2)
            mycursor = mydb.cursor()
            sqlFormula = "SELECT italy_word, english_word FROM dictionary WHERE italy_word=%s AND english_word=%s"
            mycursor.execute(sqlFormula, sql_push)
            myresult = mycursor.fetchall()
            if len(myresult) == 0:
                selected_item = table.selection()
                x = list(selected_item[0])
                if len(x) == 2:
                    id = str(x[0] + x[1])
                    print(x)
                    print(id)
                    if len(answer1) > 0:
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
                        ita_eng_dict(0)
                    else:
                        messagebox.showinfo('Check', 'Cannot change word to empty value')
                elif len(x) == 1:
                    id = str(x[0])
                    if len(answer1) > 0:
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
                        ita_eng_dict(0)
                    else:
                        messagebox.showinfo('Check', 'Cannot change word to empty value')
                elif len(x) == 3:
                    id = str(x[0] + x[1] + x[2])
                    print(x)
                    print(id)
                    if len(answer1) > 0:
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
                        ita_eng_dict(0)
                    else:
                        messagebox.showinfo('Check', 'Cannot change word to empty value')
                elif len(x) == 4:
                    id = str(x[0] + x[1] + x[2] + x[3])
                    print(x)
                    print(id)
                    if len(answer1) > 0:
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
                        ita_eng_dict(0)
                    else:
                        messagebox.showinfo('Check', 'Cannot change word to empty value')
            else:
                messagebox.showinfo('Check', 'The same pair already exists in database')
    else:
        messagebox.showinfo('Warning', 'Select entry and try again')


def add_word():
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

    search_button = Button(app, text="Add record", width=12,
                           command=lambda: add_words(word_text1, word_text2, word_entry1, word_entry2))
    search_button.pack()
    back = Button(app, text="Back", width=12, command=page_start)
    back.pack()

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
app.iconbitmap("myIcon.ico")
page_start()



app.mainloop()
