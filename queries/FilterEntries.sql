SELECT EntryID, Supplier, SO, Client, DateReceived, RTS, Description, Serial, 
	DateReported, QuantityReceived, Problem, 
	DatePullOut, DateReturned, NonWorkingDays, 
	DATEDIFF(DateReturned, DatePullOut) - NonWorkingDays AS Turnaround,
	POS, RTC, QuantityReturned, 
	QuantityReceived - QuantityReturned AS QuantityRemaining,
	NewSerial, Remarks, Status,
	DATEDIFF(DateReceived, CURDATE()) AS Aging,
	Trace
FROM Entry 
WHERE RTS LIKE %(rts)s
ORDER BY EntryID ASC