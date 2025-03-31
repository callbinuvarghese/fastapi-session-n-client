from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
from uuid import UUID, uuid4

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

class SessionData(BaseModel):
    username: str
    messages: list[str] = []

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,  # Important to allow session cookies
    allow_methods=["*"],     # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],     # Allow all headers
)

@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):
    logger.debug("Creating session")
    session = uuid4()
    data = SessionData(username=name, messages=[])

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    logger.debug(f"created session for {name} with {session}")
    return f"created session for {name} with {session}"


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    logger.debug("whoami called")
    return session_data

@app.post("/add_message", dependencies=[Depends(cookie)])
async def add_message(
    message: str = Body(..., embed=True),
    session_id: UUID = Depends(cookie),
    session_data: SessionData = Depends(verifier)
):
    # Append message to session data
    logger.debug(f"Adding meesage with session_id:{session_id}")
    session_data.messages.append(message)
    await backend.update(session_id, session_data)
    return {"message": "Message added", "all_messages": session_data.messages}


@app.get("/get_messages")
async def get_messages(
    session_id: UUID = Depends(cookie),
    session_data: SessionData = Depends(verifier),
):
    logger.debug(f"Get message with session_id:{session_id}")
    data = await backend.read(session_id)
    messages = getattr(data, "messages", [])
    logger.debug(f"Get message with session_id:{session_id}; len:{len(messages)}")
    return messages

@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    logger.debug(f"Delete session with session_id:{session_id}")
    return "deleted session"