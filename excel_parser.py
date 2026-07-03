import openpyxl
from decimal import Decimal
from cash_flow.models import Product, Provider


class SanuralExcelParser:
    """Сервисный скрипт для автоматического парсинга прайс-листов сантехники"""

    def __init__(self, file_path: str, provider_id: int):
        self.file_path = file_path
        try:
            self.provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            self.provider = None

    def sync_prices_with_db(self) -> dict:
        """Метод парсинга Excel и бесшовного обновления базы данных"""
        if not self.provider:
            return {"status": "error", "message": "Поставщик не заведен в систему"}

        try:
            # Хладнокровно загружаем Excel-книгу в режиме чтения данных (data_only=True)
            workbook = openpyxl.load_workbook(self.file_path, data_only=True)
            sheet = workbook.active  # Берём первый активный лист таблицы

            updated_count = 0

            # Начинаем сканировать строчки со 2-й (пропуская шапку таблицы)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Если строка пустая — пропускаем таск
                if not row or not row[0]:
                    continue

                sku = str(row[0]).strip()  # Колонка A: Артикул товара
                title = str(row[1]).strip()  # Колонка B: Наименование
                category = str(row[2]).strip()  # Колонка C: Категория
                purchase_price = Decimal(str(row[3]))  # Колонка D: Закупочная цена
                stock = int(row[4])  # Колонка E: Остаток на складе

                # Твой личный бизнес-хак: автоматическая наценка 25% на розницу!
                retail_price = purchase_price * Decimal('1.25')

                # Метод update_or_create: если товара нет — создаст, если есть — обновит лог цены!
                product, created = Product.objects.update_or_create(
                    sku=sku,
                    defaults={
                        'provider': self.provider,
                        'title': title,
                        'category': category,
                        'purchase_price': purchase_price,
                        'retail_price': retail_price,
                        'stock': stock,
                    }
                )
                updated_count += 1

            return {"status": "success", "message": f"Синхронизация завершена. Обновлено товаров: {updated_count}"}

        except Exception as exc:
            return {"status": "error", "message": f"Критический сбой парсера: {exc}"}