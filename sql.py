import mysql.connector
import uuid
import config

mydb = mysql.connector.connect(
  host=config.mysql_config["host"],
  user=config.mysql_config["user"],
  password=config.mysql_config["password"],
  database=config.mysql_config["db"]
)

def get_ambulance_data():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM med_alert_ambulance_details;")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched ambulance details")
  return myresult

def update_ambulance_state(state,vehicle_number):
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "UPDATE med_alert_ambulance_details SET state = '"+state+"' WHERE vehicle_number = '"+vehicle_number+"'"
  mycursor.execute(sql)
  mydb.commit()
  print("[DB TOUCH] updated status of "+vehicle_number+" to "+state)

def get_available_ambulance():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("select * from med_alert_ambulance_details where state='available';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched available ambulances")
  return myresult

def add_food_expense(user_id_of_updater,shashank_dish,sayak_dish,shashank_cost,sayak_cost,who_paid):  
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "insert into food_track (user_id_of_updater,shashank_dish,sayak_dish,shashank_cost,sayak_cost,who_paid) values ('"+user_id_of_updater+"','"+shashank_dish+"','"+sayak_dish+"',"+shashank_cost+","+sayak_cost+",'"+who_paid+"')"
  mycursor.execute(sql)
  mydb.commit()
  print("SQL query -------> "+sql)
  print("[DB TOUCH] Added expense to food_track table ")

