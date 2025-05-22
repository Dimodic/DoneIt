from sqlalchemy import select, desc, or_, func
from sqlalchemy.orm import Session

from app import models, schemas, crud


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    return crud.create_task(db, task)


def get_task(db: Session, task_id: int) -> models.Task | None:
    return crud.get_task(db, task_id)


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "id",
    sort_order: str = "asc",
) -> list[models.Task]:
    stmt = select(models.Task)

    column = getattr(models.Task, sort_by, None)
    if column is not None:
        stmt = stmt.order_by(desc(column) if sort_order == "desc" else column)

    stmt = stmt.offset(skip).limit(limit)

    return db.execute(stmt).scalars().all()


def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate) -> models.Task | None:
    return crud.update_task(db, task_id, task_data)


def delete_task(db: Session, task_id: int) -> models.Task | None:
    return crud.delete_task(db, task_id)


def search_tasks(db: Session, query: str) -> list[models.Task]:
    pattern = f"%{query.lower()}%"
    stmt = select(models.Task).where(
        or_(
            func.lower(models.Task.title).like(pattern),
            func.lower(models.Task.description).like(pattern),
        )
    )
    return db.execute(stmt).scalars().all()


def get_top_tasks(db: Session, limit: int = 10) -> list[models.Task]:
    stmt = select(models.Task).order_by(desc(models.Task.priority)).limit(limit)
    return db.execute(stmt).scalars().all()
