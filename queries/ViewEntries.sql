SELECT EntryID, Supplier, SO, Client, DateReceived, RTS, Description, Serial, 
	DateReported, QuantityReceived, Problem, ReportedBy, TestedBy,
	DatePullOut, DateReturned, NonWorkingDays, 
	DATEDIFF(DateReturned, DatePullOut) - NonWorkingDays AS Turnaround,
	POS, RTC, QuantityReturned, 
	QuantityReceived - QuantityReturned AS QuantityRemaining,
	NewSerial, Remarks, Status,
	DATEDIFF(CURDATE(), DateReceived) AS Aging,
	SupplierPOS, SupplierReturned,
	Trace
FROM Entry
WHERE Status = "Closed" or (Status = "Open" and DATEDIFF(CURDATE(), DateReceived) <= 7)
ORDER BY EntryID DESC