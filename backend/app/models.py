from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.sql import func
from .database import Base 
from sqlalchemy.orm import relationship 


class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True )
    name=Column(String,nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)

    password_hash=Column(String,nullable=True)

    auth_provider=Column(String,default="local")
    google_id=Column(String,unique=True,nullable=True)

    level=Column(String,default="Beginner")
    xp=Column(Integer,default=0)
    streak=Column(Integer,default=0)


    created_at=Column(DateTime(timezone=True),server_default=func.now())


class RevokedToken(Base):
    __tablename__="revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Vocabulary(Base):
    __tablename__="vocabulary"

    id=Column(Integer,primary_key=True,index=True)
    word=Column(String,unique=True,index=True,nullable=False)
    level=Column(String,default="Beginner")
    created_at=Column(DateTime(timezone=True),server_default=func.now())


    definitions=relationship(
        "VocabularyDefinition",
        back_populates="vocabulary",
        cascade="all, delete-orphan"
    )


    pronunciations=relationship(
        "VocabularyPronunciation",
        back_populates="vocabulary",
        cascade="all, delete-orphan"
    )


    relations = relationship(
    "VocabularyRelation",
    back_populates="vocabulary",
    cascade="all, delete-orphan"
)



#Vocabulary Definition Model

class VocabularyDefinition(Base):
    __tablename__ = "vocabulary_definitions"

    id = Column(Integer, primary_key=True, index=True)

    vocabulary_id = Column(Integer, ForeignKey("vocabulary.id"), nullable=False)
    part_of_speech = Column(String, nullable=True)
    definition = Column(String, nullable=False)
    example_sentence = Column(String, nullable=True)

    vocabulary=relationship(
        "Vocabulary",
        back_populates="definitions"
    )


# Vocabulary Pronunciation Model

class VocabularyPronunciation(Base):
    __tablename__ = "vocabulary_pronunciations"

    id = Column(Integer, primary_key=True, index=True)

    vocabulary_id = Column(Integer, ForeignKey("vocabulary.id"), nullable=False)

    ipa = Column(String, nullable=True)
    pronunciation_guide = Column(String, nullable=True)

    audio_url = Column(String, nullable=True)
    accent = Column(String, nullable=True)

    audio_source_url = Column(String, nullable=True)
    audio_license_name = Column(String, nullable=True)
    audio_license_url = Column(String, nullable=True)

    vocabulary = relationship(
    "Vocabulary",
    back_populates="pronunciations"
     )

    
# Vocabulary Relation Model

class VocabularyRelation(Base):
    __tablename__ = "vocabulary_relations"

    id = Column(Integer, primary_key=True, index=True)

    vocabulary_id = Column(Integer, ForeignKey("vocabulary.id"), nullable=False)

    related_word = Column(String, nullable=False)
    relation_type = Column(String, nullable=False)



    vocabulary=relationship(
        "Vocabulary",
        back_populates="relations"
    )
