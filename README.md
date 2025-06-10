# Phishing Email Detector

This is a simple project I built to detect phishing emails using machine learning. It's not a fancy app—just a clean CLI tool where you can train a model and test email files to see if they’re phishing or not.

---

## Project Structure

```bash
phishing_email_detector/
├── data/                  # where I keep the downloaded raw CSV files
├── data/cleaned/          # where cleaned CSVs are saved
├── model/                 # holds the saved model and vectorizer
├── example_emails/        # test email samples (scam, legit, etc.)
├── download_csv_files.py  # used to download phishing CSV from Google Drive
├── clean_data.py          # used to clean up raw CSVs
├── nltk_data/             # folder for stopwords
├── train_model.py         # script to train the model
├── phishing_detector.py   # main program to detect phishing
├── stopwords.zip.1        # NLTK stopwords (downloaded manually)
└── .gitignore             # excludes big files and unnecessary folders
```

---

## Setup Instructions

1. **Clone the repo:**

   ```bash
   git clone https://github.com/MmaGod1/phishing_email_detector.git
   cd phishing_email_detector
   ```

2. **Set up virtual environment:**

   ```bash
   python -m venv myenv
   # Activate it:
   source myenv/bin/activate  # On Linux/macOS
   myenv\Scripts\activate     # On Windows
   ```

3. **Install requirements:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the dataset:**
   You can download the phishing dataset from Google Drive using:

   ```bash
   python download_csv_files.py
   ```

5. **Extract stopwords:**
   You’ll need to extract the stopwords zip into a specific location. Just unzip `stopwords.zip.1` like this:

   ```
   mkdir -p nltk_data
   unzip stopwords.zip.1 -d nltk_data/
   ```

   That should place the stopwords at:

   ```
   nltk_data/corpora/stopwords/
   ```

6. **Clean the data:**
   After downloading, clean the raw CSV files using:

   ```bash
   python clean_data.py
   ```

---

## Training the Model

To train the model after cleaning:

```bash
python train_model.py
```

* It reads everything in `data/cleaned/`
* Trains the model with TF-IDF vectorization
* Saves both the model and vectorizer into the `model/` directory

---

## Running Detection

Once the model is trained, you can check any email text like this:

```bash
python phishing_detector.py example_emails/legit_email.txt
```

It will tell you if it’s phishing or not, and show the confidence score for both classes.

---

## ✉️ Sample Emails You Can Test With

* `Classic scam.txt`
* `Verify_account.txt`
* `Legit_email.txt`
* `Facebook_login_alert.txt`
* `Suspended_bank_account.txt`
* `Upgrade_required.txt`

You can use these to test how well the model works.

---

## Limitations & Lessons Learned

This model works well mostly on older or more obvious phishing formats, especially the ones found in public datasets.

But it doesn’t really catch newer, more sophisticated scams. If you try recent phishing emails that look almost like real ones, it might misclassify them. That’s just because the data available online is outdated or limited, and most of the examples I could find were from older phishing campaigns.

So yeah, you shouldn’t rely on this as a complete solution—more like a learning project to understand how phishing detection can be done with ML.

---

## .gitignore Setup

To avoid pushing huge files or unnecessary folders to GitHub, I added this to `.gitignore`:

```txt
myenv/
data/
```

This way, things like the downloaded datasets, and my virtual environment won’t be committed.


You can include the dataset source in your README like this (in your natural voice):

---

### Dataset Source

The dataset I used was downloaded from Kaggle. Here's the link:

> [Phishing Email Dataset by Naser Abdullah Alam on Kaggle](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset?utm_source=chatgpt.com)

But because the file is large (over 20MB), I didn't push it to GitHub. Instead, I wrote a Python script (`download_csv_files.py`) that anyone can run to download it directly from my Google Drive. Makes things easier for anyone trying to run the project locally.

