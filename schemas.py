# schemas.py
# GPT3

from pydantic import BaseModel

class Task(BaseModel):
    title: str
    priority: str
    due: str



# from pydantic import BaseModel

# class Task(BaseModel):
#     title: str
#     due_date: str
#     priority: int
