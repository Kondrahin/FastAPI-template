"""CRUD implementation."""

from typing import Any

from sqlalchemy import delete, insert, inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class CRUD:
    """CRUD operations for models."""

    def __init__(self, session: AsyncSession, cls_model: Any):
        self._session = session
        self._cls_model = cls_model

    async def create(self, *, model_data: dict[str, Any]) -> Any:
        """Create object."""
        query = insert(self._cls_model).values(**model_data)

        res = await self._session.execute(query)
        return res.inserted_primary_key  # type: ignore # pragma:nocover

    async def update(
        self,
        *,
        pkey_val: Any,
        model_data: dict[str, Any],
    ) -> None:
        """Update object by primary key."""
        pkey_column = inspect(self._cls_model).primary_key[0]
        query = (
            update(self._cls_model)
            .where(pkey_column == pkey_val)
            .values(**model_data)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(query)

    async def delete(self, *, pkey_val: Any) -> None:
        """Delete object by primary key."""
        pkey_column = inspect(self._cls_model).primary_key[0]
        query = (
            delete(self._cls_model)
            .where(pkey_column == pkey_val)
            .execution_options(synchronize_session="fetch")
        )

        await self._session.execute(query)

    async def get(self, *, pkey_val: Any) -> Any:
        """Get object by primary key."""
        pkey_column = inspect(self._cls_model).primary_key[0]
        query = (
            select(self._cls_model)
            .where(pkey_column == pkey_val)
            .execution_options(synchronize_session="fetch")
        )

        rows = await self._session.execute(query)
        return rows.scalars().unique().one()

    async def all(
        self,
    ) -> Any:
        """Get all objects by db model."""
        query = select(self._cls_model)

        rows = await self._session.execute(query)
        return rows.scalars().unique().all()
