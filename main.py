from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app import models, schemas, crud, database


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    yield


app = FastAPI(lifespan=lifespan)


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)) -> schemas.TaskOut:
    return crud.create_task(db, task)


@app.get("/tasks/", response_model=list[schemas.TaskOut])
def read_tasks(
        sort_by: str = Query(None),
        order: str = Query("asc"),
        db: Session = Depends(get_db)
) -> list[schemas.TaskOut]:
    return crud.get_tasks(db, sort_by, order)


@app.get("/tasks/top", response_model=list[schemas.TaskOut])
def get_top_tasks(
        top_n: int = Query(5),
        db: Session = Depends(get_db)
) -> list[schemas.TaskOut]:
    return crud.get_top_tasks(db, top_n)


@app.get("/tasks/search", response_model=list[schemas.TaskOut])
def search_tasks(query: str, db: Session = Depends(get_db)) -> list[schemas.TaskOut]:
    return crud.search_tasks(db, query)


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)) -> schemas.TaskOut:
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
        task_id: int,
        task: schemas.TaskUpdate,
        db: Session = Depends(get_db)
) -> schemas.TaskOut:
    updated_task = crud.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.delete("/tasks/{task_id}", response_model=schemas.TaskOut)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> schemas.TaskOut:
    deleted_task = crud.delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
