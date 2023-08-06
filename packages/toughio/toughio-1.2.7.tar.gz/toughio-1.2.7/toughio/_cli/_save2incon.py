__all__ = [
    "save2incon",
]


def save2incon(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)


def _get_parser():
    import argparse

    # Initialize parser
    parser = argparse.ArgumentParser(
        description=("Convert a SAVE file to an INCON file."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Input file

    return parser
