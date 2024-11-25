import re
import requests
from autopkglib import Processor, ProcessorError

__all__ = ["HeliconFocusURLProvider"]

class HeliconFocusURLProvider(Processor):
    description = "Fetches the latest Helicon Focus download URL from the website."
    input_variables = {}
    output_variables = {
        "url": {
            "description": "The dynamically constructed download URL for Helicon Focus."
        }
    }

    def main(self):
        # URL of the page containing version info
        history_url = "https://www.heliconsoft.com/helicon-focus-history-of-changes-mac/"
        try:
            # Fetch the page content
            response = requests.get(history_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as err:
            raise ProcessorError(f"Error fetching version page: {err}")

        # Extract the latest version using regex
        match = re.search(r"Helicon Focus Mac \(Lite, Pro, Premium\) ([0-9.]+)", response.text)
        if not match:
            raise ProcessorError("Unable to find the latest version on the website.")

        latest_version = match.group(1)
        self.output(f"Found latest version: {latest_version}")

        # Construct the download URL
        download_url = f"https://www.heliconsoft.com/downloads/HeliconFocus_{latest_version}.dmg"
        self.output(f"Constructed download URL: {download_url}")

        # Set the output variable
        self.env["url"] = download_url
