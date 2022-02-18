import random

from faker import Faker

from misago.richtext import RichText, RichTextBlock, get_block_id

from .sentences import Sentences


sentences = Sentences(max_length=200)


def create_fake_rich_text(fake: Faker, depth: int = 0) -> RichText:
    rich_text: RichText = []

    dice_roll = random.randint(0, 100)
    if dice_roll > 95:
        # 5% of rich texts are long post text
        return create_fake_long_post_rich_text(fake, depth)
    
    if dice_roll > 60:
        # 40% of rich texts are medium post text
        return create_fake_medium_post_rich_text(fake, depth)
    
    rich_text: RichText = []
    for _ in range(random.randint(1, 2)):
        rich_text.append(create_fake_rich_text_sentence(fake))

    return rich_text


IMAGE = 0
QUOTE = 1
LIST = 3
HEADER = 4


def create_fake_long_post_rich_text(fake: Faker, depth: int) -> RichText:
    rich_text: RichText = []

    for _ in range(random.randint(1, 5)):
        dice_roll = random.randint(0, 100)
        if dice_roll > 90:
            # 40% chance for sentences
            rich_text.append(create_fake_rich_text_paragraph())
        else:
            if depth == 0:
                special_content = random.choice([IMAGE, QUOTE, LIST, HEADER])
            else:
                special_content = random.choice([IMAGE, LIST, HEADER])

            if special_content == IMAGE:
                rich_text.append(create_fake_rich_text_image())
            if special_content == QUOTE:
                rich_text.append(create_fake_rich_text_quote(fake, depth + 1))
            if special_content == HEADER:
                rich_text.append(create_fake_rich_text_header(fake))
            if special_content == LIST:
                rich_text.append(create_fake_rich_text_list())

    return rich_text


def create_fake_medium_post_rich_text(fake: Faker, depth: int) -> RichText:
    rich_text: RichText = []

    if random.randint(0, 10) > 6:
        # 40% chance for text before image
        rich_text.append(create_fake_rich_text_sentence(fake))

    if depth == 0:
        special_content = random.choice([IMAGE, QUOTE, LIST, HEADER])
    else:
        special_content = random.choice([IMAGE, LIST, HEADER])

    if special_content == IMAGE:
        rich_text.append(create_fake_rich_text_image())
    if special_content == QUOTE:
        rich_text.append(create_fake_rich_text_quote(fake, depth + 1))
    if special_content == HEADER:
        rich_text.append(create_fake_rich_text_header(fake))
    if special_content == LIST:
        rich_text.append(create_fake_rich_text_list())

    if random.randint(0, 10) > 6:
        # 40% chance for text after image
        rich_text.append(create_fake_rich_text_sentence(fake))

    return rich_text


def create_fake_rich_text_sentence(fake: Faker) -> dict:
    if random.choice([True, False]):
        fake_text = fake.sentence(random.randint(3, 10))
    else:
        fake_text = sentences.get_random_sentence()
    
    return {
        "id": get_block_id(),
        "type": "p",
        "text": fake_text,
    }


def create_fake_rich_text_image() -> dict:
    width = random.randint(1, 10) * 100
    height = random.randint(1, 10) * 100
    
    return {
        "id": get_block_id(),
        "type": "p",
        "text": f'<img src="http://placekitten.com/{width}/{height}" />',
    }


def create_fake_rich_text_header(fake: Faker) -> RichTextBlock:
    if random.choice([True, False]):
        fake_text = fake.sentence(random.randint(2, 10))
    else:
        fake_text = sentences.get_random_sentence()

    return {
        "id": get_block_id(),
        "type": "h%s" % random.randint(1, 6),
        "text": fake_text,
    }


def create_fake_rich_text_paragraph() -> RichTextBlock:
    text = " ".join(sentences.get_random_sentences(random.randint(1, 4)))
    return {
        "id": get_block_id(),
        "type": "p",
        "text": text,
    }


def create_fake_rich_text_quote(fake: Faker, depth: int = 0) -> RichTextBlock:
    return {
        "id": get_block_id(),
        "type": "quote",
        "author": None,
        "post": None,
        "children": create_fake_rich_text(fake, depth),
    }


def create_fake_rich_text_list(depth: int = 0) -> RichTextBlock:
    children = []
    for _ in range(random.randint(2, 10)):
        if depth == 0 and random.randint(1, 10) == 10:
            children.append(
                {
                    "id": get_block_id(),
                    "type": "li",
                    "children": [create_fake_rich_text_list(depth + 1)],
                }
            )
        else:
            children.append(
                {
                    "id": get_block_id(),
                    "type": "li",
                    "children": [
                        {
                            "id": get_block_id(),
                            "type": "f",
                            "text": sentences.get_random_sentence(),
                        }
                    ],
                }
            )

    return {
        "id": get_block_id(),
        "type": "list",
        "ordered": random.choice((True, False)),
        "children": children,
    }
