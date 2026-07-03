import httpx
from cash_flow.models import Provider


class SanuralAPIManager:
    """Асинхронный ИТ-менеджер для интеграции с внешними API поставщиков"""

    def __init__(self, provider_id: int):
        try:
            self.provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            self.provider = None

    async def test_provider_connection(self) -> dict:
        """Метод проверки коннекта по обоим ключам Санурала"""
        if not self.provider or not self.provider.is_active:
            return {"status": "error", "message": "Поставщик не найден или отключен"}

        # Базовый URL тестового шлюза поставщика
        target_url = "https://supplier.com"

        # Настройка заголовков безопасности с хэшем из чата
        headers = {
            "Authorization": f"Bearer {self.provider.first_api_key}",
            "X-Secondary-Key": self.provider.second_api_key if self.provider.second_api_key else "",
            "Content-Type": "application/json"
        }

        # Асинхронный рантайм-запрос с жестким тайм-боксом в 10 секунд
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(target_url, headers=headers)
                if response.status_code == 200:
                    return {"status": "success", "message": "Соединение монолитно, ключи валидны"}
                return {"status": "fail", "message": f"Ошибка сервера: {response.status_code}"}
            except httpx.RequestError as exc:
                return {"status": "error", "message": f"Критический сбой сети: {exc}"}