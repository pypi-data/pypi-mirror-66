import os
import click
from .apdft import merge as libmerge
from .apdft import write as libwrite
from .apdft import TIMESTAMP_FORMAT

# from .apdft import merge as libmerge

group_context_settings = {
    # infinity because default is to wrap around at about 80
    # even when the terminal width is larger
    "max_content_width": float("inf"),
    "help_option_names": ["-h", "--help"],
}


@click.group(context_settings=group_context_settings)
@click.version_option(None, "-v", "--version")
def run():
    """Another PDF Tool command-line interface.

    Operations are supported via commands, pass the command with no arguments or
    -h/--help to learn how to use it.
    """
    pass


merge_help = f"""Merge multiple PDF files together into one

    SRC can be one or more file paths pointing directly to '.pdf' files or directories
    containing '.pdf' files, seperated by a space. SRC must be absolute or relative to
    the directory where you are invoking this command.

    If SRC is a directory, then it is searched recursively until all '.pdf'
    files are found. By default this will sort all '.pdf' files alphanumerically by
    filename. Sorting only occurs at the position where the directory is specified.

        For example, imagine this is the contents of `./dir`:

        \b
        ./dir
        |-- 0
        |   `-- 3.pdf
        |-- 1.pdf
        `-- 2.pdf

        If you run `apdft merge` like this:

            `apdft merge b.pdf dir a.pdf dest.pdf`

        The result will effectively be calling it like this:

            `apdft merge b.pdf dir/1.pdf dir/2.pdf dir/0/3.pdf a.pdf dest.pdf`

    You can disable this behavior with the -d flag, and it will default to the natural
    search order defined by the OS (`os.listdir`). Note that this will still not change
    the position of the SRC argument when it is a directory.

    DEST is a file path pointing directly to the resulting '.pdf' file, or an already
    existing directory to place the resulting '.pdf' file in.

    If DEST is a directory, then the resulting '.pdf' filename will be a timestamp of
    when the file was created in the following `strftime` format {TIMESTAMP_FORMAT}.
    """


@run.command(
    "merge",
    help=merge_help,
    short_help="Merge multiple PDF files together into one",
    no_args_is_help=True,
)
@click.option(
    "-d",
    "--disable-sorting",
    "disable_sorting",
    is_flag=True,
    default=False,
    help="Disable automatic sorting by filename for directory sources",
)
@click.argument("src", nargs=-1, type=click.Path(exists=True))
@click.argument("dest", nargs=1, type=click.Path(exists=False))
def merge(src: tuple, dest: str, disable_sorting: bool):
    in_paths = [os.path.abspath(path) for path in list(src)]
    file_obj = libmerge(in_paths, disable_sorting=disable_sorting)
    write_path = os.path.abspath(dest)
    libwrite(file_obj, write_path)
    file_obj.close()


if __name__ == "__main__":
    run()
