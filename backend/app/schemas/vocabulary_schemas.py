from pydantic import BaseModel
class VocabularyCreate(BaseModel):
    word:str
    meaning:str
    synonyms:str|None=None
    antonyms:str|None=None
    example_sentences:str|None=None
    level:str="Beginner"



class VocabularyResponse(BaseModel):
    id: int
    word: str
    meaning: str
    synonyms: str | None = None
    antonyms: str | None = None
    example_sentence: str | None = None
    level: str