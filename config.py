# config.py

SECRET_KEY = 'une_clé_secrète'
SECURITY_PASSWORD_SALT = 'sel_unique'

#SQLALCHEMY_DATABASE_URI = 'postgresql://suivi_user:6E5yKItPvmJNHOg4UwjN6EGNf6SlRf8H@dpg-d1j6g1ur433s73ftp56g-a.oregon-postgres.render.com/suiviactivites'
SQLALCHEMY_DATABASE_URI = 'postgresql://suivi_user:Suivi%401@10.7.5.179:5432/suivi_activites'

SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'nabasnak7@gmail.com'
MAIL_PASSWORD = 'qaat fwoc dvvt zsbj'
MAIL_DEFAULT_SENDER = 'nabasnak7@gmail.com'
