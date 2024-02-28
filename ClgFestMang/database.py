from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import json
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
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import ClgFestMang.models
    Base.metadata.create_all(bind=engine)


def rebuild_db():
    import ClgFestMang.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Initialize roles
    role1 = ClgFestMang.models.Role(Rname='user', Description='Standard User')
    role2 = ClgFestMang.models.Role(Rname='admin', Description='Administrator')
    db_session.add(role1)
    db_session.add(role2)
    stu = ClgFestMang.models.Student(Name='test', email='t@t', password=generate_password_hash('t'), Dept='CSE', RID=1, gender='F')
    db_session.add(stu)
    stu = ClgFestMang.models.Student(Name='prasanna', email='p@p', password=generate_password_hash('p'), Dept='CSE', RID=2, gender='M')
    db_session.add(stu)
    event = ClgFestMang.models.Event(EName='Debate', Date='2024-01-01', Desc='Debate with Aviral', Winners='Aviral Chomu')
    db_session.add(event)
    part = ClgFestMang.models.Participant(Name='harsh', email='h@h', accomodation='Azad', vegnonveg=True, CName='IITD', password=generate_password_hash('h'), gender='M')
    db_session.add(part)
    db_session.commit()

