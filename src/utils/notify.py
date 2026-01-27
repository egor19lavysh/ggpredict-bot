from aiogram import Bot


ADMIN_IDS = [8037595378]
MESSAGE_NEW_PREDICTION = """
Поздравляю! Пользователь {tag} выиграл {status} приз🎉
Скорее свяжитесь с ним чтобы уточнить детали вручения!"
"""

async def notify_admins(bot: Bot, user_id: int, status: str) -> None:
        """
        Оповещение всех админов
        
        Args:
            message: Текст сообщения
        """
        user = await bot.get_chat(user_id)
        tag = user.username
        message = MESSAGE_NEW_PREDICTION.format(tag="@" + tag if tag else f"с id {user_id}", status=status)

        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(chat_id=admin_id, text=message)
            except Exception as e:
                print(f"Failed to send notification to admin {admin_id}: {e}")