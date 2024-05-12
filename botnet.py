import argparse
import threading
import requests
from urllib.parse import urlparse, parse_qs, urlencode
from colorama import init, Fore, Style

init(autoreset=True)

def filter_urls(urls):
    filtered_urls = []
    for url in urls:
        parsed_url = urlparse(url.strip())
        if parsed_url.scheme and parsed_url.netloc:  # Check if the URL is well-formed
            filtered_urls.append(url.strip())
    return filtered_urls

def replace_url(url_list, web, use_urlencode=True, use_base64=False, use_normal=False):
    new_urls = []
    for url in url_list:
        parsed_url = urlparse(url.strip())
        query_params = parse_qs(parsed_url.query)
        modified_params = {}
        modified = False
        for param in query_params:
            if param.lower() in ['next', 'url', 'target', 'rurl', 'dest', 'destination', 
                                 'redir', 'redirect_uri', 'redirect_url', 'redirect', 
                                 'redirect_to', 'redirect_url', 'return', 'returnTo', 
                                 'return_to', 'checkout_url', 'continue', 'return_path', 'g', 'go', 'goto', 'URL']:
                modified_params[param] = [web]
                modified = True
            else:
                modified_params[param] = query_params[param]
        if modified:
            if use_normal:
                new_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(modified_params, doseq=True)}"
            else:
                if use_urlencode:
                    modified_query = urlencode(modified_params, doseq=True)
                    new_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{modified_query}"
                elif use_base64:
                    # Implement base64 encoding here if needed
                    pass  # Placeholder for base64 encoding
                else:
                    new_url = web  # Use the URL as-is without any encoding
            new_urls.append(new_url)
    return new_urls

def make_request(url):
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url.strip(), verify=False)
        status_code = response.status_code
        if status_code in [200]:
            print(f"\n[{Fore.BLUE}+{Style.RESET_ALL}] Request to {url.strip()} - Status: {status_code}")
        else:
            print(f"\n[{Fore.BLUE}-{Style.RESET_ALL}] Request to {url.strip()} - Status: {status_code}")
            return False
    except Exception as e:
        print(f"\n[{Fore.RED}-{Style.RESET_ALL}] Error by sending the request to {url.strip()}: {e}")
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to send requests to modified URLs.")
    parser.add_argument("file_path", type=str, help="Path of the .txt file containing the URLs.")
    parser.add_argument("user_web", type=str, help="URL to be used for modifying the URLs in the file.")
    parser.add_argument("threads_count", type=int, help="Number of threads to use.")
    parser.add_argument("--normal", action="store_true", help="Use the URL as-is without encoding.")
    parser.add_argument("--urlencode", action="store_true", help="Use urlencode for encoding parameters.")
    parser.add_argument("--base64", action="store_true", help="Use base64 encoding for parameters.")
    
    args = parser.parse_args()

    file_path = args.file_path
    user_web = args.user_web
    threads_count = args.threads_count
    use_urlencode = args.urlencode
    use_base64 = args.base64
    use_normal = args.normal

    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
    except FileNotFoundError:
        print("File not found.")
        exit()

    filtered_urls = filter_urls(urls)

    # Determine encoding based on user input
    if use_normal:
        new_urls = replace_url(filtered_urls, user_web, use_urlencode=False, use_base64=False, use_normal=True)
    else:
        if use_base64:
            new_urls = replace_url(filtered_urls, user_web, use_urlencode=False, use_base64=True)
        else:
            new_urls = replace_url(filtered_urls, user_web, use_urlencode=True, use_base64=False)

    while True:
        threads = []
        for new_url in new_urls:
            t = threading.Thread(target=make_request, args=(new_url,))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()
