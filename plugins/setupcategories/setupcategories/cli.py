import click
from misago.cli import cli
from misago.categories.models import Category, CategoryType
from misago.utils.async_context import uses_database


@cli.add_command
@click.command(short_help="Setups categories on demo site")
@uses_database
async def createdemocategories():
    click.echo("Creating categories")

    await Category.query.filter(type=CategoryType.THREADS).delete()

    first_category = await Category.create(
        "First category",
        color=None,
        icon=None,
        parent=None,
        left=1,
        right=4,
        depth=0,
    )

    await Category.create(
        "Child category",
        color=None,
        icon=None,
        parent=first_category,
        left=2,
        right=3,
        depth=1,
    )

    await Category.create(
        "Sibling category",
        color=None,
        icon=None,
        parent=None,
        left=5,
        right=6,
        depth=0,
    )