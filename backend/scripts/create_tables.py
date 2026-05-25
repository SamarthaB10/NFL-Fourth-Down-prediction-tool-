from app.models.fourth_down_play import FourthDownPlay
from app.database import Base,engine


def main(): 
    Base.metadata.create_all(bind = engine)
    print("tables created sucessfully")
    

if __name__ == "__main__": 
    main() 