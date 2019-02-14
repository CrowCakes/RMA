SELECT EntryID, Supplier, SO, Client, DateReceived, RTS, Description, Serial, 
	DateReported, QuantityReceived, Problem, 
	DatePullOut, DateReturned, NonWorkingDays, 
	DATEDIFF(DateReturned, DatePullOut) - NonWorkingDays AS Turnaround,
	POS, RTC, QuantityReturned, 
	QuantityReceived - QuantityReturned AS QuantityRemaining,
	NewSerial, Remarks, Status,
	DATEDIFF(DateReceived, CURDATE()) AS Aging
FROM Entry 
ORDER BY EntryID ASC