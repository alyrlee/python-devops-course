#!/usr/bin/env python
import click
import re


@click.command()
@click.option(
    "--phrase",
    prompt="Enter a phrase to tokenize",
    help="The phrase to tokenize into words"
)
def tokenize(phrase):
    """Tokenize a phrase into words."""
    words = re.findall(r'\b\w+\b', phrase.lower())
    click.echo(click.style("Tokenized words:", fg="green"))
    for word in words:
        click.echo(click.style(f"- {word}", fg="blue"))


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    tokenize()
