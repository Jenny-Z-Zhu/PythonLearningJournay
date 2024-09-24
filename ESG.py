import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import io
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret_430185784526-s65b1invd6r4jet5g9t17hrh2dta47cu.apps.googleusercontent.com.json", scope)
client = gspread.authorize(creds)

# Use the spreadsheet key instead of the name
spreadsheet_key = "15f-sfnSZ2eXTT6g11W0ittBWuZS8H3N4hyiCSQCc1rU"
sheet = client.open_by_key(spreadsheet_key).sheet1

# Get all records
data = sheet.get_all_records()


def get_actual_url(redirect_url):
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    actual_url = query_params.get('q', [None])[0]
    return actual_url


def find_report_links(company_name, year):
    # Include "Form 10-K" as part of the search query
    search_query = f"{company_name} {year} annual report OR Form 10K OR Form 10-K"
    search_url = f"https://www.google.com/search?q={search_query}"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for link in soup.find_all("a"):
        url = link.get("href")

        # Ensure the URL is absolute
        if url.startswith('/url?q='):
            url = get_actual_url(url)
        elif url.startswith('/'):
            url = 'https://www.google.com' + url

        # Filter links: only consider results that contain the company name in the URL or text
        if company_name.lower() in url.lower() or company_name.lower() in link.text.lower():
            links.append(url)

    return links


def search_pdf_for_keywords(pdf_url, keywords, company_name):
    try:
        response = requests.get(pdf_url, timeout=10)

        # Check if the file is actually a PDF
        if response.headers.get('Content-Type', '').lower() != 'application/pdf':
            print(f"Skipped non-PDF file: {pdf_url}")
            return False

        try:
            pdf_text = extract_text(io.BytesIO(response.content))
        except PDFSyntaxError:
            print(f"Failed to parse PDF file: {pdf_url}")
            return False

        # Check if the company name appears in the PDF
        if company_name.lower() not in pdf_text.lower():
            print(f"Company name not found in PDF: {pdf_url}")
            return False

        for keyword in keywords:
            if keyword.lower() in pdf_text.lower():
                return True

        return False

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the PDF from {pdf_url}: {e}")
        return False


keywords = ["affordable hous", "social hous"]

for record in data:
    company_name = record['Company Name']
    year = record['Year']

    print(f"Processing {company_name} for the year {year}...")

    try:
        report_links = find_report_links(company_name, year)

        if not report_links:
            print(f"No reports found for {company_name}.")
            continue

        for report_url in report_links:
            if report_url:
                if search_pdf_for_keywords(report_url, keywords, company_name):
                    print(f"Found relevant information in {report_url}")
                else:
                    print(f"No relevant information found in {report_url}")
            else:
                print(f"Invalid URL extracted for {company_name}.")

    except Exception as e:
        print(f"Error processing {company_name} for the year {year}: {e}")

# Add a new column for results if it doesn't exist
sheet.add_cols(1)
sheet.update_cell(1, len(sheet.row_values(1)) + 1, "Affordable Housing Strategy Found")

# Update each row with results (You should store and check 'relevant' from the above loop)
for i, record in enumerate(data):
    relevant = True  # Replace with the actual condition to set 'Yes' or 'No'
    sheet.update_cell(i + 2, len(record) + 1, "Yes" if relevant else "No")
