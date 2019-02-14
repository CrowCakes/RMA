UPDATE Entry
SET Supplier = %(supplier)s, 
SO = %(so)s, 
Client = %(client)s, 
DateReceived = %(datereceived)s, 
RTS = %(rts)s, 
Description = %(description)s, 
Serial = %(serial)s, 
DateReported = %(datereported)s, 
QuantityReceived = %(quantityreceived)s, 
Problem = %(problem)s, 
DatePullOut = %(datepullout)s, 
DateReturned = %(datereturned)s, 
NonWorkingDays = %(nonworkingdays)s,
POS = %(pos)s, 
RTC = %(rtc)s, 
QuantityReturned = %(quantityreturned)s,
NewSerial = %(newserial)s, 
Remarks = %(remarks)s, 
Status = %(status)s
WHERE EntryID = %(id)s