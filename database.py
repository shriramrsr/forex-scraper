from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

print("hellow")

# class ForexRate(Base):
#     __tablename__ = 'forex_rates'

#     id = Column(Integer, primary_key=True)
#     date = Column(Date, nullable=False)
#     base_currency = Column(String(3), nullable=False)
#     quote_currency = Column(String(3), nullable=False)
#     rate = Column(Float, nullable=False)