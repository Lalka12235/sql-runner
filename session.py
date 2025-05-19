from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

engine = create_engine(
    url='sqlite+pysqlite:///:memory:',
    echo=True
)

Session = create_session(bind=engine)