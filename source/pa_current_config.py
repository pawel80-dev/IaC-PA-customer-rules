from pa_api import display_sec_policies
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pa_api_url", type=str, help="PA API URL")
parser.add_argument("pa_api_key", type=str, help="PA API key")
args = parser.parse_args()


def main() -> None:
    policies = display_sec_policies(args.pa_api_url, args.pa_api_key)
    for policy in policies["result"]["entry"]:
        print(policy["@name"], policy["from"]["member"], policy["source"]["member"], 
              policy["to"]["member"], policy["destination"]["member"], 
              policy["application"]["member"], policy["service"]["member"], policy["action"])


if __name__ == "__main__":
    main()