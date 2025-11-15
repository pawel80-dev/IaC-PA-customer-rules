from pa_api import api_url, pa_api_key, display_obj_addresses, create_obj_addresses
from excel_api import validate_template, create_config


def main() -> None:
    conf = create_config("customer_rules/customer_A.xlsx", sheet_name="Rules")
    print(conf[0])
    for key, value in conf[0].items():
        print(f"Creating address group:\nKEY: {key}, VALUE: {value}")
        for addr_name, addr_value in value.items():
            print(f"  Address name: {addr_name}, Address value: {addr_value}")
            create_obj_addresses(api_url, pa_api_key, addr_name, addr_value, "")

    # services = display_obj_services(api_url, pa_api_key)
    # for service in services["result"]["entry"]:
    #     print(service["@name"], service["protocol"])


if __name__ == "__main__":
    main()