from pa_api import display_sec_policies

def main() -> None:
    policies = display_sec_policies(api_url, pa_api_key)
    # print(policies["result"]["entry"])
    # print("CURRENT POLICIES:")
    for policy in policies["result"]["entry"]:
        print(policy["@name"], policy["from"]["member"], policy["source"]["member"], 
              policy["to"]["member"], policy["destination"]["member"], 
              policy["application"]["member"], policy["service"]["member"], policy["action"])


if __name__ == "__main__":
    main()