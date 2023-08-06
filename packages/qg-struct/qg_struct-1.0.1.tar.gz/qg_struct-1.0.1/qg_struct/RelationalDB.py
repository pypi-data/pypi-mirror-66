def model_to_dict(model):
    return dict((col, getattr(model, col)) for col in model.__table__.columns.keys())


# from sqlalchemy import create_engine
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import sessionmaker
# import datetime
# import random

# Base = automap_base()
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/spider?charset=utf8',
#                        encoding='utf-8', pool_pre_ping=True)
# Base.prepare(engine, reflect=True)

# urlmodel = Base.classes.url


# def get_session():
#     session = sessionmaker(bind=engine, expire_on_commit=False)()
#     return session


# user = ['zwd', 'lbb', 'pyjq', 'cw', 'lrj']

# number = 100000


# def clear():
#     session = get_session()
#     session.execute('truncate table url')
#     session.commit()
#     session.close()


# def test1():
#     begin = datetime.datetime.now()
#     session = get_session()
#     for i in range(0, number):
#         url = f'http://test1.com/{i}'
#         html = f'test1 hello world my no{i}'
#         create_user = random.choice(user)
#         create_date = begin
#         session.add(urlmodel(url=url, html=html, create_user=create_user, create_date=create_date))
#     session.commit()
#     session.close()
#     print(f'test1: {datetime.datetime.now() - begin}')
#     clear()


# def test2():
#     begin = datetime.datetime.now()
#     session = get_session()
#     urlmodels = []
#     for i in range(0, number):
#         url = f'http://test2.com/{i}'
#         html = f'test2 hello world my no{i}'
#         create_user = random.choice(user)
#         create_date = begin
#         urlmodels.append(urlmodel(url=url, html=html, create_user=create_user, create_date=create_date))
#     session.add_all(urlmodels)
#     session.commit()
#     session.close()
#     print(f'test2: {datetime.datetime.now() - begin}')
#     clear()


# def test3():
#     begin = datetime.datetime.now()
#     session = get_session()
#     urlmodels = []
#     for i in range(0, number):
#         url = f'http://test3.com/{i}'
#         html = f'test3 hello world my no{i}'
#         create_user = random.choice(user)
#         create_date = begin
#         urlmodels.append(dict(url=url, html=html, create_user=create_user, create_date=create_date))
#     session.bulk_insert_mappings(urlmodel, urlmodels)
#     session.commit()
#     session.close()
#     print(f'test3: {datetime.datetime.now() - begin}')
#     clear()


# def test4():
#     begin = datetime.datetime.now()
#     session = get_session()
#     urlmodels = []
#     for i in range(0, number):
#         url = f'http://test4.com/{i}'
#         html = f'test4 hello world my no{i}'
#         create_user = random.choice(user)
#         create_date = begin
#         urlmodels.append(urlmodel(url=url, html=html, create_user=create_user, create_date=create_date))
#     session.bulk_save_objects(urlmodels)
#     session.commit()
#     session.close()
#     print(f'test4: {datetime.datetime.now() - begin}')
#     clear()


# test1()
# test2()
# test3()
# test4()
