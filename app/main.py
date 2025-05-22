from enum import Enum
from typing import List

from fastapi import FastAPI, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
from .services import task_service


class TaskSortField(str, Enum):
    id = "id"
    title = "title"
    completed = "completed"
    priority = "priority"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DoneIt API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks", response_model=schemas.TaskRead, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task)


@app.get(
    "/tasks",
    response_model=List[schemas.TaskRead],
    summary="Получить список задач с пагинацией, сортировкой",
)
def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    sort_by: TaskSortField = Query(TaskSortField.id),
    sort_order: SortOrder = Query(SortOrder.asc),
    db: Session = Depends(get_db),
):
    return task_service.get_tasks(
        db,
        skip=skip,
        limit=limit,
        sort_by=sort_by.value,
        sort_order=sort_order.value,
    )


@app.get("/tasks/search", response_model=List[schemas.TaskRead])
def search_tasks(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    return task_service.search_tasks(db, query)


@app.get("/tasks/top", response_model=List[schemas.TaskRead])
def top_tasks(
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    return task_service.get_top_tasks(db, limit)


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def read_task(
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    db_task = task_service.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int = Path(..., ge=1),
    task: schemas.TaskUpdate = ...,
    db: Session = Depends(get_db),
):
    db_task = task_service.update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    if not task_service.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
