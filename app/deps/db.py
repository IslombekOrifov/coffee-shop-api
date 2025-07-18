from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]