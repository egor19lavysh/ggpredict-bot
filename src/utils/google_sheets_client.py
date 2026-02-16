import os
import asyncio
from datetime import datetime
from typing import Optional
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from gspread import service_account
from gspread.exceptions import WorksheetNotFound
from logging import getLogger

logger = getLogger('GoogleSheetService')


class GoogleSheetsClient:
    """
    Google Sheets клиент для логирования попаданий по боссам
    """
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        """
        Инициализация Google Sheets клиента
        
        Args:
            credentials_path: Путь к JSON файлу с учетными данными сервиса
            spreadsheet_id: ID таблицы Google Sheets
        """
        self.google_service = service_account(filename=credentials_path)
        self.sheet = self.google_service.open_by_key(key=spreadsheet_id)
    
    async def hit(self, user_info: list, boss_name: str) -> bool:
        """
        Добавляет информацию о попадании в лист босса (асинхронный метод)
        
        Args:
            user_info: Список строк с информацией пользователя (данные для добавления)
            boss_name: Название листа (имя босса)
            
        Returns:
            True если успешно добавлено, False при ошибке
        """
        return await asyncio.to_thread(self._hit_sync, user_info, boss_name)
    
    def _hit_sync(self, user_info: list, boss_name: str) -> bool:
        """
        Синхронная реализация добавления данных (вспомогательный метод)
        
        Args:
            user_info: Список строк с информацией пользователя (данные для добавления)
            boss_name: Название листа (имя босса)
            
        Returns:
            True если успешно добавлено, False при ошибке
        """
        try:
            # Проверяем, существует ли лист с названием босса
            try:
                worksheet = self.sheet.worksheet(boss_name)
                print(f"✅ Лист '{boss_name}' найден")
            except WorksheetNotFound:
                # Если листа нет, создаем новый
                worksheet = self.sheet.add_worksheet(title=boss_name, rows=1000, cols=20)
                print(f"✅ Новый лист '{boss_name}' создан")
                
                # Добавляем заголовки в новый лист
                headers = ['ID', 'Тег', 'Дата участия']
                worksheet.insert_row(headers, index=1)
                print(f"✅ Заголовки добавлены в лист '{boss_name}'")
            
            # Добавляем строку данных в лист
            worksheet.append_row(user_info)
            print(f"✅ Данные добавлены в лист '{boss_name}': {user_info}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при добавлении данных: {e}")
            return False