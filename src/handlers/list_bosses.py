from aiogram import Router, F
from aiogram.types import CallbackQuery
from src.services.boss_service import BossService
from src.keyboards.boss import boss_keyboard, select_boss_keyboard
from aiogram.fsm.context import FSMContext
from src.models.boss import Boss
from .auth import send_kb_to_admin


router = Router()
boss_service = BossService()


@router.callback_query(F.data == "bosses")
async def list_bosses(callback: CallbackQuery, state: FSMContext):
    """Показать список всех боссов"""
    await callback.answer()
    await callback.message.delete()

    bosses = await boss_service.get_all_bosses()

    if not bosses:
        await callback.message.answer("Нет доступных боссов.")
        return

    await state.update_data(action="select_boss")
    await callback.message.answer("Выберите босса:", reply_markup=boss_keyboard(bosses))


@router.callback_query(F.data.startswith("boss_"))
async def show_boss_detail(callback: CallbackQuery, state: FSMContext):
    """Показать детали босса и предложить выбрать его главным"""
    await callback.answer()
    await callback.message.delete()
    
    boss_id = int(callback.data.split("_")[-1])
    await state.update_data(boss_id=boss_id)
    boss = await boss_service.get_boss_by_id(boss_id)

    if boss:
        boss_text = f"Босс: {boss.name}"
        await callback.message.answer(boss_text)
        await callback.message.answer(
            "Что вы хотите сделать?",
            reply_markup=select_boss_keyboard(boss_id)
        )
    else:
        await callback.message.answer("Босс не найден.")
        return


@router.callback_query(F.data.startswith("select_boss_"))
async def select_boss_as_main(callback: CallbackQuery, state: FSMContext):
    """Выбрать босса в качестве главного (заглушка)"""
    await callback.answer()
    
    boss_id = int(callback.data.split("_")[-1])
    
    # Заглушка для выбора главного босса
    success = await boss_service.select_boss_as_main(boss_id)
    
    if success:
        boss = await boss_service.get_boss_by_id(boss_id)
        await callback.message.answer(f"✅ Босс '{boss.name}' выбран в качестве главного!")
    else:
        await callback.message.answer("❌ Не удалось выбрать босса.")
    
    await callback.message.delete()
    await state.clear()
    await send_kb_to_admin(callback.message)
