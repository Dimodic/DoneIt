from app import models

def create_task(db, task):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db, task_id):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db, sort_by=None, order="asc"):
    mapping = {
        "title": models.Task.title,
        "status": models.Task.status,
        "created_at": models.Task.created_at,
    }
    query = db.query(models.Task)
    if sort_by in mapping:
        column = mapping[sort_by]
        query = query.order_by(column.desc() if order == "desc" else column.asc())
    return query.all()

def update_task(db, task_id, task):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db, task_id):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def get_top_tasks(db, top_n):
    return db.query(models.Task).order_by(models.Task.priority.desc()).limit(top_n).all()

def search_tasks(db, query):
    all_tasks = db.query(models.Task).all()
    query_lower = query.lower()
    return [
        task for task in all_tasks
        if query_lower in (task.title or "").lower() or query_lower in (task.description or "").lower()
    ]
