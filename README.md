# IPFS Metadata Image URL Updater

A Python utility script for batch-updating NFT metadata JSON files by replacing the `image` field with cleaned IPFS image URLs scraped from a web directory (e.g., IPFS gateway or Pinata-hosted folder).

This tool is useful when NFT image URLs contain temporary query parameters or need to be standardized before deployment or upload to marketplaces.

---

## Features

- Scrapes `.png` image links from an IPFS or HTTP directory
- Filters out Pinata `filename=` query URLs
- Cleans image URLs by removing query strings
- Matches images with existing metadata files by filename index
- Updates the `image` field in metadata JSON files
- Outputs updated metadata into a dedicated directory
- Safe handling of missing or invalid JSON files

---

## Project Structure

```text
.
├── app.py                 # Main script
├── metadata/              # Original metadata files (input)
│   ├── 0
│   ├── 1
│   └── ...
├── metadata_json/         # Updated metadata files (output)
│   ├── 0.json
│   ├── 1.json
│   └── ...
└── README.md
```

## Requirements

* Python 3.7+
* Required Python packages:
  * `requests`
  * `beautifulsoup4`

Install dependencies:

```bash
pip install requests beautifulsoup4
```

## Configuration

Edit the following variables in `app.py`:

```python
url = ''          # Base URL of the IPFS gateway or website
ifps = '/ipfs/...'  # IPFS directory path
```

Example:

```python
url = 'https://ipfs.io'
ifps = '/ipfs/QmYourCID/'
```

---

## How It Works

1. Sends an HTTP GET request to the target IPFS directory.
2. Parses the HTML page and extracts all `.png` links.
3. Skips links containing `filename=` (commonly added by Pinata).
4. Removes query parameters from image URLs.
5. Extracts image index (e.g., `0.png` → `0`).
6. Loads the corresponding metadata file from `./metadata/`.
7. Updates the `image` field with the cleaned URL.
8. Saves:
   * The updated metadata back to `./metadata/`
   * A formatted copy to `./metadata_json/{id}.json`

---

## Usage

Run the script from the project root:

```bash
python app.py
```

Console output example:

```text
Updated 'image' key in file 12
Updated 'image' key in file 13
File 14 not found.
Error decoding JSON in file 15.
```

---

## Error Handling

* **File not found**
  Logged when a metadata file does not exist for a given image index.
* **Invalid JSON**
  Logged if a metadata file cannot be parsed.
* **HTTP request failure**
  Script will abort and print the HTTP status code.

---

## Notes & Best Practices

* Metadata filenames are expected to match image indices exactly (e.g., `0.png` → `metadata/0`)
* Original metadata files are overwritten — keep backups if needed
* Output files in `metadata_json/` are prettified with indentation
* Script assumes a flat IPFS directory listing

---

## Possible Extensions

* Support for `.jpg` / `.webp`
* Automatic CID detection
* Attribute validation for NFT standards (ERC-721 / ERC-1155)
* Dry-run mode
* Logging to file
* CLI arguments with `argparse`

---

## License

MIT License
