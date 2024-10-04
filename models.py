# database/models.py

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

class ForexRate(Base):
    __tablename__ = 'forex_rates'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    base_currency = Column(String(50), nullable=False)
    quote_currency = Column(String(50), nullable=False)
    rate = Column(Float, nullable=False)

# database/db.py

# from database.models import Base, ForexRate

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    try:
        Base.metadata.create_all(engine)
        print("Database connected and tables created successfully.")
    except SQLAlchemyError as e:
        print(f"Database connection failed: {e}")
        raise

def insert_forex_rate(date, base_currency, quote_currency, rate):
    session = Session()
    forex_rate = ForexRate(date=date, base_currency=base_currency, quote_currency=quote_currency, rate=rate)
    session.add(forex_rate)
    session.commit()
    session.close()

def get_average_rate(base_currency, quote_currency, start_date, end_date):
    session = Session()
    avg_rate = session.query(func.avg(ForexRate.rate)).filter(
        ForexRate.base_currency == base_currency,
        ForexRate.quote_currency == quote_currency,
        ForexRate.date.between(start_date, end_date)
    ).scalar()
    session.close()
    return avg_rate

def get_closing_rate(base_currency, quote_currency, date):
    session = Session()
    rate = session.query(ForexRate.rate).filter(
        ForexRate.base_currency == base_currency,
        ForexRate.quote_currency == quote_currency,
        ForexRate.date == date
    ).order_by(ForexRate.id.desc()).first()
    session.close()
    return rate[0] if rate else None