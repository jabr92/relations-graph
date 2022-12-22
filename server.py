

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://localhost:5432/relations_graph', echo=True)
Session = sessionmaker(bind=engine)

