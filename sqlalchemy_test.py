from sqlalchemy import create_engine

engine = create_engine('mysql://root:123@localhost/study?charset=utf8')