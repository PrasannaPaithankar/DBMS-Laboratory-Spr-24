# models.py for the ClgFestMang app, the database connects to postgresql and the models are defined here
from sqlalchemy import (DDL, Boolean, Column, Date, ForeignKey, Integer,
                        String, event)
from sqlalchemy.orm import relationship

from .database import Base


class Event(Base):
    __tablename__ = 'Event'
    __searchable__ = ['EName', 'Desc']
    EID = Column(Integer, primary_key=True)
    EName = Column(String(255), nullable=False)
    Date = Column(Date, nullable=False)
    Desc = Column(String(255))
    Winner1 = Column(String(255))
    Winner2 = Column(String(255))
    Winner3 = Column(String(255))

    def __init__(self, EName, Date, Desc, Winner1, Winner2, Winner3):
        self.EName = EName
        self.Date = Date
        self.Desc = Desc
        self.Winner1 = Winner1
        self.Winner2 = Winner2
        self.Winner3 = Winner3

    def __repr__(self):
        return '<Event %r>' % (self.EName)


class Participant(Base):
    __tablename__ = 'Participant'
    __searchable__ = ['Name', 'CName']
    PID = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    accomodation = Column(String(255))
    vegnonveg = Column(Boolean)
    CName = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    gender = Column(String(1), nullable=False)

    def __init__(self, Name, email, accomodation, vegnonveg, CName, password, gender):
        self.Name = Name
        self.email = email
        self.accomodation = accomodation
        self.vegnonveg = vegnonveg
        self.CName = CName
        self.password = password
        self.gender = gender

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
    Dept = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    RID = Column(Integer, ForeignKey('Role.RID'))
    password = Column(String(255), nullable=False)
    gender = Column(String(1), nullable=False)
    role = relationship('Role', backref='students')

    def __init__(self, Name, Dept, email, RID, password, gender):
        self.Name = Name
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
    email = Column(String(255), nullable=False)
    student = relationship('Student', backref='organizers')
    event = relationship('Event', backref='organizers')

    def __init__(self, Roll, EID, email):
        self.Roll = Roll
        self.EID = EID
        self.email = email

    def __repr__(self):
        return '<Organizer %r>' % (self.Roll)


# class Notification(Base):
#     __tablename__ = 'Notification'
#     NID = Column(Integer, primary_key=True)
#     EID = Column(Integer, ForeignKey('Event.EID'))
#     Message = Column(String(255), nullable=False)
#     OrganizerOnly = Column(Boolean, default=False)
#     event = relationship('Event', backref='notifications')
#     participant = relationship('Participant', backref='notifications')

#     def __init__(self, EID, Message, OrganizerOnly):
#         self.EID = EID
#         self.Message = Message
#         self.OrganizerOnly = OrganizerOnly

#     def __repr__(self):
#         return '<Notification %r>' % (self.NID)


# notificationTrigger = DDL("""
#     CREATE TRIGGER notify
#     AFTER INSERT ON "Notification"
#     FOR EACH ROW
#     EXECUTE PROCEDURE notify_trigger();
# """)
# event.listen(Notification.__table__, 'after_create', notificationTrigger)
