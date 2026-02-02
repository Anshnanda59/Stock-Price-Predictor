import pandas as pd
from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from datetime import date
from typing import Annotated
import pickle

with open('Stock_price_predictor.pkl','rb') as f:
    model = pickle.load(f)


app = FastAPI()
class StockData(BaseModel):
    symbol : Annotated[str,Field(...)]
    date : Annotated[date,Field(...,description='Market open Date')]
    open : Annotated[float,Field(...,description='Opens at ')]
    high : Annotated[float,Field(...,description='Highest value ')]
    low : Annotated[float,Field(...,description='Lowest value ')]
    volume : Annotated[int,Field(...,description='Volume ')]

@app.get('/')
def root():
    return {'message': 'Stock price predictor'}

@app.post('/predict_stock')
async def predict_stock(data: StockData):
    df = pd.DataFrame([{
        'symbol':data.symbol,
        'date':data.date,
        'open':data.open,
        'high':data.high,
        'low':data.low,
        'volume':data.volume
    }])
    
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df = df.drop('date',axis=1)
    
    predict = model.predict(df)[0]

    return JSONResponse(status_code=200,content={'Predicted_close': f'{predict}'})
    
    