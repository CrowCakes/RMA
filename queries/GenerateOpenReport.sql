SELECT EntryID, Supplier, SO, Client, DateReceived, RTS, Description, Serial, 
	DateReported, QuantityReceived, Problem, ReportedBy, TestedBy,
	DatePullOut, DateReturned, NonWorkingDays, 
	DATEDIFF(DateReturned, DatePullOut) - NonWorkingDays AS Turnaround,
	POS, RTC, QuantityReturned, 
	QuantityReceived - QuantityReturned AS QuantityRemaining,
	NewSerial, Remarks, Status,
	DATEDIFF(DateReceived, CURDATE()) AS Aging,
	SupplierPOS, SupplierReturned,
	Trace
FROM Entry
WHERE DateReported >= %(start)s AND DateReported <= %(end)s AND Status = "Open"
ORDER BY DateReported ASC