# models.py for the ClgFestMang app, the database connects to postgresql and the models are defined here
from sqlalchemy import (DDL, Boolean, Column, Date, ForeignKey, Integer,
                        String, event)
from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy.exc import IntegrityError
from datetime import datetime


class Event(Base):
    __tablename__ = 'Event'
    __searchable__ = ['EName', 'Desc']
    EID = Column(Integer, primary_key=True)
    EName = Column(String(255), nullable=False)
    Date = Column(Date, nullable=False)
    Desc = Column(String(255))
    Venue = Column(String(255))
    Sponsor = Column(String(255))
    Winner1 = Column(String(255))
    Winner2 = Column(String(255))
    Winner3 = Column(String(255))

    def __init__(self, EName, Date, Desc, Winner1, Winner2, Winner3, Venue, Sponsor):
        self.EName = EName
        self.Date = Date
        self.Desc = Desc
        self.Winner1 = Winner1
        self.Winner2 = Winner2
        self.Winner3 = Winner3
        self.Venue = Venue
        self.Sponsor = Sponsor

    def __repr__(self):
        return '<Event %r>' % (self.EName)


class Participant(Base):
    __tablename__ = 'Participant'
    __searchable__ = ['Name', 'CName']
    PID = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    accomodation = Column(String(255))
    vegnonveg = Column(Boolean)
    CName = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    gender = Column(String(1), nullable=False)

    def __init__(self, Name, email, accomodation, vegnonveg, CName, password, gender, username):
        self.Name = Name
        self.email = email
        self.accomodation = accomodation
        self.vegnonveg = vegnonveg
        self.CName = CName
        self.password = password
        self.gender = gender
        self.username = username

    def __repr__(self):
        return '<Participant %r>' % (self.Name)


class Role(Base):
    __tablename__ = 'Role'
    RID = Column(Integer, primary_key=True)
    Rname = Column(String(255), nullable=False)
    Description = Column(String(255), nullable=False)

    def __init__(self, Rname, Description):
        self.Rname = Rname
        self.Description = Description

    def __repr__(self):
        return '<Role %r>' % (self.Rname)


class Student(Base):
    __tablename__ = 'Student'
    __searchable__ = ['Name', 'Dept']
    Roll = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    Dept = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    RID = Column(Integer, ForeignKey('Role.RID'))
    password = Column(String(255), nullable=False)
    gender = Column(String(1), nullable=False)
    role = relationship('Role', backref='students')

    def __init__(self, Name, Dept, email, RID, password, gender, username):
        self.Name = Name
        self.username = username
        self.Dept = Dept
        self.email = email
        self.RID = RID
        self.password = password
        self.gender = gender

    def __repr__(self):
        return '<Student %r>' % (self.Name)


class Student_Event(Base):
    __tablename__ = 'Student_Event'
    Roll = Column(Integer, ForeignKey(
        'Student.Roll'), primary_key=True)
    EID = Column(Integer, ForeignKey('Event.EID'), primary_key=True)
    Position = Column(Integer, default=0)
    student = relationship('Student', backref='events')
    event = relationship('Event', backref='students')

    def __init__(self, Roll, EID, Position):
        self.Roll = Roll
        self.EID = EID
        self.Position = Position

    def __repr__(self):
        return '<Student_Event %r>' % (self.Roll)


class Event_Participant(Base):
    __tablename__ = 'Event_Participant'
    EID = Column(Integer, ForeignKey('Event.EID'), primary_key=True)
    PID = Column(Integer, ForeignKey(
        'Participant.PID'), primary_key=True)
    Position = Column(Integer, default=0)
    event = relationship('Event', backref='participants')
    participant = relationship('Participant', backref='events')

    def __init__(self, EID, PID, Position):
        self.EID = EID
        self.PID = PID
        self.Position = Position

    def __repr__(self):
        return '<Event_Participant %r>' % (self.EID)


class Volunteer(Base):
    __tablename__ = 'Volunteer'
    __searchable__ = ['Roll']
    Roll = Column(Integer, ForeignKey(
        'Student.Roll'), primary_key=True)
    EID = Column(Integer, ForeignKey('Event.EID'), primary_key=True)
    student = relationship('Student', backref='volunteers')
    event = relationship('Event', backref='volunteers')

    def __init__(self, Roll, EID):
        self.Roll = Roll
        self.EID = EID

    def __repr__(self):
        return '<Volunteer %r>' % (self.Roll)


class Organizer(Base):
    __tablename__ = 'Organizer'
    Roll = Column(Integer, ForeignKey(
        'Student.Roll'), primary_key=True)
    EID = Column(Integer, ForeignKey('Event.EID'), primary_key=True)
    student = relationship('Student', backref='organizers')
    event = relationship('Event', backref='organizers')

    def __init__(self, Roll, EID):
        self.Roll = Roll
        self.EID = EID

    def __repr__(self):
        return '<Organizer %r>' % (self.Roll)


class Notification(Base):
    __tablename__ = 'Notification'
    NID = Column(Integer, primary_key=True)
    sender = Column(Integer, ForeignKey('Student.Roll'))
    receiver = Column(Integer, ForeignKey('Student.Roll'))
    message = Column(String(500), nullable=False)
    time = Column(Date, nullable=False)
    studentRecv = relationship('Student', foreign_keys=[receiver])
    studentSend = relationship('Student', foreign_keys=[sender])

    def __init__(self, sender, receiver, message,time):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.time = time

    def __repr__(self):
        return '<Notification %r>' % (self.NID)


class food(Base):
    __tablename__ = 'food'
    FID = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    type = Column(Boolean, nullable=False)
    detail = Column(String(255), nullable=False)

    def __init__(self, Name, type, detail):
        self.Name = Name
        self.type = type
        self.detail = detail

    def __repr__(self):
        return '<food %r>' % (self.Name)


def modifyfood_listener(mapper, connection, target):
    if connection.dialect.name == 'postgresql':
        print("Trigger event is an INSERT")
        existing_food = connection.execute(
            food.__table__.select().where(food.Name == target.Name)
        ).fetchone()

        if existing_food:
            connection.execute(
                food.__table__.update().
                where(food.Name == target.Name).
                values(type=target.type, detail=target.detail)
            )

event.listen(food, 'before_insert', modifyfood_listener)

trigger_ddl = DDL("""
CREATE OR REPLACE FUNCTION modifyfood_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE food
        SET type = NEW.type,
            detail = NEW.detail
        WHERE Name = NEW.Name;
        RETURN NEW;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
""")

event.listen(food.__table__, 'after_create', trigger_ddl)


def notification_trigger_listener(mapper, connection, target):
    if connection.dialect.name == 'postgresql':
        target.time = datetime.now().date() 

        try:
            sender_student = connection.execute(Student.__table__.select().where(Student.Roll == target.sender)).fetchone()
            receiver_student = connection.execute(Student.__table__.select().where(Student.Roll == target.receiver)).fetchone()

            if not sender_student or not receiver_student:
                raise IntegrityError(None, None, None)

        except IntegrityError:
            raise ValueError('Invalid sender or receiver')

event.listen(Notification, 'before_insert', notification_trigger_listener)