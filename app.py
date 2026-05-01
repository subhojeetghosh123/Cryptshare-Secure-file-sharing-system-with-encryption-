import requests
import time
import os
import shutil

from flask import Flask, render_template, request, send_file
from crypto_utils import encrypt_file, decrypt_file

# -------------------------------
# TEMP PASSWORD STORAGE
# -------------------------------
file_passwords = {}

# -------------------------------
# VIRUSTOTAL API
# -------------------------------
API_KEY = "05d2ed57e6d72e4d08c320df291bf723fda0edeb0ab062ec2f96eaa74f3704ca"


def scan_file(filepath):
    upload_url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": API_KEY}

    # Upload file to VirusTotal
    with open(filepath, "rb") as f:
        resp = requests.post(upload_url, files={"file": f}, headers=headers)

    if resp.status_code != 200:
        return {"status": "error"}

    analysis_id = resp.json()["data"]["id"]

    # Poll analysis status
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    file_hash = None

    for _ in range(25):  # wait up to ~50 sec
        r = requests.get(analysis_url, headers=headers)
        data = r.json()

        status = data["data"]["attributes"]["status"]

        if status == "completed":
            file_hash = data.get("meta", {}).get("file_info", {}).get("sha256")
            if file_hash:
                break

        time.sleep(2)

    if not file_hash:
        return {
            "status": "unknown",
            "malicious_count": 0,
            "safe_count": 0,
            "file_id": analysis_id
        }

    # Get final scan report
    file_url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    fr = requests.get(file_url, headers=headers)
    fdata = fr.json()

    stats = fdata["data"]["attributes"]["last_analysis_stats"]

    malicious = stats.get("malicious", 0)
    harmless = stats.get("harmless", 0)

    return {
        "status": "malicious" if malicious > 0 else "safe",
        "malicious_count": malicious,
        "safe_count": harmless,
        "file_id": file_hash
    }


# -------------------------------
# GET NGROK URL
# -------------------------------
def get_base_url():
    try:
        url = "http://127.0.0.1:4040/api/tunnels"
        data = requests.get(url).json()
        return data["tunnels"][0]["public_url"]
    except:
        return request.host_url


# -------------------------------
# FLASK APP
# -------------------------------
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"

os.makedirs("uploads", exist_ok=True)


# -------------------------------
# HOME + UPLOAD
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        password = request.form.get("password")

        if file.filename == "":
            return "No file selected!"

        filename = file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save password
        file_passwords[filename] = password

        # Save uploaded file
        file.save(filepath)

        # Show scanning page
        return render_template("scanning.html", filename=filename)

    return render_template("upload.html")


# -------------------------------
# SCAN FILE ROUTE
# -------------------------------
@app.route("/scan/<filename>")
def scan(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    scan_result = scan_file(filepath)

    if scan_result["status"] == "malicious":
        os.remove(filepath)
        return f"⚠️ Malware detected! ({scan_result['malicious_count']} engines flagged this file)"

    elif scan_result["status"] == "error":
        return "⚠️ Error scanning file."

    # Encrypt file after safe scan
    encrypt_file(filepath)

    # Generate shareable link
    base_url = get_base_url()
    download_link = base_url + "/download/" + filename

    return render_template(
        "success.html",
        link=download_link,
        scan=scan_result
    )


# -------------------------------
# DOWNLOAD + PASSWORD CHECK
# -------------------------------
@app.route("/download/<filename>", methods=["GET", "POST"])
def download(filename):
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(path):
        return "File not found!"

    # Show password form
    if request.method == "GET":
        return render_template("password.html")

    # Verify password
    entered_password = request.form.get("password")
    real_password = file_passwords.get(filename)

    if entered_password != real_password:
        return render_template("password.html", error="❌ Wrong Password!")

    # Decrypt temporary copy
    temp_path = "temp_" + filename
    shutil.copy(path, temp_path)

    decrypt_file(temp_path)

    return send_file(temp_path, as_attachment=True)


# -------------------------------
# SHOW FILES (OPTIONAL)
# -------------------------------
@app.route("/files")
def files():
    return str(os.listdir("uploads/"))


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)