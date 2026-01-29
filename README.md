# NuScrape

A high-performance Python 3 web crawler with built-in vulnerability detection capabilities.

## Features

- **Fast Concurrent Crawling**: Async/await architecture with configurable concurrency (5-10x faster)
- **Cross-Domain Discovery**: No TLD restrictions - crawls across all domains found
- **Vulnerability Detection**: Real-time scanning for common web vulnerabilities
- **Email Harvesting**: Automatic email address collection
- **Metadata Extraction**: Collects IP, server type, content-type, and webpage titles
- **SQLite Storage**: Persistent storage of domains, emails, and vulnerabilities

## Vulnerability Detection

NuScrape automatically detects:

- **SQL Injection** (UNION SELECT, OR statements, data manipulation, comment injection)
- **Cross-Site Scripting (XSS)** (script tags, event handlers, JavaScript URIs, iframes)
- **Open Redirects** (common redirect parameters)
- **Local File Inclusion (LFI)** (path traversal, file parameters)
- **Server-Side Request Forgery (SSRF)** (localhost, private IPs, URL parameters)
- **Exposed Sensitive Files** (.env, .git, .aws, config files, backups)
- **Default Credentials** (common username/password combinations)

Each vulnerability is classified by severity (high, medium, low) and stored in the database with timestamps.

## Installation

Clone the repository:
```bash
git clone <repository-url>
cd NuScrape
```

Create a virtual Python environment:
```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
./main.py -D https://example.com
```

With custom concurrency (default is 10):
```bash
./main.py -D https://example.com -c 5   # 5 concurrent requests
./main.py -D https://example.com -c 20  # 20 concurrent requests
```

View help:
```bash
./main.py --help
```

## Database

NuScrape creates a SQLite database (`ScrapeDB`) with three tables:

### Domains Table
- url
- ip
- servertype
- content_type
- title

### Emails Table
- email_address

### Vulnerabilities Table (NEW)
- url
- vulnerability_type
- severity (high/medium/low)
- pattern
- details
- timestamp

## Performance

- **Concurrent Requests**: 10 by default (configurable via `-c` flag)
- **Request Timeout**: 30 seconds per request
- **URL Limit**: 10,000 URLs to prevent infinite crawling
- **Speed Improvement**: 5-10x faster than sequential crawling

## Requirements

- Python 3.7+
- aiohttp
- beautifulsoup4
- lxml
- requests
- See `requirements.txt` for full list

## Security Notes

- SSL verification is currently disabled for testing purposes
- The tool is designed for authorized security testing only
- Always obtain proper authorization before scanning any domain
- Vulnerabilities detected are patterns that may require manual verification

## Contributing

Contributions are welcome! Please ensure all tests pass and follow the existing code style.

## License

See LICENSE file for details.

## Changelog

See CHANGES.md for detailed changelog of recent updates.
