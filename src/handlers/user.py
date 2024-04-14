from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from sqlalchemy.ext.asyncio import AsyncSession

from utils.filters import IsAdmin
from utils.states.user import TestStates
from services.services import create_test
from utils.keyboards.reply import user as user_reply_keyboard
from utils.keyboards.inline import user as user_inline_keyboard


router = Router(name='users')


@router.message(~IsAdmin(), Command('start'))
async def user_start_command(message: Message, state: FSMContext) -> None:
    # buttons = await user_inline_keyboard.start_inline_keyboard()
    buttons = await user_reply_keyboard.start_reply_keyboard()
    await message.answer('Hello User', reply_markup=buttons)


@router.callback_query(~IsAdmin(), F.data == 'is_user')
async def user_is_user_callback_query(callback: CallbackQuery) -> None:
    await callback.message.answer('Yes')


@router.message(~IsAdmin(), F.text.lower() == 'is user')
async def user_is_user_command_reply(message: Message) -> None:
    await message.answer('Yes')


# Test
@router.message(~IsAdmin(), Command('test-create'))
async def user_test_create_command(message: Message, state: FSMContext) -> None:
    await state.set_state(TestStates.text)
    await message.answer(
        text='Write the text of the test',
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(~IsAdmin(), TestStates.text)
async def test_create_name(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await state.set_state(TestStates.is_test)

    buttons = await user_reply_keyboard.test_create_keyboard()
    await message.answer(text='Is Test?', reply_markup=buttons)


@router.message(~IsAdmin(), TestStates.is_test, F.text.lower() == 'yes')
async def test_create_is_test(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(is_test=True)
    data = await state.get_data()
    await state.clear()

    await create_test(data, message, session)


@router.message(~IsAdmin(), TestStates.is_test, F.text.lower() == 'no')
async def test_create_is_test(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(is_test=False)
    data = await state.get_data()
    await state.clear()

    await create_test(data, message, session)
