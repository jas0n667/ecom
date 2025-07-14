import asyncio
from uuid import uuid4
from sqlalchemy import Text, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql+asyncpg://admin:admin123@localhost:5432/mydb"

# ──────────────────────────────
class Base(AsyncAttrs, DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)


REAL_PRODUCTS = [
    # ЭЛЕКТРОНИКА
    {
        "category": "Электроника",
        "items": [
            {"name": "Смартфон Samsung Galaxy S23", "price": 399990, "image": "https://example.com/galaxy_s23.jpg"},
            {"name": "Наушники Apple AirPods Pro", "price": 119990, "image": "https://example.com/airpods_pro.jpg"},
            {"name": "Ноутбук Apple MacBook Air M2", "price": 629990, "image": "https://example.com/macbook_air.jpg"},
            {"name": "Игровая приставка Sony PlayStation 5", "price": 299990, "image": "https://example.com/ps5.jpg"},
            {"name": "Телевизор LG OLED 55\"", "price": 549990, "image": "https://example.com/lg_oled.jpg"},
            {"name": "Монитор Samsung 27\" 4K", "price": 199990, "image": "https://example.com/monitor_4k.jpg"},
            {"name": "Планшет iPad 10.2\"", "price": 229990, "image": "https://example.com/ipad.jpg"},
            {"name": "Фитнес-браслет Xiaomi Mi Band 7", "price": 24990, "image": "https://example.com/miband7.jpg"},
            {"name": "Внешний SSD Samsung T7 1TB", "price": 139990, "image": "https://example.com/samsung_t7.jpg"},
            {"name": "Гарнитура Logitech G733", "price": 89990, "image": "https://example.com/logitech_g733.jpg"},
            {"name": "Клавиатура Razer Huntsman", "price": 99990, "image": "https://example.com/razer_huntsman.jpg"},
            {"name": "Мышь Logitech MX Master 3S", "price": 64990, "image": "https://example.com/mx_master.jpg"},
            {"name": "Powerbank Baseus 20000 мАч", "price": 34990, "image": "https://example.com/baseus_powerbank.jpg"},
            {"name": "Wi-Fi роутер TP-Link Archer AX73", "price": 69990, "image": "https://example.com/ax73.jpg"},
            {"name": "Умные часы Huawei Watch GT 3", "price": 119990, "image": "https://example.com/huawei_gt3.jpg"},
            {"name": "Колонка JBL Flip 6", "price": 62990, "image": "https://example.com/jbl_flip6.jpg"},
            {"name": "SSD Kingston NV2 1TB", "price": 49990, "image": "https://example.com/kingston_nv2.jpg"},
        ]
    },
    # ОДЕЖДА
    {
        "category": "Одежда",
        "items": [
            {"name": "Футболка Nike Dri-FIT", "price": 19990, "image": "https://example.com/nike_drifit.jpg"},
            {"name": "Кроссовки Adidas Ultraboost", "price": 69990, "image": "https://example.com/adidas_ultraboost.jpg"},
            {"name": "Куртка Columbia утепленная", "price": 119990, "image": "https://example.com/columbia_jacket.jpg"},
            {"name": "Джинсы Levi’s 501", "price": 54990, "image": "https://example.com/levis_501.jpg"},
            {"name": "Спортивный костюм Puma", "price": 79990, "image": "https://example.com/puma_suit.jpg"},
            {"name": "Рубашка ZARA Slim Fit", "price": 34990, "image": "https://example.com/zara_shirt.jpg"},
            {"name": "Пуховик Uniqlo", "price": 99990, "image": "https://example.com/uniqlo_down.jpg"},
            {"name": "Сумка Eastpak", "price": 42990, "image": "https://example.com/eastpak.jpg"},
            {"name": "Кепка New Era", "price": 17990, "image": "https://example.com/newera_cap.jpg"},
            {"name": "Носки Nike (3 пары)", "price": 6990, "image": "https://example.com/nike_socks.jpg"},
            {"name": "Поясная сумка Adidas", "price": 24990, "image": "https://example.com/adidas_belt.jpg"},
            {"name": "Флисовая кофта Patagonia", "price": 89990, "image": "https://example.com/patagonia_fleece.jpg"},
            {"name": "Шапка The North Face", "price": 22990, "image": "https://example.com/tnf_hat.jpg"},
            {"name": "Рюкзак Herschel", "price": 49990, "image": "https://example.com/herschel_backpack.jpg"},
            {"name": "Очки Ray-Ban Wayfarer", "price": 89990, "image": "https://example.com/rayban.jpg"},
            {"name": "Перчатки Reusch зимние", "price": 29990, "image": "https://example.com/reusch_gloves.jpg"},
            {"name": "Плавки Speedo", "price": 17990, "image": "https://example.com/speedo_swim.jpg"},
        ]
    },
    # БЫТОВАЯ ТЕХНИКА
    {
        "category": "Бытовая техника",
        "items": [
            {"name": "Кофемашина DeLonghi Magnifica", "price": 299990, "image": "https://example.com/magnifica.jpg"},
            {"name": "Пылесос Dyson V11", "price": 449990, "image": "https://example.com/dyson_v11.jpg"},
            {"name": "Микроволновка Samsung", "price": 74990, "image": "https://example.com/microwave.jpg"},
            {"name": "Блендер Bosch", "price": 29990, "image": "https://example.com/blender.jpg"},
            {"name": "Увлажнитель воздуха Xiaomi", "price": 34990, "image": "https://example.com/humidifier.jpg"},
            {"name": "Мультиварка REDMOND", "price": 39990, "image": "https://example.com/multicooker.jpg"},
            {"name": "Холодильник LG No Frost", "price": 599990, "image": "https://example.com/lg_fridge.jpg"},
            {"name": "Стиральная машина Samsung EcoBubble", "price": 429990, "image": "https://example.com/washing.jpg"},
            {"name": "Электрочайник Tefal", "price": 17990, "image": "https://example.com/kettle.jpg"},
            {"name": "Тостер Philips", "price": 22990, "image": "https://example.com/toaster.jpg"},
            {"name": "Посудомоечная машина Bosch", "price": 359990, "image": "https://example.com/dishwasher.jpg"},
            {"name": "Фен Remington", "price": 19990, "image": "https://example.com/hairdryer.jpg"},
            {"name": "Утюг Braun", "price": 24990, "image": "https://example.com/iron.jpg"},
            {"name": "Вафельница Kitfort", "price": 15990, "image": "https://example.com/waffle.jpg"},
            {"name": "Кухонный комбайн Moulinex", "price": 79990, "image": "https://example.com/processor.jpg"},
            {"name": "Термопот Panasonic", "price": 59990, "image": "https://example.com/thermopot.jpg"},
        ]
    }
]

def generate_products():
    products = []
    for group in REAL_PRODUCTS:
        for item in group["items"]:
            products.append(
                Product(
                    name=item["name"],
                    description=f"Товар категории {group['category']}. Отличное качество и гарантия!",
                    price=item["price"],
                    image=item["image"],
                    category=group["category"]
                )
            )
    return products


async def seed():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        session.add_all(generate_products())
        await session.commit()
        print("✅  Добавлено 50 товаров с реальными названиями.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
