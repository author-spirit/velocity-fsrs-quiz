## Intro
Velocity flashcard & quiz app built for easy customization and reliablity.

Velocity uses (Py-FSRS service)(https://github.com/open-spaced-repetition/py-fsrs)

## Requirements
- Server: FastAPI
- Database: Sqlite, peewee ORM, Pydantic

## Backend folder Structure
- **core:** contains core functionalities of app like config, connector etc
- **db:** database related files - SQLite connector, Sqlite DB file
- **models:** ORM, database models
- **schema:** pydantic schema for my tables
- **scripts:** Runnable scripts
- **services:** features provided by the app
    - **flashcard:** Deck, Card and other operations
    - **quiz:** Quiz operations
- **tests:** unit tests
- **.env:** configurations
- **main.py:** Main python executor

## How To
### First time installation
- Run `python3 scripts/setup.py`

### Server
- `uvicorn main:app --reload`
- Running at `localhost:8000`

### Migration
- Run `python3 scripts/dbmigration.py`

## Apis
Use swagger
> http://127.0.0.1:8000/docs
