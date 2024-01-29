import argparse
import requests
import re
import json
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style

EndPoints = []

def is_in_array(element, arr):
    return element in arr

def is_valid(stringo):
    invalid_chars = ["$", "#", "|", "\\", "?", "(", ")", "[", "]", "{", "}", ",", "<", ":", "*", ">", "\n", "./", "//", ".svg", ".png", ".jpg", ".ico"]
    return not any(char in stringo for char in invalid_chars) and len(stringo) > 1

def extract_all_urls(content):
    urls = set()
    href_links = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
    urls.update(href_links)
    
    a_links = re.findall(r'<a [^>]*href=["\'](https?://[^"\']+)["\'][^>]*>', content)
    urls.update(a_links)

    src_links = re.findall(r'src=["\'](https?://[^"\']+)["\']', content)
    urls.update(src_links)

    endpoints = re.findall(r'\"/[^"]+\"', content)
    for endpoint in endpoints:
        current_endpoint = endpoint[2:-1]
        if is_valid(current_endpoint) and not is_in_array(current_endpoint, EndPoints):
            EndPoints.append(current_endpoint)
            urls.add(current_endpoint)

    try:
        json_data = json.loads(content)
        json_urls = [url for url in find_urls_in_json(json_data)]
        urls.update(json_urls)
    except json.JSONDecodeError:
        pass

    return list(urls)

def find_urls_in_json(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower() == 'url':
                yield value
            elif isinstance(value, (dict, list)):
                yield from find_urls_in_json(value)
    elif isinstance(data, list):
        for item in data:
            yield from find_urls_in_json(item)

def gimme_js_link(js_url, output, activation_flag):
    try:
        with open(output, 'a') as my_output, open('success.txt', 'a') as success_output:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0"}
            response = requests.get(js_url, headers=headers, timeout=7)
            if response.status_code == 200:
                content = response.text

                all_urls = extract_all_urls(content)

                for url in all_urls:
                    if activation_flag:
                        print(Fore.GREEN + f"URL: {js_url} - Extracted URL: {url}" + Style.RESET_ALL)
                    else:
                        print(Fore.GREEN + f"Extracted URL: {url}" + Style.RESET_ALL)
                    my_output.write(f"{url}\n")
                    success_output.write(f"{js_url}/{url}\n")

            else:
                print(Fore.RED + f"[ - ] Bad JS File Detected - URL: {js_url}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[ - ] Error accessing {js_url}: {e}" + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(description='EndpointsExtractor Tool')
    parser.add_argument('-u', dest='single_url', help='Single URL to grep endpoints from')
    parser.add_argument('-l', dest='urls_list', help='List of .js file URLs to grep endpoints from')
    parser.add_argument('-o', dest='output', default='js_endpoints.txt', help='Output file')
    parser.add_argument('-p', dest='activation_flag', action='store_true', help='Public mode for showing the URLs of each endpoint & showing the function (endpoints/fetch)')
    parser.add_argument('-t', dest='threads', type=int, default=1, help='Number of threads to use for concurrent processing')

    args = parser.parse_args()

    if not args.single_url and not args.urls_list or args.single_url and args.urls_list:
        parser.error('Please use either -u for single_url mode or -l for URLs_list mode, not both or neither')

    if args.single_url:
        gimme_js_link(args.single_url, args.output, args.activation_flag)
    elif args.urls_list:
        with open(args.urls_list, 'r') as urls_file:
            with ThreadPoolExecutor(max_workers=args.threads) as executor:
                executor.map(lambda line: gimme_js_link(line.strip(), args.output, args.activation_flag), urls_file)

if __name__ == "__main__":
    main()
