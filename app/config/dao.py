from sqlalchemy import select


class BaseDAO:
    model = None

    @classmethod
    async def get_by_id(cls, db, obj_id: int):
        q = await db.execute(select(cls.model).where(cls.model.id == obj_id))
        return q.scalar_one_or_none()

    @classmethod
    async def get_all(cls, db,):
        q = await db.execute(select(cls.model))
        return q.scalars().all()

    @classmethod
    async def get_one_by_filters(cls, db, **filters):
        stmt = select(cls.model)
        for attr, value in filters.items():
            stmt = stmt.where(getattr(cls.model, attr) == value)
        q = await db.execute(stmt)
        return q.scalar_one_or_none()

    @classmethod
    async def get_all_by_filters(cls, db, **filters):
        stmt = select(cls.model)
        for attr, value in filters.items():
            stmt = stmt.where(getattr(cls.model, attr) == value)
        q = await db.execute(stmt)
        return q.scalars().all()
