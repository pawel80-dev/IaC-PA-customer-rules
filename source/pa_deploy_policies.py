from pa_api import create_obj_services, create_obj_addresses, create_address_group
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

    for addr_group in conf["addr_groups"]:
        for addr_object in addr_group["objects"]:
            addr_group_items = []
            for addr_obj_name, addr_obj_value in addr_object.items():
                create_obj_addresses(args.pa_api_url, args.pa_api_key, addr_obj_name, addr_obj_value, "")
                addr_group_items.append(addr_obj_name)
            create_address_group(args.pa_api_url, args.pa_api_key, addr_group["name"], addr_group_items, "")


if __name__ == "__main__":
    main()