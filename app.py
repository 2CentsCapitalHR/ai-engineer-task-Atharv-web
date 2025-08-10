from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, session, jsonify
import os, json, traceback
from pathlib import Path
from werkzeug.utils import secure_filename
import legal_work as lw
import time

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev_secret")

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
CHECKLIST_PATH = Path("backend/checklist.json")
FAISS_DB_PATH = Path("backend/faiss_db")
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Global progress variable (simple in-memory store)
progress_status = {"step": "", "percent": 0}

def update_progress(step, percent):
    progress_status["step"] = step
    progress_status["percent"] = percent

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_workflow():
    try:
        # Clear previous
        for p in INPUT_DIR.iterdir():
            if p.is_file():
                p.unlink()

        uploaded_paths = []
        for file in request.files.getlist("docx_files"):
            if file.filename.lower().endswith(".docx"):
                dest = INPUT_DIR / secure_filename(file.filename)
                file.save(dest)
                uploaded_paths.append(str(dest))

        if not uploaded_paths:
            flash("Please upload at least one .docx file.", "error")
            return redirect(url_for("index"))

        # Step 1: Identify process
        update_progress("Identifying legal process...", 20)
        time.sleep(0.5)
        process = lw.identify_legal_process(uploaded_paths)

        # Step 2: Compare with checklist
        update_progress("Comparing with checklist...", 40)
        time.sleep(0.5)
        checklist_result = lw.compare_with_checklist(process, uploaded_paths, str(CHECKLIST_PATH))

        # Step 3: Check legal issues
        update_progress("Checking legal issues...", 60)
        time.sleep(0.5)
        issues = lw.check_legal_issues(uploaded_paths, str(FAISS_DB_PATH))

        # Step 4: Annotate and save
        update_progress("Annotating documents...", 80)
        time.sleep(0.5)
        out_folder = OUTPUT_DIR
        report = lw.annotate_and_generate_report(process, uploaded_paths, checklist_result, str(CHECKLIST_PATH), issues, str(out_folder))

        # Step 5: Save report & zip
        update_progress("Saving results...", 100)
        OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
        report_path = OUTPUT_DIR / "report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        annotated_files = [f.name for f in OUTPUT_DIR.glob("*.docx")]
        return render_template("index.html", report=report,annotated_files=annotated_files)

    except Exception as e:
        flash(f"Error: {e}", "error")
        traceback.print_exc()
        return redirect(url_for("index"))

@app.route("/progress")
def progress():
    return jsonify(progress_status)

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR,filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
