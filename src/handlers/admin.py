from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.filters import IsAdmin
from utils.keyboards.inline import admin as admin_inline_keyboard
from utils.keyboards.reply import admin as admin_reply_keyboard


router = Router(name='admin')


@router.message(IsAdmin(), Command('start'))
async def admin_start_command(message: Message, state: FSMContext):
    # buttons = await admin_inline_keyboard.start_inline_keyboard()
    buttons = await admin_reply_keyboard.start_reply_keyboard()
    await message.answer('Hello Admin', reply_markup=buttons)


@router.callback_query(IsAdmin(), F.data == 'is_admin')
async def admin_is_admin_callback_query(callback: CallbackQuery):
    await callback.message.answer('Yes')


@router.message(~IsAdmin(), F.text.lower() == 'is admin')
async def admin_is_admin_command_reply(message: Message):
    await message.answer('Yes')
