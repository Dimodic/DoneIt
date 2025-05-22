from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)


def get_tasks(db: Session) -> list[models.Task]:
    return db.execute(select(models.Task)).scalars().all()


def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate) -> models.Task | None:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> models.Task | None:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task
