import mysql.connector
from tkinter import messagebox

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="lama",
  database="mydatabase"
)


def sql_input(x, y):
  italy_word = x
  english_word = y
  sql_push = (italy_word, english_word)
  mycursor = mydb.cursor()
  sqlFormula = "INSERT INTO dictionary (italy_word, english_word) VALUES (%s, %s)"
  mycursor.execute(sqlFormula, sql_push)
  mydb.commit()
  return

def sql_mistake_input(x, y):
  italy_word = x
  english_word = y

  sql_push = (italy_word, english_word)
  mycursor = mydb.cursor()
  sqlFormula = "SELECT italy_word, english_word FROM error_dictionary WHERE italy_word=%s AND english_word=%s"
  mycursor.execute(sqlFormula, sql_push)
  myresult = mycursor.fetchall()

  if len(myresult) == 0:
    sql_push = (italy_word, english_word)
    mycursor = mydb.cursor()
    sqlFormula = "INSERT INTO error_dictionary (italy_word, english_word) VALUES (%s, %s)"
    mycursor.execute(sqlFormula, sql_push)
    mydb.commit()
  else:
    print("bad word")


def sql_count_records():
  records = 0
  mycursor = mydb.cursor()
  mycursor.execute("SELECT italy_word FROM dictionary")
  myresult = mycursor.fetchall()
  for i in myresult:
    records += 1

  messagebox.showinfo(title="Records", message=f"{records} pairs of records in database")
  return

def score_sql_input(x, y):
    if x > 0:
      cr = []
      cr.append(x)
      sql_push = cr
      mycursor = mydb.cursor()
      sqlFormula = "INSERT INTO scores (correct, incorrect) VALUES (%s, 0)"
      mycursor.execute(sqlFormula, sql_push)
      mydb.commit()

    elif y > 0:
      incr = []
      incr.append(y)
      sql_push = incr
      mycursor = mydb.cursor()
      sqlFormula = "INSERT INTO scores (incorrect, correct) VALUES (%s, 0)"
      mycursor.execute(sqlFormula, sql_push)
      mydb.commit()


def score_sql_output():
  characters_to_remove = "[(')], "
  points_correct = []
  mycursor = mydb.cursor()
  mycursor.execute("SELECT correct FROM scores")
  myresult = mycursor.fetchall()
  points_correct.append(myresult)

  x = str(points_correct[0])
  for char in characters_to_remove:
    x = x.replace(char, '')
  sum_of_correct = 0
  for digit in x:
    if digit.isdigit():
      sum_of_correct += int(digit)
  print("Poprawne: " + str(sum_of_correct))

  points_incorrect = []
  mycursor = mydb.cursor()
  mycursor.execute("SELECT incorrect FROM scores")
  myresult = mycursor.fetchall()
  points_incorrect.append(myresult)
  y = str(points_incorrect[0])
  for char in characters_to_remove:
    y = y.replace(char, '')
  sum_of_incorrect = 0
  for digit in y:
    if digit.isdigit():
      sum_of_incorrect += int(digit)
  print("Niepoprawne: " + str(sum_of_incorrect))
  final_count = (f"{sum_of_correct} good answers and {sum_of_incorrect} wrong answers")

  return final_count