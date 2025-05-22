from app import crud, schemas
from app.database import SessionLocal


def test_priority_validator_positive_path():
    obj = schemas.TaskBase(title="OK", priority=7)
    assert obj.priority == 7  # валидно, исключения нет


def test_crud_get_tasks_direct():
    with SessionLocal() as db:
        task = crud.create_task(db, schemas.TaskCreate(title="Direct CRUD"))
        tasks = crud.get_tasks(db)

    assert any(t.id == task.id for t in tasks)

def test_priority_validator_none_branch():
    result = schemas.TaskBase.priority_must_be_non_negative(None)
    assert result is None