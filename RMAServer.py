import mysql.connector
import datetime
import socket
import sys
import threading
from RMAServerFunctions import *
from mysql.connector import errorcode

class RMAServer:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		
	def listen(self):
		self.sock.listen(5)
		
		# set up DB credentials
		dbconfig = {
                "database": "RMA",
                "user": "RMA",
                "password": "applesauce",
                "host": "127.0.0.1"
		}
		
		# connect to the database
		try:
			cnx = mysql.connector.connect(**dbconfig)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
		else:
			print("Server ready")
			sys.stdout.flush()
			while True:
				client, address = self.sock.accept()
				
				if not cnx.is_connected():
					try:
						cnx = mysql.connector.connect(**dbconfig)
					except mysql.connector.Error as err:
						if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
							print("Something is wrong with your user name or password")
							sys.stdout.flush()
						elif err.errno == errorcode.ER_BAD_DB_ERROR:
							print("Database does not exist")
							sys.stdout.flush()
						else:
							print(err)
							sys.stdout.flush()
							
				#self.listenToClient(client, address, cnx)
				threading.Thread(target = self.listenToClient,args = (client,address,cnx)).start()
		sys.stdout.flush()
		cnx.close()
	# end of function
		
	def listenToClient(self, connection, address, cnx):
		available_options = make_available_query_list()
		input_required = InputQueries()

		user_option = get_client_input(connection)
		
		if user_option not in available_options:
			print(datetime.datetime.now())
			print user_option + " is not a valid query. Please copy the query name exactly"
			print "\r\n"
			sys.stdout.flush()
		else:
			insert_data = []
			if user_option in input_required:
				if (user_option == "GenerateReport" or
					user_option == "GenerateOpenReport" or
					user_option == "GenerateReportTSC" or
					user_option == "GenerateReportSupplier" or
					user_option == "FilterEntries" or
					user_option == "DeleteEntry"):
					data = get_client_input(connection)
					insert_data.append(data)
					
				elif (user_option == "GenerateReportIndividualSupplier"):
					for i in range(2):
						data = get_client_input(connection)
						insert_data.append(data)
					
				elif (user_option == "InsertNewEntry"):
					for i in range(22):
						data = get_client_input(connection)
						insert_data.append(data)
					#drain_client_input(connection)
						
				elif (user_option == "EditEntry"):
					for i in range(23):
						data = get_client_input(connection)
						insert_data.append(data)
					#drain_client_input(connection)
					
			drain_client_input(connection)
		
			cursor = cnx.cursor()
			
			HandleQuery(user_option, cursor, connection, cnx, insert_data)
				
			cursor.close()
		#end of processing
			
		connection.close()
	# end of function
	
