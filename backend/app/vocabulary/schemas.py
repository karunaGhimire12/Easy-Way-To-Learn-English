
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class VocabularyDefinitionSchema(BaseModel):
    part_of_speech: Optional[str] = None
    definition: str
    example_sentence: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VocabularyPronunciationSchema(BaseModel):
    ipa: Optional[str] = None
    pronunciation_guide: Optional[str] = None
    audio_url: Optional[str] = None
    accent: Optional[str] = None

    audio_source_url: Optional[str] = None
    audio_license_name: Optional[str] = None
    audio_license_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VocabularyRelationSchema(BaseModel):
    related_word: str
    relation_type: str

    model_config = ConfigDict(from_attributes=True)


class VocabularyResponse(BaseModel):
    id: int
    word: str
    level: Optional[str] = None

    definitions: list[VocabularyDefinitionSchema] = Field(default_factory=list)
    pronunciations: list[VocabularyPronunciationSchema] = Field(default_factory=list)
    relations: list[VocabularyRelationSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
