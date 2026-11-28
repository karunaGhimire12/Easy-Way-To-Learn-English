from fastapi import APIRouter,Depends,HTTPException
from  sqlalchemy.orm import Session

from app.database import get_db
from app.models import Vocabulary 
from app.vocabulary.schemas import VocabularyResponse


router=APIRouter(
    prefix="/vocabulary",
    tags=["Vocabulary"]
)


@router.get("/")
def vocabulary_home():
    return {
        "message":"Vocabulary router is working now ! "
}


@router.get("/{word}",response_model=VocabularyResponse)
def search_vocabulary(
    word:str,
    db:Session=Depends(get_db)
):
    searched_word=word.strip().lower()

    vocabulary=db.query(Vocabulary).filter(
        Vocabulary.word== searched_word
    ).first()

    if vocabulary is None:
        raise HTTPException(
            status_code=404,
            detail="Sorry, we couldn't find this word."
        )

    return vocabulary
