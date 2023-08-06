import argparse


def cli():
    parser = argparse.ArgumentParser(prog="smn")
    subparsers = parser.add_subparsers(
        title="Sub commands for smn",
        metavar="command"
    )

    # new sub command
    new_parser = subparsers.add_parser(
        'new',
        help="new markdown files"
    )
    new_parser.set_defaults(handle=handle_new)

    # parse args
    smn = 'smn'
    args = parser.parse_args()
    if hasattr(args, 'handle'):
        args.handle(smn, args)
    else:
        parser.print_help()


def handle_new(smn, args):
    print('smn: %s, args: %s' % (smn, args))

    cmd = ['smn', 'new']
    print('cmd: ', cmd)


if __name__ == '__main__':
    cli()

