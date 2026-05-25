from fastapi import APIRouter
from app.schemas.RecommendSchema import RecommendMLRequest, RecommendMLResponse
from app.services.model_service import predict_epa_options, recommend
router = APIRouter() 

@router.post("/recommended/ml",response_model=RecommendMLResponse)
def getML_Recommendation(inp:RecommendMLRequest): 
    yardLine100 = inp.yardline_100
    ydstogo = inp.ydstogo
    
    predictedepa = predict_epa_options(yardLine100,ydstogo)
    recommendation = recommend(yardLine100,ydstogo)
    return{
        "recommendation": recommendation,
        "predicted_epa" :predictedepa,
        
    }