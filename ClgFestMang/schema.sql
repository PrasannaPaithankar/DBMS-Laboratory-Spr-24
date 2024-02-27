CREATE TABLE Event (
    EID INTEGER PRIMARY KEY,
    EName VARCHAR(255) NOT NULL,
    Date DATE NOT NULL,
    Desc VARCHAR(255),
    Winners VARCHAR(255)
);

CREATE TABLE Participant (
    PID INTEGER PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    accomodation VARCHAR(255) NOT NULL,
    vegnonveg BOOLEAN NOT NULL,
    CName VARCHAR(255)
);

CREATE TABLE Role (
    RID INTEGER PRIMARY KEY,
    Rname VARCHAR(255) NOT NULL,
    Description VARCHAR(255) NOT NULL
);

CREATE TABLE Student (
    Roll INTEGER PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Dept VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    RID INTEGER,
    FOREIGN KEY (RID) REFERENCES Role(RID)
);

CREATE TABLE Student_Event (
    Roll INTEGER,
    EID INTEGER,
    Position INTEGER DEFAULT 0,
    PRIMARY KEY (Roll, EID),
    FOREIGN KEY (Roll) REFERENCES Student(Roll),
    FOREIGN KEY (EID) REFERENCES Event(EID)
);

-- Create Event_Participant Relation table
CREATE TABLE Event_Participant (
    EID INTEGER,
    PID INTEGER,
    Position INTEGER DEFAULT 0,
    PRIMARY KEY (EID, PID),
    FOREIGN KEY (EID) REFERENCES Event(EID),
    FOREIGN KEY (PID) REFERENCES Participant(PID)
);

-- Create Volunteer table
CREATE TABLE Volunteer (
    Roll INTEGER PRIMARY KEY,
    EID INTEGER,
    FOREIGN KEY (Roll) REFERENCES Student(Roll),
    FOREIGN KEY (EID) REFERENCES Event(EID)
);

-- Create Organizer table
CREATE TABLE Organizer (
    Roll INTEGER PRIMARY KEY,
    EID INTEGER,
    email VARCHAR(255) NOT NULL,
    FOREIGN KEY (Roll) REFERENCES Student(Roll),
    FOREIGN KEY (EID) REFERENCES Event(EID)
);

INSERT INTO Event (EID, EName, Date, Desc, Winners) VALUES (1, 'Dance', '2020-01-01', 'Dance Competition', '1,2,3');