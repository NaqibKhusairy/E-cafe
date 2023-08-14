import mysql.connector
import bcrypt
import datetime

dash = "-" * 70

table1 = [
	["1", "Customer"],
	["2", "Staff"] #belum
]

table2 = [
	["1", "Order"],
	["2", "View Menu"],
	["3", "Back"]
]
Makanan = [
	[" Code", "Makanan", "Price"],
	["x", "  Telur Rabus", "0.50"],
	["x", "  Telur Mata", "1.00"],
	["x", "  Telur Dadar", "1.50"],
	["x", "  Nasi Putih", "1.50"],
	["x", "  Nasi Lemak", "2.00"],
	["x", "  Ayam Goreng", "3.00"],
	["x", "  Nasi Bujang", "4.00"],
	["x", "  Nasi Goreng Biasa", "4.50"],
	["x", "  Nasi Ayam", "5.00"],
	["x", "  Nasi Goreng Tomyam", "5.00"],
	["x", "  Nasi Goreng Kampung", "5.00"],
	["x", "  Nasi Goreng Cina", "5.00"],
	["x", "  Nasi Goreng Bujang", "5.00"],
	["x", "  Nasi Goreng Pataya", "6.00"],
	["x", "  Nasi Goreng Ayam", "7.00"],
	["x", "  Nasi Goreng Ayam Merah", "7.00"],
	["x", "  Nasi Goreng Daging Merah", "7.00"],
	["x", "  Nasi Goreng USA", "8.00"],
	["x", "  Mee Goreng", "5.00"],
	["x", "  Maggi Goreng", "5.00"],
	["x", "  Bihun Goreng", "5.00"],
	["x", "  Kuew Teow Goreng", "5.00"],
	["x", "  Maggi Kari", "5.50"],
	["x", "  Maggi Sup", "5.50"],
	["x", "  Maggi Tomyam", "5.50"],
	["x", "  Sayur Campur", "8.00"],
	["x", "  Kailan Ikan Masin", "8.00"],
	["x", "  Kangkung Goreng Belacan", "8.00"],
	["x", "  Ayam Masak Merah", "8.00"],
	["x", "  Daging Masak Merah", "8.00"],
	["x", "  Tomyam Ayam", "8.00"],
	["x", "  Tomyam Daging", "8.00"],
	["x", "  Tomyam Seafood", "9.00"],
	["x", "  Tomyam Campur", "9.40"],
	["x", "  Char Kuew Teow Udang", "8.00"],
	["x", "  Char Kuew Teow Kerang", "8.00"],
	["x", "  Char Kuew Teow Udang + Kerang", "9.50"],
	["x", "  Char Kuew Teow Special", "10.00"]
]

Minuman = [
	[" Code", "Minuman", "Panas"  , "Ais"],
	["x", "  Air Kosong", "0.20" , "0.50"],
	["x", "  Teh Panas", "1.00" , "1.20"],
	["x", "  Kopi Panas", "1.00" , "1.20"],
	["x", "  Teh Tarik", "1.50" , "1.70"],
	["x", "  Kopi O", "1.50" , "1.70"],
	["x", "  Milo Panas", "1.50" , "1.70"],
	["x", "  Teh O", "1.50" , "1.70"],
	["x", "  Kopi ", "1.50" , "1.70"],
	["x", "  Sirap Bandung", "2.50" , "2.70"],
	["x", "  Bandung Soda", "  -" , "3.00"],
	["x", "  Ais Kepal", "  -" , "3.00"],
	["x", "  ABC", "  -" , "3.00"],
	["x", "  Cendol Biasa", "  -" , "3.50"],
	["x", "  Cendol Jagung", "  -" , "3.50"],
	["x", "  Cendol Pulut", "  -" , "4.00"],
	["x", "  Jus Oren", "  -" , "3.40"],
	["x", "  Jus Tembikai", "  -" , "3.50"],
	["x", "  Jus Mangga", "  -" , "3.60"],
	["x", "  Jus Epal", "  -" , "3.70"],
	["x", "  Cendol Spesial", "  -" , "5.00"]
]
orderlist=[]

def database():
	return mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="cafe") #done

def createdatabase():
	try:
		mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			password="")

		myprojectdb = mydb.cursor()
		myprojectdb.execute("CREATE DATABASE IF NOT EXISTS cafe")

		projectdatabase = database()
		mydbse = projectdatabase.cursor()

		mydbse.execute("CREATE TABLE IF NOT EXISTS staff "
			"(username VARCHAR(200), "
			"password VARCHAR(200), "
			"PRIMARY KEY (username)) ")

		mydbse.execute("CREATE TABLE IF NOT EXISTS orders "
			"(username VARCHAR(200), "
			"detail LONGTEXT, "
			"total VARCHAR(200)) ")

		mydbse.execute("SELECT * FROM staff WHERE username=%s", ("admin",))
		sameinpt = mydbse.fetchone()

		if not sameinpt:
			passwrd = "admin"
			passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
			mydbse.execute("INSERT INTO staff"
				"(username, password)"
				"VALUES(%s, %s )",
				("admin", passwrd))
			projectdatabase.commit()

	except mysql.connector.Error as err:
		print("Error: {}".format(err)) #done

def showmenu():
	menu()
	order() #done

