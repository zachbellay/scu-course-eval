## SCU Course Evals Scraper
This codebase contains the code to do the following:
- scrape & download PDFs from SCU Course Evals (`scripts3/download_all.py`)
- convert PDFs to text (`scripts3/pdfs_to_text.py`)
- parse PDF and extract information we care about, such as overall difficulty into a CSV (`scripts3/parse.py`)


To run this code we must do the following:

### Step 1. Setup Environment

Do this on an intel x86 machine, as opposed to an M1 Mac, see note

Why: You need to do this so that packages can be installed appropriately and not conflict with your system's python. There is a good chance that by using your system python this won't work.

My recommended approach for python virtual environments is to use pyenv. You can use whatever approach you prefer, but this is what I'd suggest:

Step 1: Install pyenv
- `curl https://pyenv.run | bash`

Step 2: Add pyenv commands to your bashrc (or other shell config):
- Follow instructions for your specific shell here: https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv

Step 3: Install Python 3.7
- `pyenv install 3.7`

Step 4: Create `scu-course-evals` environment
- `pyenv virtualenv 3.7 scu-course-evals`

Step 5: Set `scu-course-evals` as local environment (specific to this directory)
- `pyenv local scu-course-evals`

Step 5b (Optional): If that doesn't work run `pyenv shell scu-course-evals`

Step 6: Install dependencies:
- `pip install -r requirements.txt && pip install pandas scipy`

_Note: As far as I know, scipy doesn't work on M1 Macs (at least I haven't been able to get it to work) so I would suggest using x86 architecture intel machines_ 

## Step 2: Download PDFS

Step 1. `mkdir pdfs`

Step 2. If you had a `pdfs.zip`, unzip it here such that the directory structure looks like: `./pdfs/Fall_2010`

Step 3. Update the `class_ids.csv`: This can be done by going to https://www.scu.edu/apps/evaluations and selecting the Quarter and Year you are interested in. Then to get that Quarter + Year's ID, look in the URL for the `vtrm` query param. Copy that as the ID. For the Low, and High fields, order the table by the number column, and add the lowest number, and the highest number to the CSV.

Step 4. Next, go into your browser and "Inspect Element". From there, open the Network tab in your browser. Refresh the page, and scroll to the very top to find the request that returns the HTML document. Select that request and look at the Request Headers. You should see that there is a Cookie field, and that there is a `SimpleSAML` and `SimpleSAMLAuthToken`. Copy paste those into `scripts3/download_all.py` in order to be able to make requests logged in as your user.

Step 4. `cd scripts3` and then run `python download_all.py`, wait for the script to complete running.


## Step 3: Convert PDFs to text

Step 1. Install `xpdftotext`: Go to https://www.xpdfreader.com/download.html and download the xpdf command line tools for your system.  Make sure it is installed correctly by going to your terminal and running `pdftotext --help` and making sure that it returns something.

Step 2. Then run `mkdir txts`

Step 3. Again, if you have a `txts.zip`, be sure to unzip it here

Step 3. `cd scripts3`

Step 4. Run `python pdfs_to_text.py` and wait for the script to complete running.

## Step 4: Extract Data from text into CSV

Step 1. `cd scripts3`

Step 2: Run `python parse.py` and wait for the script to complete running.


Result: `course_evals.csv` file. Copy paste this into the `flask-scu-course-evals` file so that you can run the `csv_to_sqlite.py` script there. See that repo's README for more details
