from sqlalchemy.orm import declarative_base
import sqlalchemy.ext.asyncio

# postgress is username and 12345678  is password

db_url= "postgresql+asyncpg://postgres:12345678@localhost:5432/Seed"
Base = declarative_base()
engine= sqlalchemy.ext.asyncio.create_async_engine(db_url)

AsyncSessionLocal = sqlalchemy.ext.asyncio.async_sessionmaker(
    bind=engine,
    class_=sqlalchemy.ext.asyncio.AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as db:
           yield db
         

async def init_models():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )