from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy.orm import Session
import defs, models, schemas

app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/languages", tags=["Languages"], response_model=List[schemas.Language])
def list_languages(db: Session = Depends(get_db)):
    """
    List all available languages
    """

    return defs.list_languages(db)


@app.post("/languages", tags=["Languages"], response_model=schemas.Language)
def create_language(language: schemas.LanguageCreate, db: Session = Depends(get_db)):
    """
    Create a new language
    """

    return defs.create_language(db, language)


@app.get("/phrases", tags=["Phrases"], response_model=List[schemas.Phrase])
def list_phrases(db: Session = Depends(get_db)):
    """
    List all available phrases
    """

    return defs.list_phrases(db)


@app.post("/phrases", tags=["Phrases"], response_model=schemas.Phrase)
def create_phrase(phrase: schemas.PhraseCreate, db: Session = Depends(get_db)):
    """
    Create a new phrase
    """

    return defs.create_phrase(db, phrase)


@app.get("/translations/", tags=["Translations"], response_model=list[schemas.Translation])
def get_translations_by_phrase(phrase: str, language_id: int, db: Session = Depends(get_db)):
    """
    Get translations for a specific phrase text and language ID
    """

    translations = defs.get_translations_by_phrase(db, phrase, language_id)
    if not translations:
        raise HTTPException(status_code=404, detail="No translations found for the given phrase and language")

    return translations


@app.get("/translations/{phrase_id}", tags=["Translations"], response_model=list[schemas.Translation])
def get_translations_by_phrase_id(phrase_id: int, db: Session = Depends(get_db)):
    """
    Get translations for a specific phrase ID
    """

    translations = defs.get_translations_by_phrase_id(db, phrase_id)
    if not translations:
        raise HTTPException(status_code=404, detail="No translations found for the given phrase_id")
    return translations


@app.post("/translations", tags=["Translations"], response_model=schemas.Translation)
def create_translation(translation: schemas.TranslationCreate, db: Session = Depends(get_db)):
    """
    Create a new translation for a specific phrase ID and language ID
    """

    phrase = db.query(models.Phrase).filter(models.Phrase.id == translation.phrase_id).first()
    language = db.query(models.Language).filter(models.Language.id == translation.language_id).first()
    user = db.query(models.User).filter(models.User.id == translation.user_id).first()

    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return defs.create_translation(db, translation)


@app.get("/get_flags/{translation_id}", tags=["Flags"], response_model=list[schemas.FlagResponse])
async def get_flags(translation_id: int, db: Session = Depends(get_db)):
    """
    Get flags for a specific translation ID
    """

    flags = defs.get_flags_by_translation_id(db, translation_id)
    if not flags:
        raise HTTPException(status_code=404, detail="No flags found for the given translation_id")

    return [
        {
            "id": flag.id,
            "translation_id": flag.translation_id,
            "user_id": flag.user_id,
            "flag": flag.flag,
            "comment": flag.comment,
            "created_at": flag.created_at,
            "updated_at": flag.updated_at,
            "uname": flag.user.uname
        }
        for flag in flags
    ]


@app.post("/flag_translation/", tags=["Flags"], response_model=schemas.FlagResponse)
async def flag_translation(flag: schemas.FlagCreate, db: Session = Depends(get_db)):
    """
    Flag a translation
    0: Incorrect
    1: Accurate
    """

    if flag.flag not in ["0", "1"]:
        raise HTTPException(status_code=400, detail="Flag must be either '0' or '1'.")

    new_flag = defs.flag_translation(db, flag)

    return new_flag


@app.post("/users", tags=["Users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """

    return defs.create_user(db, user)
