from fastapi import HTTPException,status,APIRouter,Depends,Response
from ..database import get_db
from  sqlalchemy.orm import Session
from .. import schemas,models,utils,oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['authentication']
)
 
@router.post('/login')
def login(user_credential:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail='Invalid credential!')
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credential!!!!!")
   
    access_token = oauth.create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token,"token_type" : "bearer"}