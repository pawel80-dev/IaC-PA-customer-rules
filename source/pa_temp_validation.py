from excel_api import validate_template


def main() -> None:
    validate_template("customer_rules/customer_A.xlsx", sheet_name="Rules")


if __name__ == "__main__":
    main()