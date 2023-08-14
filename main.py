import mysql.connector
import bcrypt
import random
import datetime
import string

dash = "-" * 70

table1 = [
	["1", "Customer"],
	["2", "Staff"]
]

table2 = [
	["1", "Order"],
	["2", "View Menu"],
	["3", "Back"]
]

table3 = [
	["1","Add Staff account"],
	["2","Delete Staff account"],
	["3","View Order"],
	["4","Customer Payment"],
	["5","Change Password"],
	["6","Log Out"],
]

table4 = [
	["1","View Order"],
	["2","Customer Payment"],
	["3","Change Password"],
	["4","Log Out"],
]

Makanan = [
	[" Code", "Makanan", "Price"],
	["x", "Telur Rabus", "0.50"],
	["x", "Telur Mata", "1.00"],
	["x", "Telur Dadar", "1.50"],
	["x", "Nasi Putih", "1.50"],
	["x", "Nasi Lemak", "2.00"],
	["x", "Ayam Goreng", "3.00"],
	["x", "Nasi Bujang", "4.00"],
	["x", "Nasi Goreng Biasa", "4.50"],
	["x", "Nasi Ayam", "5.00"],
	["x", "Nasi Goreng Tomyam", "5.00"],
	["x", "Nasi Goreng Kampung", "5.00"],
	["x", "Nasi Goreng Cina", "5.00"],
	["x", "Nasi Goreng Bujang", "5.00"],
	["x", "Nasi Goreng Pataya", "6.00"],
	["x", "Nasi Goreng Ayam", "7.00"],
	["x", "Nasi Goreng Ayam Merah", "7.00"],
	["x", "Nasi Goreng Daging Merah", "7.00"],
	["x", "Nasi Goreng USA", "8.00"],
	["x", "Mee Goreng", "5.00"],
	["x", "Maggi Goreng", "5.00"],
	["x", "Bihun Goreng", "5.00"],
	["x", "Kuew Teow Goreng", "5.00"],
	["x", "Maggi Kari", "5.50"],
	["x", "Maggi Sup", "5.50"],
	["x", "Maggi Tomyam", "5.50"],
	["x", "Sayur Campur", "8.00"],
	["x", "Kailan Ikan Masin", "8.00"],
	["x", "Kangkung Goreng Belacan", "8.00"],
	["x", "Ayam Masak Merah", "8.00"],
	["x", "Daging Masak Merah", "8.00"],
	["x", "Tomyam Ayam", "8.00"],
	["x", "Tomyam Daging", "8.00"],
	["x", "Tomyam Seafood", "9.00"],
	["x", "Tomyam Campur", "9.40"],
	["x", "Char Kuew Teow Udang", "8.00"],
	["x", "Char Kuew Teow Kerang", "8.00"],
	["x", "Char Kuew Teow Udang + Kerang", "9.50"],
	["x", "Char Kuew Teow Special", "10.00"]
]

Minuman = [
	[" Code", "Minuman", "Panas"  , "Ais"],
	["x", "Air Kosong", "0.20" , "0.50"],
	["x", "Teh Panas", "1.00" , "1.20"],
	["x", "Kopi Panas", "1.00" , "1.20"],
	["x", "Teh Tarik", "1.50" , "1.70"],
	["x", "Kopi O", "1.50" , "1.70"],
	["x", "Milo Panas", "1.50" , "1.70"],
	["x", "Teh O", "1.50" , "1.70"],
	["x", "Kopi ", "1.50" , "1.70"],
	["x", "Sirap Bandung", "2.50" , "2.70"],
	["x", "Bandung Soda", "  -" , "3.00"],
	["x", "Ais Kepal", "  -" , "3.00"],
	["x", "ABC", "  -" , "3.00"],
	["x", "Cendol Biasa", "  -" , "3.50"],
	["x", "Cendol Jagung", "  -" , "3.50"],
	["x", "Cendol Pulut", "  -" , "4.00"],
	["x", "Jus Oren", "  -" , "3.40"],
	["x", "Jus Tembikai", "  -" , "3.50"],
	["x", "Jus Mangga", "  -" , "3.60"],
	["x", "Jus Epal", "  -" , "3.70"],
	["x", "Cendol Spesial", "  -" , "5.00"]
]

