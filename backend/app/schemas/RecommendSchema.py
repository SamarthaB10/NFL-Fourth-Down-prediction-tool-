from pydantic import BaseModel, Field,ConfigDict,field_validator,model_validator
from typing import Optional,Dict
from datetime import datetime

VALID_TEAMS = {
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LV", "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS",
}

class RecommendationRequest(BaseModel):
    model_config = ConfigDict(
      json_schema_extra=  {
        "examples":[{
            "season": 2026,
            "posteam": "BAL",
            "defteam": "KC",
            "yardline_100": 45,
            "ydstogo": 4
        }]
        
        }
    )
    season: int = Field(..., ge=1999, le=datetime.now().year,description= "Target season you are looking for, we will query its historical seasons prior to it ")
    posteam: Optional[str] = Field(None, min_length=2, max_length=3,description="Team on offense,optional")
    defteam: Optional[str] = Field(None, min_length=2, max_length=3,description="Team on defense, optional ")
    yardline_100: int = Field(..., ge=1, le=99,description="Yards from the opponent endzone, lower = closer to scoring")
    ydstogo: int = Field(..., ge=1, le=99,description="Yards needed till the first down")
    
    @field_validator("posteam","defteam")
    @classmethod
    def normalize_team_abbreviation(cls,value:Optional[str])->Optional[str]: 
        if value is None: 
            return value 
        normalized = value.strip().upper()
        recommendation = None 
        if normalized in VALID_TEAMS: 
            return normalized
        for team in VALID_TEAMS:
            if team.startswith(normalized[:2]): 
                recommendation = team
                break
            if len(normalized) >= 2 and team.endswith(normalized[-2:]): 
                recommendation = team 
        
        if not recommendation: 
             raise ValueError(f"Invalid NFL team abbreviation: {value}")
        else: 
            raise ValueError(
            f"Invalid NFL team abbreviation: {value}. "
            f"Did you mean '{recommendation}'?"
            )
    
    @model_validator(mode="after")
    def validate_matchup(self): 
        if self.posteam is not None and self.defteam is not None: 
            if self.posteam == self.defteam:
                raise ValueError("Teams cannot be the same ")
        return self




class RecommendationOptions(BaseModel):
    count: int = Field(..., ge=0)
    avgEpa: Optional[float] = None


class HistoricalContext(BaseModel):
    similarPlays: int = Field(..., ge=0)
    decisionCounts: Dict[str, int]
    averageEpa: Dict[str, Optional[float]]


class RecommendationResponse(BaseModel):
    recommendation: Optional[str] = Field(None, description="Model Recommendation")
    options: Dict[str, RecommendationOptions]
    historical_context: HistoricalContext
    input: RecommendationRequest
    message: Optional[str] = None



class RecommendMLRequest(BaseModel): 
    yardline_100:int = Field(..., le = 99, ge=1, description="Yard line of the play, 5 yard line is 5 yards from endzone ")
    ydstogo :int = Field(...,le= 50,ge=1, description= "4th and 5, 4th and 10 etc")
    
class RecommendMLResponse(BaseModel): 
    recommendation: str = Field(..., description="ML recommendation")
    predicted_epa : Dict[str,float]
