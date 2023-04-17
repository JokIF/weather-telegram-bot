import click
import logging


@click.group()
@click.option('-d', '--debug', 'debug', is_flag=True, default=False)
def cli(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    import main_bot.init as init
    init.setup()


@cli.command()
def start():
    from main_bot.init import executor
    executor.start_polling()
