from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import List
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from model import models
from datetime import timedelta
from controller import order_controller, user_controller, store_controller, location_controller, raider_controller
from schemas import schemas



#INIT DB
models.Base.metadata.create_all(bind=engine)

#INTI APP
app = FastAPI()


# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Define the CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5500",
    "http://127.0.0.1:5500/",
    "http://127.0.0.1:5500"
]
# Add the middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return {"Hello": "World"}

# Routes
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_controller.auth_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_controller.create_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_dict = user_controller.decode_token(token)
    if not user_dict:
        raise HTTPException(HTTPException(status_code=401, detail="Invalid authentication credentials"))
    username = user_dict.get("sub")
    db_user = user_controller.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_controller.create_user(db=db, user=user)

@app.get('/users/{user_id}', response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_controller.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get('/users/', response_model=List[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_controller.get_users(db, skip=skip, limit=limit)


#location endpoint
#get ID
@app.get('/location/{location_id}', response_model= schemas.Location)
async def get_location(location_id : int, db : Session = Depends(get_db)):
    return location_controller.get_location_by_id(db=db, location_id=location_id)
#get all
@app.get('/location/', response_model=List[schemas.Location])
async def get_all_location(skip: int=0, limit:int=100, db:Session = Depends(get_db)):
    return location_controller.get_location(db, skip=skip, limit=limit)

# Update a location by ID
@app.put('/location/{location_id}', response_model=schemas.Location)
async def update_location(location_id: int, location: schemas.LocationUpdate, db: Session = Depends(get_db)):
    return location_controller.update_location(db=db, location_id=location_id, location=location)
#CREATE
@app.post("/location/", response_model=schemas.Location)
async def create_location(location: schemas.Location, db: Session = Depends(get_db)):
    return location_controller.create_location(db=db, location=location)
# DELETE
@app.delete("/location/{location_id}", response_model=schemas.Location)
async def delete_location(location_id : int, db : Session = Depends(get_db)):
    return location_controller.delete_location(db=db, location_id=location_id)

"""
STORE END POINT
"""
# Create a new store
@app.post('/stores', response_model=schemas.Store)
async def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    return store_controller.create_store(db=db, store=store)

# Get all stores
@app.get('/stores', response_model=List[schemas.Store])
async def read_stores(db: Session = Depends(get_db)):
    return store_controller.get_all_stores(db=db)

# Get a store by ID
@app.get('/stores/{store_id}', response_model=schemas.Store)
async def read_store(store_id: int, db: Session = Depends(get_db)):
    return store_controller.get_store_by_id(db=db, store_id=store_id)

# Update a store by ID
@app.put('/stores/{store_id}', response_model=schemas.Store)
async def update_store(store_id: int, store: schemas.StoreUpdate, db: Session = Depends(get_db)):
    return store_controller.update_store(db=db, store_id=store_id, store=store)

# Delete a store by ID
@app.delete('/stores/{store_id}', response_model=schemas.Store)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    return store_controller.delete_store(db=db, store_id=store_id)

#endpoint for raider

#get all
@app.get('/raiders/', response_model=List[schemas.Raider])
async def get_raiders(db: Session = Depends(get_db)):
    return raider_controller.get_all_raider(db=db)

#create raider
@app.post('/raiders/', response_model=schemas.Raider)
async def create_raider(raider: schemas.RaiderCreate, db: Session = Depends(get_db)):
    return raider_controller.create_raider(db=db, raider=raider)

#delete raider
@app.delete('/raiders/{raider_id}', response_model=schemas.Raider)
async def delete_raider(raider_id : int, db: Session = Depends(get_db)):
    return raider_controller.delete_raider(db=db, raider_id=raider_id)

"""
ORDER ENDPOINT
"""

#get_orders
@app.get('/orders/', response_model=List[schemas.Order])
async def get_all_order(db: Session = Depends(get_db)):
    return order_controller.get_all_orders(db=db)


#create order
@app.post('/orders/', response_model= schemas.Order)
async def create_order(order : schemas.OrderCreate, db : Session = Depends(get_db)):
    return order_controller.create_order(db = db, order = order)

#UPDATE ORDER
@app.put('/orders/', response_model= schemas.Order)
async def update_order(order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    return order_controller.update_order(db=db, order=order)

#GET ORDER by ID
@app.get('/orders/{order_id}', response_model=schemas.Order)
async def get_order(order_id : int, db : Session = Depends(get_db)):
    return order_controller.get_order_by_id(db=db, order_id=order_id)

#GET ORDER BY USER ID
@app.get('/orders/by_user_id/{user_id}', response_model=schemas.Order)
async def get_order_by_user_id(user_id: int, db : Session = Depends(get_db)):
    return order_controller.get_order_by_user_id(user_id=user_id, db=db)

#DELETE ORDER
@app.delete('/orders/{order_id}', response_model=schemas.Order)
async def delete_order(order_id : int, db : Session = Depends(get_db)):
    return order_controller.delete_order(db=db, order_id= order_id)

