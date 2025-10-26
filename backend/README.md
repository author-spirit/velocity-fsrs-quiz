## Intro
Velocity flashcard & quiz app built for easy customization and reliablity

## Requirements
- Server: FastAPI - Async, Uvicorn
- Database: Sqlite, peewee ORM, Pydantic

## Folder Structure
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
### Server
- `uvicorn main:app --reload`
- Running at `localhost:8000`

## TODO
- Enable Edit Mode for flashcard
- Provide Quiz Service

## Endpoints
- Get Card By Id
```
GET: {url}/flashcard/deck/{id}
Response: JSON
```

- Create Deck
```
POST: {url}/flashcard/deck
Request Body:
{
    "name": <Name of Deck>
    "author": <Author Name>
}
```