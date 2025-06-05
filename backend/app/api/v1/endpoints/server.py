from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Server
from app.schemas.server_schemas import ServerCreate, ServerUpdate

router = APIRouter()

# get server's average honor score
@router.get("/{server_id}")
def get_average_honor_score(server_id: str, session: Session = Depends(get_session)):
    server = session.get(Server, server_id)

    if not server:
        raise HTTPException(status_code = 404, details = "Server not found")

    return server



# create server
@router.post("/", response_model = Server)
def create_server(server_create: ServerCreate, session: Session = Depends(get_session)):
    existing_server = session.exec(
        select(Server).where(
            Server.id == id
    )).first()

    if existing_server:
        raise HTTPException(status_code = 400, detail=f"Server with id {server_create.id} already exists")

    server = Server.model_validate(server_create)

    session.add(server)
    session.commit()
    session.refresh(server)
    return server
    



# update (post) average honor score (or other things as well perhaps)

# @router.patch("/{server_id}", response_model = Server)
# def update_server(id: str, server_update: ServerUpdate, session: Session = Depends(get_session)):
#     server = session.exec(
#         select(Server).where(
#             Server.id == id
#     )).one()

#     if not server:
#         raise HTTPException(status_code = 404, detail = "Server not found")

#     update_server = server_update.model_dump(exclude_unset=True)
#     for key, value in update_server.items():
#         setattr(server, key, value)

#     session.add(server)
#     session.commit()
#     session.refresh(server)
#     return server

