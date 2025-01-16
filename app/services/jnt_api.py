import requests
from bs4 import BeautifulSoup

def fetch_jt_rate(payload: dict, package_type: str) -> float:
    GET_URL = "https://www.jtexpress.my/shipping-rates"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": GET_URL,
        "X-Requested-With": "XMLHttpRequest"
    }

    session = requests.Session()
    response = session.get(GET_URL, headers=HEADERS)
    

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch the response. Status code: {response.status_code}")

    # Parse the CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '_token'})
    if not csrf_token:
        raise ValueError("CSRF Token not found.")
    csrf_token_value = csrf_token['value']

    payload["_token"] = csrf_token_value
    post_response = session.post(GET_URL, headers=HEADERS, data=payload)

    #print("J&T Post Response:", post_response.status_code)
    #print("J&T Payload", payload)

    soup = BeautifulSoup(post_response.text, 'html.parser')
    rows = soup.find_all('tr')

    for row in rows:
        headers = row.find_all('th')
        if headers and "Total (incl. Tax)" in headers[0].get_text():
            cells = row.find_all('td')
            rates = [cell.get_text(strip=True).replace(',', '') for cell in cells]

            # Select the appropriate rate based on package_type
            if package_type == "parcel":
                if rates[0].upper() != "N/A":
                    return float(rates[0])
                else:
                    return "N/A"
            elif package_type == "document":
                if rates[1].upper() != "N/A":
                    return float(rates[1])
                else:
                    return "N/A"
            else:
                raise ValueError(f"Invalid package_type: {package_type}. Must be 'parcel' or 'document'.")


    raise ValueError("J&T rate not found in response")

