 # Finder-JS

This tool extracts endpoints from JavaScript files. It can be used in two modes: single URL mode and URLs list mode.

## Installation

To install the tool, simply clone the repository:

```bash
git clone https://github.com/ThatNotEasy/Finder-JS.git
```

## Usage

### Single URL Mode

To use the tool in single URL mode, run the following command:

```bash
python3 finder-js.py -u https://example.com/script.js
```

This will extract endpoints from the specified URL and save them to the file `js_endpoints.txt`.

### URLs List Mode

To use the tool in URLs list mode, run the following command:

```bash
python3 finder-js.py -l urls.txt
```

This will extract endpoints from all the URLs in the specified file and save them to the file `js_endpoints.txt`.

The `urls.txt` file should contain a list of URLs, one per line.

### Output

The output of the tool is a text file containing a list of endpoints. Each endpoint is on a new line.

## Options

The tool has the following options:

* `-u`: The URL to extract endpoints from.
* `-l`: The file containing a list of URLs to extract endpoints from.
* `-o`: The output file to save the endpoints to.
* `-p`: Public mode for showing the URLs of each endpoint & showing the function (endpoints/fetch).
* `-t`: The number of threads to use for concurrent processing.

This will extract endpoints from all the URLs in the specified file and save them to the file `js_endpoints.txt`.

## How it works

The tool works by first downloading the specified JavaScript file. It then parses the file and extracts all the URLs that are found in the file. Finally, it saves the extracted URLs to
