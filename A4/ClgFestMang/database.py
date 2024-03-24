import json

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from werkzeug.security import generate_password_hash

with open('./instance/config.json') as config_file:
    config = json.load(config_file)

engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import ClgFestMang.models
    Base.metadata.create_all(bind=engine)


def rebuild_db():
    import ClgFestMang.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Initialize roles
    role = ClgFestMang.models.Role(Rname='user', Description='Standard User')
    db_session.add(role)
    role = ClgFestMang.models.Role(Rname='admin', Description='Administrator')
    db_session.add(role)
    role = ClgFestMang.models.Role(Rname='volunteer', Description='Volunteer')
    db_session.add(role)
    role = ClgFestMang.models.Role(Rname='organizer', Description='Organizer')
    db_session.add(role)

    stu = ClgFestMang.models.Student(Name='test', username = 'test',email='t@t', password=generate_password_hash('t'), Dept='CSE', RID=1, gender='F')
    db_session.add(stu)
    stu = ClgFestMang.models.Student(Name='prasanna', username = 'prasanna',email='p@p', password=generate_password_hash('p'), Dept='CSE', RID=2, gender='M')
    db_session.add(stu)
    st = ClgFestMang.models.Student(Name='aviral', username = 'aviral',email='a@a', password=generate_password_hash('a'), Dept='CSE', RID = 3,gender='M')
    db_session.add(st)
    st = ClgFestMang.models.Student(Name='utsav', username = 'utsav',email='u@u', password=generate_password_hash('u'), Dept='CSE', RID = 4,gender='M')
    db_session.add(st)
    st = ClgFestMang.models.Student(Name='parth', username = 'parth',email='pa@pa', password=generate_password_hash('p'), Dept='CSE', RID = 3,gender='M')
    db_session.add(st)

    event = ClgFestMang.models.Event(EName='Debate', Date='2024-03-06', Desc='Debate with Aviral', Winner1='To be decided', Winner2='To be decided', Winner3='To be decided',Venue='Kalidas', Sponsor='Pepsi')
    db_session.add(event)
    event = ClgFestMang.models.Event(EName='Dance', Date='2024-01-01', Desc='Dance with Utsav', Winner1='Aviral', Winner2='Aviral', Winner3='Aviral', Venue='Kalidas', Sponsor='Pepsi')
    db_session.add(event)
    event = ClgFestMang.models.Event(EName='Music', Date='2024-03-06', Desc='Music with Harsh', Winner1='Aviral', Winner2='Aviral', Winner3='Aviral',Venue='Kalidas', Sponsor='Pepsi')
    db_session.add(event)
    event = ClgFestMang.models.Event(EName='Hackathon', Date='2024-03-06', Desc='Hackathon with Prasanna', Venue='Azad', Sponsor='Optiver', Winner1='To be decided', Winner2='To be decided', Winner3='To be decided')
    db_session.add(event)

    part = ClgFestMang.models.Participant(Name='harsh',username='harsh', email='h@h', accomodation='Azad', vegnonveg=True, CName='IITD', password=generate_password_hash('h'), gender='M')
    db_session.add(part)
    stu = ClgFestMang.models.Student(Name='organ', username = 'organ',email='o@o', password=generate_password_hash('o'), Dept='EE', RID=4, gender='F')
    db_session.add(stu)

    stu = ClgFestMang.models.Volunteer(Roll=3, EID=1)
    db_session.add(stu)
    stu = ClgFestMang.models.Volunteer(Roll=5, EID=1)
    db_session.add(stu)

    org = ClgFestMang.models.Organizer(Roll=4, EID=1)
    db_session.add(org)

    noti = ClgFestMang.models.Notification(sender=4, receiver=5, message='hello', time = '2024-01-01')
    db_session.add(noti)
    noti = ClgFestMang.models.Notification(sender=4, receiver=5, message='hello', time = '2024-01-01')
    db_session.add(noti)
    noti = ClgFestMang.models.Notification(sender=4, receiver=5, message='hello', time = '2024-01-01')
    db_session.add(noti)
    noti = ClgFestMang.models.Notification(sender=4, receiver=5, message='hello', time = '2024-01-01')
    db_session.add(noti)
    
    noti = ClgFestMang.models.Notification(sender=4, receiver=5, message='hello', time = '2024-01-01')
    db_session.add(noti)

    food = ClgFestMang.models.food(Name = 'Chicken Paratha', type = True, detail = 'Chicken')
    db_session.add(food)
    food = ClgFestMang.models.food(Name = 'Paneer Bhurji', type = False, detail = 'Paneer')
    db_session.add(food)

    db_session.commit()
