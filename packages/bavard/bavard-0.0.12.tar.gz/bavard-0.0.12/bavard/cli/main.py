import click

from bavard.cli.qa import qa
from bavard.cli.text_summarization import text_summarization


@click.group()
def cli():
    pass


cli.add_command(qa)
cli.add_command(text_summarization)


def main():
    cli()


if __name__ == '__main__':
    cli()
