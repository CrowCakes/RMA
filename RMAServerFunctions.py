import mysql.connector
import os
import socket
import sys
from datetime import date

def InputQueries():
	input_queries = ["InsertNewEntry",
					"EditEntry",
					"GenerateReport",
					"GenerateOpenReport",
					"GenerateReportTSC",
					"GenerateReportSupplier",
					"GenerateReportIndividualSupplier",
					"FilterEntries",
					"DeleteEntry"]
	return input_queries

# Construct a query from a multiline sql file in queries subdirectory
def make_query(filename):
	query = ""
	query_dir = os.path.dirname(__file__)
	rel_path = os.path.join("queries", filename)
	abs_path = os.path.join(query_dir, rel_path)
	for line in open(abs_path):
		query += line
	return query
# end of function
  
# Listen for and construct user client input
def get_client_input(socket_connection):
	data = ""
	#print "Waiting for input from user client"
	while True:
		stream_data = socket_connection.recv(1)
		#reached the end of the form
		if stream_data == '\f':
			break
		else:
			data += stream_data
  #print "Received data:", data
	return data
# end of function

# Listen for and construct user client input
def drain_client_input(socket_connection):
	data = ""
	#print "Waiting for input from user client"
	while True:
		stream_data = socket_connection.recv(1)
		#reached the end of the form
		if stream_data == '\n':
			break
		else:
			data += stream_data
  #print "Received data:", data
	return data
# end of function

# fetch the list of valid queries that the server should handle
def make_available_query_list():
	available_options = []
	for line in open('querylist.txt'):
		fline = line.rstrip()
		available_options.append(fline)
	return available_options
	
def ViewEntries(sqlcursor, connection):
	for (EntryID, Supplier, SO, Client, DateReceived, RTS, Description, Serial, 
	DateReported, QuantityReceived, Problem, 
	DatePullOut, DateReturned, NonWorkingDays, Turnaround,
	POS, RTC, QuantityReturned, QuantityRemaining,
	NewSerial, Remarks, Status, Aging, Trace) in sqlcursor:
		#print("{}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}\t").format(EntryID, Supplier, SO, Client, DateReceived, RTS, Description, Serial, DateReported, QuantityReceived, Problem, DatePullOut, DateReturned, NonWorkingDays, Turnaround, POS, RTC, QuantityReturned, QuantityRemaining, NewSerial, Remarks, Status, Aging)
		#sys.stdout.flush()
		connection.sendall(("{}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::, {}::\n").format(EntryID, Supplier, SO, Client, DateReceived, RTS, Description, Serial, DateReported, QuantityReceived, Problem, DatePullOut, DateReturned, NonWorkingDays, Turnaround, POS, RTC, QuantityReturned, QuantityRemaining, NewSerial, Remarks, Status, Aging, Trace))
		
def GenerateReportSupplier(sqlcursor, connection):
	for (Supplier, Total, Percentage) in sqlcursor:
		connection.sendall(("{}::, {}::, {}::\n").format(Supplier, Total, Percentage))

def ViewSuppliers(sqlcursor, connection):
	for (Suppliers, foo) in sqlcursor:
		connection.sendall(("{}::\n").format(Suppliers))

def FlushCursor(sqlcursor):
	print("Flushing cursor")
	for line in sqlcursor:
		print(line)
	print("\r\n")