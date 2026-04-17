from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'app.db'}"

ALLOWED_POLICY_COUNTRIES = {
    "Азербайджан",
    "Таджикистан",
    "Узбекистан",
    "Молдова",
    "Украина",
    "Киргизия",
    "Казахстан",
    "Армения",
}

PURPOSES = [
    "трудовая деятельность",
    "учеба",
    "частная",
    "деловая",
    "туризм",
    "иная",
]
