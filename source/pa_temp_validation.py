from excel_api import validate_template
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("ex_file_path", type=str, help="Excel file path")
parser.add_argument("ex_sheet", type=str, help="Excel sheet name")
args = parser.parse_args()


def main() -> None:
    validate_template(args.ex_file_path, args.ex_sheet)


if __name__ == "__main__":
    main()