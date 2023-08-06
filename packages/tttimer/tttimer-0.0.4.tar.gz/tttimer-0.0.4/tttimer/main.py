"""Main function."""
from fire import Fire
from tttimer.cli_handler import CliHandler


def main():
    """Init function."""
    Fire(CliHandler)


if __name__ == '__main__':
    main()
