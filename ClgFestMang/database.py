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

    stu = ClgFestMang.models.Student(Name='test', email='t@t', password=generate_password_hash('t'), Dept='CSE', RID=1, gender='F')
    db_session.add(stu)
    stu = ClgFestMang.models.Student(Name='prasanna', email='p@p', password=generate_password_hash('p'), Dept='CSE', RID=2, gender='M')
    db_session.add(stu)
    
    event = ClgFestMang.models.Event(EName='Debate', Date='2024-01-01', Desc='Debate with Aviral', Winner1='Aviral', Winner2='Aviral', Winner3='Aviral')
    db_session.add(event)
    part = ClgFestMang.models.Participant(Name='harsh', email='harshsharma2024@gmail.com', accomodation='Azad', vegnonveg=True, CName='IITD', password=generate_password_hash('h'), gender='M')
    db_session.add(part)

    stu = ClgFestMang.models.Student(Name='organ', email='o@o', password=generate_password_hash('o'), Dept='EE', RID=4, gender='F')
    db_session.add(stu)
    org = ClgFestMang.models.Organizer(Roll=3, EID=1)
    db_session.add(org)

    stu = ClgFestMang.models.Student(Name='vol', email='v@v', password=generate_password_hash('v'), Dept='ME', RID=3, gender='M')
    db_session.add(stu)
    vol = ClgFestMang.models.Volunteer(Roll=1, EID=1)
    db_session.add(vol)

    db_session.commit()
