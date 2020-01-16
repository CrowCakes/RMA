INSERT INTO Entry(Supplier, SO, Client, DateReceived, RTS, Description, Serial, 
	DateReported, QuantityReceived, Problem, ReportedBy, TestedBy,
	DatePullOut, DateReturned, NonWorkingDays,
	POS, RTC, QuantityReturned,
	NewSerial, Remarks, Status, 
	SupplierPOS, SupplierReturned, Trace)
VALUES (%(supplier)s, %(so)s, %(client)s, %(datereceived)s, %(rts)s, 
%(description)s, %(serial)s, %(datereported)s, %(quantityreceived)s, %(problem)s, 
%(datepullout)s, %(datereturned)s, %(nonworkingdays)s, %(pos)s, %(rtc)s, 
%(quantityreturned)s, %(newserial)s, %(remarks)s, %(status)s, 
%(supplierpos)s, %(supplierreturned)s, %(trace)s)