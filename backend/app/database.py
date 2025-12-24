from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Use the ASYNC driver
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# 2. Create Async Engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Needed for SQLite
    echo=True # Helps debug SQL queries
)

# 3. Create Async Session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# 4. Dependency with proper Error Handling
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Only commit if no error occurred
            await session.commit()
        except Exception:
            # Rollback on error
            await session.rollback()
            raise
        finally:
            # Close session
            await session.close()