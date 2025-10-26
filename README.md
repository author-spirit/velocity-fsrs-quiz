# velocity-NEST
Learning platform provides spaced-repetition, visual learning & contests

## Components
### Backend
- Python3 (FlaskAPI)

### DataModel
- Sqlite (Peewee)
- Supabase (after full implementation)

### Frontend
- Flutter (Planned)

# Schema
## Deck
- id | Int | Primary Key
- title | String | Deck title 
- mode | enum | flashcard/quiz
- owner | Foreign Key | User
- description | Text | Markdown
- tags | JSON
- created_time | timestamp
- modified_time | timestamp
- is_draft | boolean

## card
- id | Int | Primary Key
- deck_id | Foreign Key | Deck
- (optional) type	| enum	flashcard / mcq / code / interactive
- question	| Text	| The question text or prompt
- answers	| JSONB	| One or multiple answers, depending on type
- explanation	| Text	| Optional explanation
- order	| Int	| Position in deck
- difficulty | Enum | easy/medium/hard
- created_time | timestamp
- modified_time | timestamp

## The Hitchhiker's Guide
1. Modules: Keep the module names short avoid dot (.), use underscore but limit too much
2. Readability [Code Style](https://docs.python-guide.org/writing/style/#code-style)

## Folder Structure
```
velocity/
│    backend/
│    │── main.py
│    │── core/
│    │   └── __init__.py
│    │── db/
│    │   └── __init__.py
│    │── models/
│    │   └── __init__.py
│    │── schemas/
│    │   └── __init__.py
│    │── api/
│    │   └── __init__.py
│    │── services/
│    │   └── __init__.py
│    │── utils/
│    │   └── __init__.py
│    │── tests/
│    │   └── __init__.py
│    │── README.md
│    │── .env
|    flutter/  
```