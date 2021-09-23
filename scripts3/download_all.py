import re
import csv
import os
import urllib.request
from bs4 import BeautifulSoup
import traceback
import requests
import os

csv_path = "../class_ids.csv"
pdf_dir = "../pdfs"
cookies = {
    "SimpleSAML": "1500a428859da425fdcc3be4224db7e1",
    "SimpleSAMLAuthToken": "_a0f18a5f9eacccaaac91ea17085426b15f71c47195",
}


def download_all():
    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Fetch info from CSV file
            quarter = row["Quarter"]
            year = row["Year"]
            id = int(row["Id"])
            low = int(row["Low"])
            high = int(row["High"])

            download_dir = os.path.join(pdf_dir, str(quarter) + "_" + str(year))

            # Check whether the current quarter & year already has a directory
            if os.path.isdir(download_dir):

                print(str(quarter) + " " + str(year) + " directory found!")

                # Get the index of the last PDF that was downloaded in this directory
                _dir = [
                    i.replace(".pdf", "")
                    for i in os.listdir(download_dir)
                    if "pdf" in i
                ]

                if len(_dir) > 0:
                    last_pdf_index = int(max(_dir))
                else:
                    last_pdf_index = low

                # If the last index that was downloaded was also the high from the CSV, then this directory is complete
                if last_pdf_index == high:
                    print(quarter + " " + year + " directory already completed!")
                else:
                    low = last_pdf_index
                    print(quarter + " " + year + " downloads resuming from " + str(low))
                    download_range(quarter, year, id, low, high, cookies)
            else:
                print("Downloading evals from " + str(quarter) + " " + str(year))
                download_range(quarter, year, id, low, high, cookies)


def download_range(quarter, year, id, low, high, cookies):

    rel_pdf_dir = "../pdfs"
    cd = os.getcwd()
    pdf_dir = os.path.abspath(os.path.join(cd, rel_pdf_dir))

    download_dir = os.path.join(pdf_dir, str(quarter) + "_" + str(year))

    os.makedirs(download_dir, exist_ok=True)

    # Iterate from low to high and download all eval PDFs
    for i in range(int(low), int(high) + 1):
        try:
            # Construct URL path to PDF and read response
            url = (
                "https://www.scu.edu/apps/evaluations/?vclass="
                + str(i)
                + "&vtrm="
                + str(id)
            )
            response = requests.get(url, cookies=cookies)
            read = response.content

            # Determine whether recieved page is a PDF
            if len(read) >= 10000:
                print("ID: " + str(i) + " downloaded as " + str(i) + ".pdf")
                filename = str(i) + ".pdf"
                file = open(os.path.join(download_dir, filename), "wb")
                file.write(read)
                file.close()
            elif (
                "Multiple evaluations were found for this course. Please make a selection:"
                in str(read)
            ):

                soup = BeautifulSoup(read, "html.parser")

                base_url = "https://www.scu.edu/apps/evaluations/"
                pattern = r"href=\"(.*?)\">"
                list_of_evals = soup.body.find_all("ul")

                urls = re.findall(pattern, str(list_of_evals))
                urls = [url.replace("&amp;", "&") for url in urls]
                urls = [f"{base_url}{url}" for url in urls]

                for j, url in enumerate(urls):
                    response = requests.get(url, cookies=cookies)
                    read = response.content
                    filename = f"{str(i)}_{str(j)}.pdf"
                    print(f"ID: {str(i)} downloaded as   {filename}")
                    with open(os.path.join(download_dir, filename), "wb") as f:
                        f.write(read)

            else:
                print("ID: " + str(i) + " invalid")

        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(f"{i}: Error: {str(e)}")
            traceback.print_exc()


if __name__ == "__main__":
    download_all()
    # download_range("Spring", 2019, 4040, 83960, 83961, cookies)
