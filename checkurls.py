import sys
import re

def delete_unwanted_links(urls):
    # Regular expression to match URLs starting with specified domains or containing the word "google"
    pattern_delete = r"^(?:https?://(?:www\.)?(?:google\.(?:es|com)|accounts\.google\.com|translate\.google\.com|support\.google\.com|policies\.google\.com|google)|http://www\.translate\.google\.es)(?:$|/|\?)"

    # Regular expression to match URLs without specified parameters
    pattern_params = r"^https?://.*?(?:(?:\?next=|&?url=|&?target=|&?rurl=|&?dest=|&?destination=|&?redir=|&?redirect_uri=|&?redirect_url=|&?redirect=|/cgi-bin/redirect.cgi\?|/out/|/out\?|&?view=|&?login?to=|&?image_url=|&?go=|&?return=|&?returnTo=|&?return_to=|&?checkout_url=|&?continue=|&?return_path=|&?g=|&?go=|&?goto=|&?URL=).*)$"

    # Filter out links that match the patterns
    filtered_urls = [url for url in urls if not (re.match(pattern_delete, url) or not re.match(pattern_params, url))]

    return filtered_urls

def read_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        return urls
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

def write_urls_to_file(file_path, urls):
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(url + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py input_file.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    urls = read_urls_from_file(input_file)
    
    filtered_urls = delete_unwanted_links(urls)
    
    write_urls_to_file(input_file, filtered_urls)
    
    print(f"Filtered URLs have been written back to '{input_file}'.")
