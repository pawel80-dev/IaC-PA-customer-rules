from pa_api import create_obj_services
from excel_api import create_config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pa_api_url", type=str, help="PA API URL")
parser.add_argument("pa_api_key", type=str, help="PA API key")
parser.add_argument("ex_file_path", type=str, help="Excel file path")
parser.add_argument("ex_sheet", type=str, help="Excel sheet name")
args = parser.parse_args()


def main() -> None:
    conf = create_config(args.ex_file_path, sheet_name=args.ex_sheet)
    for service in conf["services"]:
        create_obj_services(args.pa_api_url, args.pa_api_key, service["name"], service["protocol"], service["port"], "")

    # services = display_obj_services(api_url, pa_api_key)
    # for service in services["result"]["entry"]:
    #     print(service["@name"], service["protocol"])


if __name__ == "__main__":
    main()