def find_item_details(item_code):
	for row in Makanan[1:]:
		if row[0] == item_code:
			item = row[1]
			price = float(row[2])

	for row in Minuman[1:]:
		if row[0] == item_code:

				if row[2] == "  -" :
					item = row[1]
					price = float(row[3])

				else:
					askminuman = input("You Want Panas Or Ais ? ")
					askminuman = askminuman.lower()
					if askminuman == "panas" :
						item = row[1] + "Panas"
						price = float(row[2])

					elif askminuman == "ais": 
						item = row[1]+ " Ais"
						price = float(row[3])

	return item, price #done

def order():
	orderlist = []
	totalprice = 0
	usename = input("Plese Enter Your nickname : ")
	usename = usename.upper()

	while True : 
		orderuser = input("Plese Enter Your Order : ")
		orderuser = orderuser.upper()
		print(dash)
		item_details, price = find_item_details(orderuser)

		if item_details:
			print("Order:", item_details," , RM {:.2f}".format(price))
			orderlist.append({
				'orderuser' : item_details,
				'price': price
				})
			totalprice += float(price)
		else:
			print("Invalid order")

		print(dash)
		askuser = input("Do You Want to add more order ? [Y or Any Key To Confirm] : ")
		askuser = askuser.upper()

		if askuser != "Y" :
			print(dash+"\n"+usename + " Order : ")
			for x in range(len(orderlist)):
				cusorder = orderlist[x]['orderuser']
				odercus = cusorder
				price = orderlist[x]['price']
				print(x + 1, cusorder," , RM {:.2f}".format(price))
			print("Total Price : RM {:.2f}".format(totalprice))
			
			try:
				projectdatabase = database()
				mydbse = projectdatabase.cursor()

				odercus = "\n".join(order['orderuser'] for order in orderlist)
				totalprice = "RM {:.2f}".format(totalprice)

				mydbse.execute("INSERT INTO orders"
					"(username, detail, total)"
					"VALUES(%s, %s, %s)",
					(usename, odercus, totalprice))

				projectdatabase.commit()

			except mysql.connector.Error as err:
				print("Error: {}".format(err))

			print()
			print(dash)
			print("             Receipt             ")
			print(dash)
			print("Customer: ", usename)
			print("Date: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			print(dash)
			print("{:<6} {:<19}{:<31} {:<14}".format("No.", "","  Item", "Price"))
			print(dash)
			for x in range(len(orderlist)):
				cusorder = orderlist[x]['orderuser']
				odercus = cusorder
				price = orderlist[x]['price']
				print("{:<6} {:<48} {:<5}".format(x + 1, cusorder,"  RM {:.2f}".format(price)))
			print(dash)
			print("Total Price: ", totalprice)
			print(dash)
			print("Thank you for your order!")
			main() #done

def menu() :
	x = 0
	print(dash + "\n" +
		"                       MENU                     " +
		"\n" + dash + "\n" +
		"|{:<6}|{:13}{:<35}|{:<3}{:<9}|".format(Makanan[0][0], "",Makanan[0][1], "",Makanan[0][2]) +
		"\n" + dash)

	for row in Makanan[1:] :
		x += 1
		row[0] = "F" + str(x)
		print("|{:<6}|{:<48}|  RM {:<5}  |".format(row[0], row[1], row[2]))
	print(dash +" \n")

	x = 0
	print(dash + "\n" +
		"|{:<6}|{:13}{:<23}|{:<3}{:<8}|{:<3}{:<9}|".format(Minuman[0][0], "", Minuman[0][1], "", Minuman[0][2], "", Minuman[0][3]) +
		"\n" + dash)

	for row in Minuman[1:] :
		x += 1
		row[0] = "D" + str(x)
		print("|{:<6}|{:<36}|  RM {:<4}  |  RM {:<5}  |".format(row[0], row[1], row[2], row[3]))
	print(dash +" \n") #done

def ordermenu():
	askuser = input("You want To Order ? [Y or Any Key To Exit] : ")
	askuser=askuser.upper()
	if askuser == "Y" :
		order()
	else:
		user() #done

def user():
	print(dash + "\n" +
		"                 Welcome Customer                 " +
		"\n" + dash)
	for row in table2 : 
		for col in row :
			print(col, end = "\t")
		print()
	print(dash)
	try :
		askuser = int(input("Please Choose [1 or 2 or 3] : "))
		if askuser == 1 :
			showmenu()
		elif askuser == 2 :
			menu()
			ordermenu()
		elif askuser == 3 :
			main()
		else :
			print(dash + "\n" +
				"              Invalid Choice !!!              ")
			user()
	except :
		print(dash + "\n" +
			"              Invalid Choice !!!              ")
		main()#done

def admin():#belum siap
	print("Admin Belum Siap")

def main() :
	print(dash + "\n" +
		"            Welcome To Food Ordering System                  " +
		"\n" + dash)
	for row in table1 : 
		for col in row :
			print(col, end = "\t")
		print()
	print(dash)
	try :
		askuser = int(input("Please Choose [1 or 2] : "))
		if askuser == 1 :
			user()
		elif askuser == 2 :
			admin()
		else :
			print(dash + "\n" +
			  "              Invalid Choice !!!              ")
			main()
	except :
		print(dash + "\n" +
			  "              Invalid Choice !!!              ")
		main()#done

while True :
	createdatabase()
	main()