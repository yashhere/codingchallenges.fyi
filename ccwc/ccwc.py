import argparse
from os import path
import sys


def count_bytes(data):
    return len(data)


def count_lines(data):
    lines = data.splitlines()
    return len(lines)


def count_words(data):
    total_words = 0
    lines = data.splitlines()
    for line in lines:
        words = line.split()
        total_words += len(words)
    return total_words


def count_characters(data):
    total_chars = 0
    for _ in data.decode():
        total_chars += 1
    return total_chars


def parse_arguments(args):
    arg_parser = argparse.ArgumentParser(
        prog="ccwc",
        description="word, line, character, and byte count",
        usage="wc [-clmw] [file]",
    )
    opts = arg_parser.add_mutually_exclusive_group()
    opts.add_argument("-c", action="store_true", default=False)
    opts.add_argument("-l", action="store_true", default=False)
    opts.add_argument("-w", action="store_true", default=False)
    opts.add_argument("-m", action="store_true", default=False)
    arg_parser.add_argument(
        "input_file", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    return arg_parser.parse_args(args)


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])

    is_stdin = False
    stdin_output_string = output_string = ""
    try:
        if args.input_file and args.input_file.name == "<stdin>":
            data = sys.stdin.read().encode("utf-8")
            is_stdin = True
        else:
            try:
                stdin_output_string = f"{args.input_file.name}"
                with open(args.input_file.name, "rb") as f:
                    data = f.read()
            except FileNotFoundError:
                print(f"File: {path.basename(args.input_file.name)} not found.")
                sys.exit(1)

        if args.c:
            result = count_bytes(data)
            output_string = f"  {result}"
        elif args.m:
            result = count_characters(data)
            output_string = f"  {result}"
        elif args.w:
            result = count_words(data)
            output_string = f"  {result}"
        elif args.l:
            result = count_lines(data)
            output_string = f"  {result}"
        else:
            bytes = count_bytes(data)
            words = count_words(data)
            lines = count_lines(data)
            output_string = f"    {lines}   {words}  {bytes}"

        print(f"{output_string} {stdin_output_string if not is_stdin else ''}")
    except OSError:
        print("OS error occurred")