orderlist=[]

def database():
	return mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="cafe")

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
			"ordernum VARCHAR(200),"
			"detail LONGTEXT, "
			"total VARCHAR(200), "
			"payment VARCHAR(200)) ")

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
		print("Error: {}".format(err))

def showmenu():
	menu()
	order()

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

	return item, price

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
			characters = string.ascii_lowercase + string.digits
			ordernumber = ''.join(random.choice(characters) for _ in range(12))
			
			try:
				projectdatabase = database()
				mydbse = projectdatabase.cursor()

				odercus = "\n".join(order['orderuser'] for order in orderlist)
				totalprice = "RM {:.2f}".format(totalprice)

				mydbse.execute("INSERT INTO orders"
					"(username, ordernum, detail, total, payment)"
					"VALUES(%s, %s, %s, %s, %s)",
					(usename, ordernumber, odercus, totalprice, "unpaid"))

				projectdatabase.commit()

			except mysql.connector.Error as err:
				print("Error: {}".format(err))

			print()
			print(dash)
			print("{:<25} {:<45}".format("","Your Order"))
			print(dash)
			print("Customer     : ", usename)
			print("Date         : ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			print("Order Number : ",ordernumber)
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
			main()

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
		print("|{:<6}|  {:<48}|  RM {:<5}  |".format(row[0], row[1], row[2]))
	print(dash +" \n")

	x = 0
	print(dash + "\n" +
		"|{:<6}|{:13}{:<23}|{:<3}{:<8}|{:<3}{:<9}|".format(Minuman[0][0], "", Minuman[0][1], "", Minuman[0][2], "", Minuman[0][3]) +
		"\n" + dash)

	for row in Minuman[1:] :
		x += 1
		row[0] = "D" + str(x)
		print("|{:<6}|  {:<36}|  RM {:<4}  |  RM {:<5}  |".format(row[0], row[1], row[2], row[3]))
	print(dash +" \n")

def ordermenu():
	askuser = input("You want To Order ? [Y or Any Key To Exit] : ")
	askuser=askuser.upper()
	if askuser == "Y" :
		order()
	else:
		user()

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
		main()

def addstaff(username):
	print(dash)
	print("{:<14}{:<61}".format("","Add New Staff "))
	print(dash)
	try:
		username2 = input("Please enter Username: ")
		projectdatabase = database()
		mydbse = projectdatabase.cursor()
		mydbse.execute("SELECT * FROM staff WHERE username = %s",(username2,))
		sameid = mydbse.fetchone()

		if sameid :
			print("The Account is Already Registered.")
			askuser = input("Do you want To Register Other Account ? [ Y to continue or any key to back] : ")
			askuser = askuser.upper()
			if askuser == "Y" :
				addstaff(username)
			else :
				staf(username)
		else :
			passwrd1 = input("Please enter Password: ")
			passwrd = bcrypt.hashpw(passwrd1.encode('utf-8'), bcrypt.gensalt())
			mydbse.execute("INSERT INTO staff"
				"(username, password)"
				"VALUES(%s, %s )",
				(username2, passwrd))
			projectdatabase.commit()

			passwrd1 = "*" * len(passwrd1)

			print("Registeration Complete ....")
			print(dash)
			print("Username : "+username2+
				"\nPassword : "+passwrd1)
			staf(username)

	except mysql.connector.Error as err:
		print("Failed to Insert data: {}".format(err))
		staf(username)

def deletestaff(username):
	print(dash)
	print("{:<14}{:<61}".format("","Delete Staff "))
	print(dash)
	try:
		username2 = input("Please enter Username: ")
		projectdatabase = database()
		mydbse = projectdatabase.cursor()
		mydbse.execute("SELECT * FROM staff WHERE username = %s",(username2,))
		staffrecord = mydbse.fetchone()

		if staffrecord :
			print(dash)
			print("Deleting " + username2 + " account...")
			print(dash)
			askuser = input(f"Do you want to Delete the {username2} account? [Y or N]: ").upper()
			if askuser == "Y" :
				mydbse.execute("DELETE FROM staff WHERE username = %s",(username2))
				projectdatabase.commit()
				print("Deleted " + username2 + " account successfully")
				staf(username)
			elif askuser == "N" :
				print("Deleting Canceled")
				staf(username)
			else :
				print("You Need to enter either Y or N !!!!")
				staf(username)
		else :
			print("User not Found")
			staf(username)

	except mysql.connector.Error as err:
		print("Failed to Deleted User:", str(e))
		staf(username)

def vieworder(username):
	print(dash)
	print("{:<14}{:<61}".format("","Customer Order"))
	print(dash)
	try:
		projectdatabase = database()
		mydbse = projectdatabase.cursor()
		mydbse.execute("SELECT * FROM orders WHERE payment = %s", ("unpaid",))
		listorder = mydbse.fetchall()

		if listorder :
			for senaraiorder  in listorder :
				username2 = senaraiorder[0]
				ordernum = senaraiorder[1]
				detail = senaraiorder[2]
				total = senaraiorder[3]

				print("{:<14}: {:<61}".format("Username",username2))
				print("{:<14}: {:<61}".format("Order Number",ordernum))
				print("{:<14}: {:<61}".format("Order",""))
				print(detail)
				print("{:<14}: {:<61}".format("Total Price",total))
				print(dash)
			staf(username)
		else :
			print("No Order")
			staf(username)

	except mysql.connector.Error as err:
		print("Failed to Find Order :{}".format(err))
		staf(username)

def cuspay(username):
	print(dash)
	print("{:<14}{:<61}".format("","Customer Payment"))
	print(dash)
	try:
		projectdatabase = database()
		mydbse = projectdatabase.cursor()
		ordernum = input("Insert Order Number : ").lower()

		mydbse.execute("SELECT * FROM orders WHERE ordernum = %s", (ordernum,))
		ordercus = mydbse.fetchone()

		if ordercus and ordercus[4].lower() == 'unpaid' :
			mydbse.execute("SELECT * FROM orders WHERE ordernum = %s", (ordernum,))
			listorder = mydbse.fetchall()

			if listorder :
				for senaraiorder in listorder :
					username2 = senaraiorder[0]
					ordernum = senaraiorder[1]
					detail = senaraiorder[2]
					total = senaraiorder[3]

					print("{:<14}: {:<61}".format("Username",username2))
					print("{:<14}: {:<61}".format("Order Number",ordernum))
					print("{:<14}: {:<61}".format("Order",""))
					print(detail)
					print("{:<14}: {:<61}".format("Total Price",total))
					print(dash)
					askcasher = input(f"Do {username2} want to Pay? [Y or N]: ").upper()

					if askcasher == "Y" :
						mydbse.execute("UPDATE orders SET payment = %s WHERE username = %s",("paid",username2))
						projectdatabase.commit()

						print()
						print(dash)
						print("{:<25} {:<45}".format("","Payment Detail"))
						print(dash)
						print("Customer     : ", username2)
						print("Date         : ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
						print("Order Number : ", ordernum)
						print(dash)
						print("Order : ")
						print(detail)
						print(dash)
						print("Total Price: ", total)
						print(dash)
						print("Paid")
						print(dash)
						print("Thank you "+username2+" For Coming..")
						staf(username)
					elif askuser == "N" :
						staf(username)
					else :
						print("You Need to enter either Y or N !!!!")
						staf(username)

			else:
				print("No Order")
				staf(username)
		else :
			print("Your Have Paid")
			staf(username)

	except mysql.connector.Error as err:
		print("Failed to Find Order :{}".format(err))
		staf(username)

def changepass(username):
	print(dash)
	print("{:<25}{:<50}".format("",username+" Change Password"))
	print(dash)
	try:
		projectdatabase = database()
		mydbse = projectdatabase.cursor()
		passwrd = input("Please enter your New Password: ")
		cpasswrd = input("Please confirm your New Password: ")

		if passwrd == cpasswrd :
			passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
			mydbse.execute("UPDATE staff SET password=%s WHERE username=%s",(passwrd, username))
			projectdatabase.commit()

			cpasswrd = "*" * len(cpasswrd)

			print("Change Password Complete ....")
			print(dash)
			print("Username : "+username+
				"\nPassword : "+cpasswrd)
			staf(username)
		else :
			print("Please Make Sure Your Password and confirm passwrd is same. please register again")
			changepass(username)

	except mysql.connector.Error as err:
		print("Failed to update data: {}".format(err))
		staf(username)

def staf(username):
	print(dash)
	print("{:<14}{:<61}".format("","Welcome Back " +username))
	print(dash)
	if username.lower() == "admin" :
		for row in table3 :
			for col in row :
				print(col, end = "\t")
			print()
		print(dash)
		try :
			askuser = int(input("Please Choose [1 or 2 or 3 or 4 or 5 or 6] : "))
			if askuser == 1 :
				addstaff(username)
			elif askuser == 2 :
				deletestaff(username)
			elif askuser == 3 :
				vieworder(username)
			elif askuser == 4 :
				cuspay(username)
			elif askuser == 5 :
				changepass(username)
			elif askuser == 6 :
				main()
			else :
				print(dash + "\n" +
				  "              Invalid Choice !!!              ")
				staf(username)
		except :
			print(dash + "\n" +
				  "              Invalid Choice !!!              ")
			staf(username)
	else:
		for row in table4 :
			for col in row :
				print(col, end = "\t")
			print()
		print(dash)
		try :
			askuser = int(input("Please Choose [1 or 2 or 3 or 4] : "))
			if askuser == 1 :
				vieworder(username)
			elif askuser == 2 :
				cuspay(username)
			elif askuser == 3 :
				changepass(username)
			elif askuser == 4 :
				main()
			else :
				print(dash + "\n" +
				  "              Invalid Choice !!!              ")
				staf(username)
		except :
			print(dash + "\n" +
				  "              Invalid Choice !!!              ")
			staf(username)

def admin(count):
	print(dash)
	print("{:<23}{:<47}".format("","Staff Log In"))
	print(dash)
	username = input("Please enter your Username: ")
	try:
		projectdatabase = database()
		mydbse = projectdatabase.cursor()
		mydbse.execute("SELECT * FROM staff WHERE username = %s",(username,))
		userdata = mydbse.fetchone()

		if userdata :
			passwrd = input("Please enter your Password: ")
			if bcrypt.checkpw(passwrd.encode('utf-8'), userdata[1].encode('utf-8')):
				print("Welcome back," + username + ".")
				staf(username)
			else:
				if count == 1 :
					print("Your password is wrong. Sorry You have reached the Maximum Limit which is 3 times. Please Try Again")
					admin(3)
				else:
					count -=1
					print("Your password is wrong. Please try again. You only have " + str(count) + " chances left")
					admin(count)
		else:
			print("Your staff account is not in the database, are you serious you are staff?")
			askuser = input("Do you want To Login Y for yes or any key to quit ? [ Y or any key ] : ")
			askuser = askuser.upper()
			if askuser == "Y":
				admin(count)
			else:
				main()

	except mysql.connector.Error as err:
		print("Failed to log in: {}".format(err))

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
			count=3
			admin(count)
		else :
			print(dash + "\n" +
			  "              Invalid Choice !!!              ")
			main()
	except :
		print(dash + "\n" +
			  "              Invalid Choice !!!              ")
		main()

while True :
	createdatabase()
	main()
