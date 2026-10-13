#!/usr/bin/env python3

import ssl
import socket
from datetime import datetime, timezone
import os

FILENAME = "urls.txt"

def get_cert_expiry(hostname, port=443, timeout=5):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expire_date_str = cert['notAfter']
                expire_date = datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
                return expire_date
    except Exception as e:
        return f"Error: {e}"

def check_certificates():
    if not os.path.exists(FILENAME):
        print(f"Error: Could not find '{FILENAME}' in the current directory.")
        print("Please create 'urls.txt' and put one URL per line.")
        return

    print(f"{'URL':<30} | {'Certificate Validity':<22} | {'Less than 60 days?'}")
    print("-" * 75)
    
    now = datetime.now(timezone.utc)
    
    # Read file line-by-line using a loop
    with open(FILENAME, 'r') as file:
        for line in file:
            url = line.strip()
            
            # Skip empty lines or comment lines starting with '#'
            if not url or url.startswith('#'):
                continue
                
            expiry = get_cert_expiry(url)
            
            if isinstance(expiry, datetime):
                formatted_date = expiry.strftime('%d %B %Y')
                days_remaining = (expiry - now).days
                is_less_than_60 = "Yes" if days_remaining < 60 else "No"
                print(f"{url:<30} | {formatted_date:<22} | {is_less_than_60}")
            else:
                print(f"{url:<30} | {expiry}")

if __name__ == "__main__":
    check_certificates()