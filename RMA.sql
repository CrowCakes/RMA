DROP DATABASE IF EXISTS RMA;

CREATE DATABASE RMA;
USE RMA;

CREATE TABLE Entry (
	EntryID int AUTO_INCREMENT PRIMARY KEY,
	Supplier varchar(50),
	SO varchar(20),
	Client varchar(50),
	DateReceived date,
	RTS varchar(20),
	Description varchar(300),
	Serial varchar(75),
	DateReported date,
	QuantityReceived int,
	Problem varchar(50),
	DatePullOut date,
	DateReturned date,
	NonWorkingDays int,
	POS varchar(50),
	RTC varchar(50),
	QuantityReturned int,
	NewSerial varchar(75),
	Remarks varchar(300),
	Status varchar(20)
);

/*
CREATE TABLE EntryText {
	EntryID int,
	Description varchar(300),
	Remarks varchar(300)
	
	FOREIGN KEY (EntryID) REFERENCES Entry (EntryID)
	ON UPDATE CASCADE 
	ON DELETE CASCADE;
}
*/

/*
TURN AROUND DAYS = DateReturned - DatePullOut - NonWorkingDays
QUANTITY REMAINING = QuantityReceived - QuantityReturned
AGING = DateReceived - Today (?)
*/