# handle query execution
def HandleQuery(option, sqlcursor, client_connection, sql_connection, insert_data=[]):
	#execute query
	if not insert_data:
		sqlcursor.execute(make_query(option+'.sql'))
	else:
		try:
			if (option == "InsertNewEntry"):
				if (len(insert_data[0]) <= 50 and
					len(insert_data[1]) <= 20 and
					len(insert_data[2]) <= 50 and
					len(insert_data[3]) == 10 and
					len(insert_data[4]) <= 20 and
					len(insert_data[5]) <= 300 and
					len(insert_data[6]) <= 75 and
					len(insert_data[7]) <= 10 and
					str.isdigit(insert_data[8]) and
					len(insert_data[9]) <= 50 and
					len(insert_data[10]) == 10 and
					len(insert_data[11]) == 10 and
					str.isdigit(insert_data[12]) and
					len(insert_data[13]) <= 50 and
					len(insert_data[14]) <= 50 and
					str.isdigit(insert_data[15]) and
					len(insert_data[16]) <= 75 and
					len(insert_data[17]) <= 300 and
					len(insert_data[18]) <= 20 and
					len(insert_data[19]) <= 50 and
					len(insert_data[20]) <= 50 and
					str.isdigit(insert_data[21])):
					user_option_data = {
						'supplier': insert_data[0],
						'so': insert_data[1],
						'client': insert_data[2],
						'datereceived': insert_data[3],
						'rts': insert_data[4],
						'description': insert_data[5],
						'serial': insert_data[6],
						'datereported': insert_data[7],
						'quantityreceived': insert_data[8],
						'problem': insert_data[9],
						'datepullout': insert_data[10],
						'datereturned': insert_data[11],
						'nonworkingdays': insert_data[12],
						'pos': insert_data[13],
						'rtc': insert_data[14],
						'quantityreturned': insert_data[15],
						'newserial': insert_data[16],
						'remarks': insert_data[17],
						'status': insert_data[18],
						'supplierpos': insert_data[19],
						'supplierreturned': insert_data[20],
						'trace': insert_data[21]
					}
					sqlcursor.execute(make_query(option+'.sql'), user_option_data)
					sql_connection.commit()
					client_connection.sendall("Successfully completed the operation!")
				else:
					client_connection.sendall("Something was wrong with the information entered")
					print(datetime.datetime.now())
					print("InsertNewEntry: Something's wrong with the data sent")
					print(insert_data)
					print("\n")
				
			elif (option == "EditEntry"):
				if (str.isdigit(insert_data[0]) and
					len(insert_data[1]) <= 50 and
					len(insert_data[2]) <= 20 and
					len(insert_data[3]) <= 50 and
					len(insert_data[4]) == 10 and
					len(insert_data[5]) <= 20 and
					len(insert_data[6]) <= 300 and
					len(insert_data[7]) <= 75 and
					len(insert_data[8]) <= 10 and
					str.isdigit(insert_data[9]) and
					len(insert_data[10]) <= 50 and
					len(insert_data[11]) == 10 and
					len(insert_data[12]) == 10 and
					str.isdigit(insert_data[13]) and
					len(insert_data[14]) <= 50 and
					len(insert_data[15]) <= 50 and
					str.isdigit(insert_data[16]) and
					len(insert_data[17]) <= 75 and
					len(insert_data[18]) <= 300 and
					len(insert_data[19]) <= 20 and
					len(insert_data[20]) <= 50 and
					len(insert_data[21]) <= 50 and
					str.isdigit(insert_data[22])):
					user_option_data = {
						'id': insert_data[0],
						'supplier': insert_data[1],
						'so': insert_data[2],
						'client': insert_data[3],
						'datereceived': insert_data[4],
						'rts': insert_data[5],
						'description': insert_data[6],
						'serial': insert_data[7],
						'datereported': insert_data[8],
						'quantityreceived': insert_data[9],
						'problem': insert_data[10],
						'datepullout': insert_data[11],
						'datereturned': insert_data[12],
						'nonworkingdays': insert_data[13],
						'pos': insert_data[14],
						'rtc': insert_data[15],
						'quantityreturned': insert_data[16],
						'newserial': insert_data[17],
						'remarks': insert_data[18],
						'status': insert_data[19],
						'supplierpos': insert_data[20],
						'supplierreturned': insert_data[21],
						'trace': insert_data[22]
					}
					sqlcursor.execute(make_query(option+'.sql'), user_option_data)
					sql_connection.commit()
					client_connection.sendall("Successfully completed the operation!")
				else:
					client_connection.sendall("Something was wrong with the information entered")
					print(datetime.datetime.now())
					print("EditEntry: Something's wrong with the data sent")
					print(insert_data)
					print("\n")
				
			elif (option == "DeleteEntry"):
				if (str.isdigit(insert_data[0])):
					user_option_data = {'entryid': insert_data[0]}
					
					sqlcursor.execute(make_query(option+'.sql'), user_option_data)
					sql_connection.commit()
					client_connection.sendall("Successfully completed the operation!")
				else:
					client_connection.sendall("EntryID sent wasn't a number")
					print(datetime.datetime.now())
					print("DeleteEntry: Something's wrong with the data sent")
					print(insert_data)
					print("\n")
				
			elif (option == "GenerateReport" or
					option == "GenerateOpenReport" or
					option == "GenerateReportSupplier" or
					option == "GenerateReportTSC"):
				if len(insert_data[0]) == 4:
					user_option_data = {
						'start': ("{}-01-01").format(insert_data[0]),
						'end': ("{}-12-31").format(insert_data[0])
					}
					sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				else:
					client_connection.sendall("Number sent didn't correspond to a year")
					print(datetime.datetime.now())
					print("Reports: Something's wrong with the data sent")
					print(insert_data)
					print("\n")
				
			elif (option == "GenerateReportIndividualSupplier"):
				if (len(insert_data[0]) == 4 and
					len(insert_data[1]) <= 50):
					user_option_data = {
						'start': ("{}-01-01").format(insert_data[0]),
						'end': ("{}-12-31").format(insert_data[0]),
						'supplier': insert_data[1]
					}
					sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				else:
					client_connection.sendall("Number sent didn't correspond to a year")
					print(datetime.datetime.now())
					print("GenerateReportIndividualSupplier: Something's wrong with the data sent")
					print(insert_data)
					print("\n")
				
			elif (option == "FilterEntries"):
				user_option_data = {'rts': ("%{}%").format(insert_data[0])}
				sqlcursor.execute(make_query(option+'.sql'), user_option_data)
				
		except mysql.connector.Error as err:
			sql_connection.rollback()
		
			print(datetime.datetime.now())
			print(err)
			print "\r\n"
			FlushCursor(sqlcursor)
			sys.stdout.flush()
	
		except Exception as err2:
			sql_connection.rollback()
			
			print(datetime.datetime.now())
			print(err2)
			print "\r\n"
			FlushCursor(sqlcursor)
			sys.stdout.flush()
		
	#send results of view queries
	if (option == "ViewEntries" or
		option == "ViewOpenEntries" or
		option == "GenerateReport" or
		option == "GenerateOpenReport" or
		option == "GenerateReportTSC" or
		option == "GenerateReportIndividualSupplier" or
		option == "FilterEntries"):
		ViewEntries(sqlcursor, client_connection)
	elif (option == "GenerateReportSupplier"):
		GenerateReportSupplier(sqlcursor, client_connection)
	elif (option == "ViewSuppliers"):
		ViewSuppliers(sqlcursor, client_connection)
	else:
		FlushCursor(sqlcursor)
		sys.stdout.flush()
#end of function