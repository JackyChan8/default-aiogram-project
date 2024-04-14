from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Test


async def create_test(test, message: Message, session: AsyncSession):
    query = (
        insert(Test)
        .values(**test)
    )
    try:
        await session.execute(query)
        await session.commit()
        await message.answer('Success Create Test', reply_markup=ReplyKeyboardRemove())
    except Exception as exc:
        await session.rollback()
        await message.answer('An error has occurred')
        await message.answer(str(exc))
