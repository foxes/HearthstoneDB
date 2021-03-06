DROP TABLE Player CASCADE CONSTRAINTS;
DROP TABLE Regions CASCADE CONSTRAINTS;
DROP TABLE Deck CASCADE CONSTRAINTS;
DROP TABLE Card CASCADE CONSTRAINTS;
DROP TABLE DeckContains CASCADE CONSTRAINTS;
DROP TABLE Mechanics CASCADE CONSTRAINTS;
DROP TABLE Class CASCADE CONSTRAINTS;
DROP TABLE HeroPower CASCADE CONSTRAINTS;
DROP TABLE Hero CASCADE CONSTRAINTS;

CREATE TABLE Player(
	bnetID NVARCHAR2(17) PRIMARY KEY,
	creationDate DATE NOT NULL
);

CREATE TABLE Regions(
	bnetID NVARCHAR2(17),
	region NVARCHAR2(7),
	PRIMARY KEY(bnetID, region)
);

CREATE TABLE Deck(
	deckName NVARCHAR2(20),
	bnetID NVARCHAR2(17),
	region NVARCHAR2(7),
	creationDate DATE,
	class NVARCHAR2(7),
	PRIMARY KEY(deckName, bnetID, region)
);

CREATE TABLE Card(
	cardID NVARCHAR2(12) PRIMARY KEY,
	cardName NVARCHAR2(50) NOT NULL,
	type NVARCHAR2(6) NOT NULL,
	manaCost INTEGER NOT NULL,
	attack INTEGER,
	health INTEGER,
	race NVARCHAR2(10),
	durability INTEGER,
	cardText NVARCHAR2(500),
	rarity NVARCHAR2(9) NOT NULL,
	isLegendary INTEGER NOT NULL,
	class NVARCHAR2(7)
);

CREATE TABLE DeckContains(
	deckName NVARCHAR2(20),
	bnetID NVARCHAR2(17),
	region NVARCHAR2(7),
	cardID NVARCHAR2(12),
	copies INTEGER NOT NULL,
	PRIMARY KEY(deckName, bnetID, region, cardID)
);

CREATE TABLE Mechanics(
	cardID NVARCHAR2(12),
	mechanic NVARCHAR2(12),
	PRIMARY KEY(cardID, mechanic)
);

CREATE TABLE Class(
	className NVARCHAR2(7) PRIMARY KEY,
	classDescription NVARCHAR2(1000) NOT NULL,
	hpID INTEGER NOT NULL
);

CREATE TABLE HeroPower(
	hpID INTEGER PRIMARY KEY,
	hpName NVARCHAR2(12) NOT NULL,
	description NVARCHAR2(100) NOT NULL
);

CREATE TABLE Hero(
	heroName NVARCHAR2(12) PRIMARY KEY,
	description NVARCHAR2(100) NOT NULL,
	className NVARCHAR2(7) NOT NULL
);