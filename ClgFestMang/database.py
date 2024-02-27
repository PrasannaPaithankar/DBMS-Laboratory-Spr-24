from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import json

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
    role1 = ClgFestMang.models.Role(Rname='Student', Description='Student')
    role2 = ClgFestMang.models.Role(Rname='Volunteer', Description='Volunteer')
    role3 = ClgFestMang.models.Role(Rname='Organizer', Description='Organizer')
    db_session.add(role1)
    db_session.add(role2)
    db_session.add(role3)
    db_session.commit()

