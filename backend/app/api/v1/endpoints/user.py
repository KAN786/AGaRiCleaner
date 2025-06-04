from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas.user_schemas import UserCreate, UserUpdate

router = APIRouter()

# @router.get("/")
# def get_users(session: Session = Depends(get_session)):
    # users = session.exec(select(User)).all()
    # return users

# gets all users from a certain server

# @router.get("/{server_id}")
# def get_users(server_id: str, session: Session = Depends(get_session)):
#     users = session.exec(
#         select(User).where(
#             User.server_id == server_id
#         )
#     ).all()

#     if not users:
#         raise HTTPException(status_code = 404, detail = "Server not found")
    
#     return users

# @router.get("/{server_id}/{system_id}")
# def get_user(server_id: str, system_id: str, session: Session = Depends(get_session)):
#     user = session.get(User, server_id, system_id)

#     if not user:
#         raise HTTPException(status_code = 404, detail = "User not found")
    
#     return user

@router.post("/", response_model = User)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(
            User.system_id == user_create.system_id
    )).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"User with system_id {user_create.system_id} already exists"
        )
    
    user = User.model_validate(user_create)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.patch("/{server_id}/{system_id}", response_model=User)
def update_user(server_id: str, system_id: str, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = session.exec(
        select(User).where(
            (User.server_id == server_id) & (User.system_id == system_id)
        )
    ).one()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    update_data = user_update.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    