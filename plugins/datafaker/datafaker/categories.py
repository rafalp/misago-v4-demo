import random
from typing import Optional

from faker import Faker

from misago.categories.get import get_all_categories
from misago.categories.models import Category
from misago.categories.tree import insert_category


ICONS = (
    "fas fa-audio-description",
    "fas fa-closed-captioning",
    "far fa-closed-captioning",
    "fas fa-question-circle",
    "far fa-question-circle",
    "fas fa-asterisk",
    "fas fa-at",
    "fas fa-atom",
    "fas fa-ban",
    "fas fa-bed",
    "fas fa-beer",
    "fas fa-bicycle",
    "fas fa-biking",
    "fas fa-biohazard",
    "fas fa-bold",
    "fas fa-brush",
    "fab fa-buffer",
    "fas fa-bus",
    "fas fa-bus-alt",
    "fas fa-capsules",
    "fas fa-carrot",
    "fas fa-car",
    "fas fa-car-alt",
    "fas fa-car-battery",
    "fas fa-car-side",
    "fas fa-chair",
    "fas fa-chart-bar",
    "fas fa-chart-line",
    "fas fa-chart-pie",
    "fas fa-check-circle",
    "fas fa-check-circle",
    "far fa-clock",
    "fas fa-clock",
    "fas fa-cookie",
    "fas fa-cookie-bite",
    "far fa-credit-card",
    "fas fa-credit-card",
    "fas fa-cube",
    "fas fa-database",
    "fas fa-desktop",
    "fas fa-dice",
    "fas fa-directions",
)


async def create_fake_category(
    fake: Faker, *, parent: Optional[Category] = None
) -> Category:
    all_categories = await get_all_categories()
    new_category = await Category.create(
        name=get_fake_category_name(fake),
        color=fake.color(luminosity="bright"),
        icon=random.choice(ICONS),
        parent=parent,
    )
    category, _ = await insert_category(all_categories, new_category, parent)
    return category


def get_fake_category_name(fake: Faker) -> str:
    return fake.street_name()
