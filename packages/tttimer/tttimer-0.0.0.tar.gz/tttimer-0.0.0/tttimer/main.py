"""Main function."""
import argparse


def cli():
    """CLI function to parse CLI arguments.

    Returns:
        args: dict -- CLI arguments

    """
    parser = argparse.ArgumentParser(description='CVM crawler CLI')
    # name
    parser.add_argument('name', type=str, nargs='?', default='World',
                        help='CVM document id to start scrapping data.')
    # bold
    parser.add_argument('--bold', '-b', action='store_true',
                        help='CVM document id to start scrapping data.')
    args = parser.parse_args()
    return args


def main():
    """Create Main function."""
    args = cli()
    if args.bold:
        msg = "Hello **{}**"
    else:
        msg = "Hello {}"

    print(msg.format(args.name))


if __name__ == '__main__':
    main()
