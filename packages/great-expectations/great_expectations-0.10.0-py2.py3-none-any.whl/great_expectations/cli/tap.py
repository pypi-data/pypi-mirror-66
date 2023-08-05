import os
import sys

import click

from great_expectations import DataContext
from great_expectations import exceptions as ge_exceptions
from great_expectations.cli.datasource import (
    get_batch_kwargs,
    select_datasource,
)
from great_expectations.cli.util import cli_message, load_expectation_suite
from great_expectations.core.usage_statistics.usage_statistics import send_usage_message
from great_expectations.data_context.util import file_relative_path
from great_expectations.util import lint_code


@click.group()
def tap():
    """Tap operations"""
    pass


@tap.command(name="new")
@click.argument("suite")
@click.argument("tap_filename")
@click.option("--datasource", default=None)
@click.option(
    "--directory",
    "-d",
    default=None,
    help="The project's great_expectations directory.",
)
def tap_new(suite, tap_filename, directory, datasource=None):
    """BETA! Create a new tap file for easy deployments."""
    cli_message("<yellow>This is a BETA feature which may change. If you have ideas please file a GitHub issue!</yellow>")
    context = _get_context(directory)
    try:
        _validate_tap_filename(tap_filename)
        context_directory = context.root_directory
        datasource = _get_datasource(context, datasource)
        suite = load_expectation_suite(context, suite)
        _, _, _, batch_kwargs = get_batch_kwargs(context, datasource.name)

        tap_filename = _write_tap_file_to_disk(
            batch_kwargs, context_directory, suite, tap_filename
        )
        cli_message(
        f"""\
<green>A new tap has been generated!</green>
To run this tap, run: <green>python {tap_filename}</green>
You can edit this script or place this code snippet in your pipeline."""
        )
        send_usage_message(
            data_context=context,
            event="cli.tap.new",
            success=True
        )
    except Exception as e:
        send_usage_message(
            data_context=context,
            event="cli.tap.new",
            success=False
        )
        raise e


def _validate_tap_filename(tap_filename):
    if not tap_filename.endswith(".py"):
        cli_message(
            "<red>Tap filename must end in .py. Please correct and re-run</red>"
        )
        exit(1)


def _get_context(directory):
    try:
        context = DataContext(directory)
    except ge_exceptions.ConfigNotFoundError as err:
        cli_message("<red>{}</red>".format(err.message))
        exit(1)
    return context


def _get_datasource(context, datasource):
    datasource = select_datasource(context, datasource_name=datasource)
    if not datasource:
        cli_message("<red>No datasources found in the context.</red>")
        sys.exit(1)
    return datasource


def _load_template():
    with open(file_relative_path(__file__, "tap_template.py"), "r") as f:
        template = f.read()
    return template


def _write_tap_file_to_disk(batch_kwargs, context_directory, suite, tap_filename):
    tap_file_path = os.path.abspath(os.path.join(context_directory, "..", tap_filename))

    template = _load_template().format(
        tap_filename, context_directory, suite.expectation_suite_name, batch_kwargs
    )
    linted_code = lint_code(template)
    with open(tap_file_path, "w") as f:
        f.write(linted_code)

    return tap_file_path
