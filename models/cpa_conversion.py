from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CPAConversion(Base):
    __tablename__ = 'cpa_conversions'
    id = Column(Integer, primary_key=True)
    reddit_post_id = Column(String, ForeignKey('posts.id'))
    medium_article = Column(String)
    linkedin_clicks = Column(Integer)
    conversions = Column(Integer)
