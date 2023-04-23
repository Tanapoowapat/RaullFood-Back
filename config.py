from dotenv import load_dotenv
import os

load_dotenv()


# LOAD DATABASE CONFIG
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

postgresqlConfig = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER,
    DB_PASS,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)

#LOAD SECRET KEY 
SECRET_KEY = os.getenv("SECRET_KEY")