import random
from datetime import timedelta
from typing import AsyncGenerator, Union

from faker import Faker
from sqlalchemy import select

from misago.categories.get import get_all_categories
from misago.database import database
from misago.tables import users
from misago.threads.models import Post, Thread
from misago.users.models import User
from misago.utils import timezone

from .randomrow import get_random_thread
from .shortcuts import get_random_poster
from .threads import create_fake_post, create_fake_thread
from .users import create_fake_user


async def create_fake_forum_history(
    fake: Faker, days: int, daily_actions: int
) -> AsyncGenerator[Union[Post, Thread, User], None]:
    await move_existing_users_to_past(days)

    categories = await get_all_categories()
    if not categories:
        raise ValueError("No categories have been found.")

    popular_threads = []

    start_date = timezone.now()
    for days_ago in reversed(range(days)):
        for action_date in get_day_actions_dates(start_date, days_ago, daily_actions):
            action = random.randint(0, 100)
            if action >= 80:
                yield await create_fake_user(fake, joined_at=action_date)
            elif action > 60:
                category = random.choice(categories)
                starter, starter_name = await get_random_poster(fake)

                thread = await create_fake_thread(
                    fake,
                    category,
                    starter=starter,
                    starter_name=starter_name,
                    started_at=action_date,
                )

                if random.randint(0, 100) > 95:
                    # Thread has 5% chance to be popular
                    popular_threads.append(thread)

                yield thread
            else:
                if random.randint(0, 100) > 60 and popular_threads:
                    # There's 40% chance new reply will be in a popular thread
                    thread = random.choice(popular_threads)
                else:
                    thread = await get_random_thread()
                    if not thread:
                        continue

                poster, poster_name = await get_random_poster(fake)

                post = await create_fake_post(
                    fake,
                    thread,
                    poster=poster,
                    poster_name=poster_name,
                    posted_at=action_date,
                )

                await thread.update(last_post=post, increment_replies=True)

                yield post


async def move_existing_users_to_past(days: int):
    query = select([users.c.id, users.c.joined_at])
    for row in await database.fetch_all(query):
        past_joined_at = row["joined_at"] - timedelta(days=days)
        await database.execute(
            users.update(None).values(joined_at=past_joined_at).where(users.c.id == row["id"])
        )


def get_day_actions_dates(start_date, days_ago, daily_actions):
    actions = []
    for _ in range(random.randint(0, daily_actions)):
        action_date = start_date - timedelta(
            days=days_ago, seconds=random.randint(1, 3600 * 24) - 1
        )
        actions.append(action_date)
    return sorted(actions)
