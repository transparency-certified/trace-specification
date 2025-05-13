import os
import json
import argparse
import requests

DEFAULT_ZENODO_URL = "https://sandbox.zenodo.org/api"
HEADERS = {"Content-Type": "application/json"}


def create_deposition(api_url, access_token):
    response = requests.post(
        f"{api_url}/deposit/depositions",
        params={"access_token": access_token},
        json={},
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()


def upload_files(bucket_url, files, access_token):
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "rb") as fp:
            response = requests.put(
                f"{bucket_url}/{filename}",
                data=fp,
                params={"access_token": access_token},
            )
            response.raise_for_status()
            print(f"Uploaded: {filename}")


def set_metadata(api_url, deposition_id, metadata, access_token):
    url = f"{api_url}/deposit/depositions/{deposition_id}"
    response = requests.put(
        url,
        params={"access_token": access_token},
        json=metadata,
        headers=HEADERS,
    )
    response.raise_for_status()
    print("Metadata set.")


def main():
    parser = argparse.ArgumentParser(description="Upload files to Zenodo using the REST API.")
    parser.add_argument("access_token", help="Zenodo access token")
    parser.add_argument(
        "--api-url",
        default=DEFAULT_ZENODO_URL,
        help="Base API URL for Zenodo (default: sandbox)",
    )
    parser.add_argument(
        "--metadata",
        default="zenodo.json",
        help="Path to Zenodo metadata file (default: zenodo.json)",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="List of files to upload",
    )
    args = parser.parse_args()

    with open(args.metadata, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"Creating deposition on {args.api_url}...")
    deposition = create_deposition(args.api_url, args.access_token)
    deposition_id = deposition["id"]
    bucket_url = deposition["links"]["bucket"]
    print(f"Deposition ID: {deposition_id}")

    print("Uploading files...")
    upload_files(bucket_url, args.files, args.access_token)

    print("Create metadata...")
    set_metadata(args.api_url, deposition_id, metadata, args.access_token)

    print("Draft deposit created: ", deposition["links"]["html"])

if __name__ == "__main__":
    main()
