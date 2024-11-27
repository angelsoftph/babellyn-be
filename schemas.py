from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LanguageBase(BaseModel):
    name: str
    story: Optional[str] = None


class LanguageCreate(LanguageBase):
    pass


class Language(LanguageBase):
    id: int

    class Config:
        from_attributes = True


class PhraseBase(BaseModel):
    phrase: str


class PhraseCreate(PhraseBase):
    pass


class Phrase(PhraseBase):
    id: int

    class Config:
        from_attributes = True


class TranslationBase(BaseModel):
    phrase_id: int
    language_id: int
    trans: str
    user_id: int


class TranslationCreate(TranslationBase):
    pass


class TranslationUpdate(BaseModel):
    trans: Optional[str]


class Translation(TranslationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class FlagBase(BaseModel):
    translation_id: int
    user_id: int
    flag: Optional[str] = None
    comment: Optional[str] = None


class FlagCreate(FlagBase):
    pass


class Flag(FlagBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True