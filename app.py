import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file
import subprocess

app = Flask(__name__, static_folder='static')

# Create storage directory if it doesn't exist
os.makedirs('storage', exist_ok=True)

# LaTeX preamble with common packages
LATEX_PREAMBLE = r"""\documentclass[12pt]{article}
\usepackage{tikz}
\usepackage{circuitikz}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{float}
\usepackage{geometry}
\usepackage{pgfplots}
\usepackage{color}
\usepackage{xcolor}

\geometry{a4paper, margin=1in}
\pgfplotsset{compat=1.18}

\begin{document}
"""

LATEX_ENDING = r"""
\end{document}
"""

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/compile', methods=['POST'])
def compile_latex():
    try:
        # Get LaTeX code from request
        latex_code = request.json.get('latex_code')
        if not latex_code:
            raise ValueError("No LaTeX code provided")

        # Generate timestamp and create directory for this attempt
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        attempt_dir = os.path.join('storage', timestamp)
        os.makedirs(attempt_dir, exist_ok=True)

        # Define file paths within the attempt directory
        tex_filename = os.path.join(attempt_dir, 'document.tex')
        pdf_filename = os.path.join(attempt_dir, 'document.pdf')
        log_filename = os.path.join(attempt_dir, 'document.log')
        aux_filename = os.path.join(attempt_dir, 'document.aux')

        # Write LaTeX code to file with preamble and ending
        full_latex_code = LATEX_PREAMBLE + latex_code + LATEX_ENDING
        with open(tex_filename, 'w', encoding='utf-8') as f:
            f.write(full_latex_code)

        # Compile LaTeX to PDF (run twice to resolve references)
        process = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', attempt_dir, tex_filename],
            capture_output=True,
            text=True
        )
        
        # Run second time to resolve references if first run was successful
        if process.returncode == 0:
            process = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', attempt_dir, tex_filename],
                capture_output=True,
                text=True
            )

        success = process.returncode == 0
        error_code = process.returncode if not success else None

        # Get error message from log file if compilation failed
        error_message = process.stderr
        if not success and os.path.exists(log_filename):
            with open(log_filename, 'r', encoding='utf-8') as f:
                log_content = f.read()
                # Look for error message in log
                if '!' in log_content:
                    error_message = log_content[log_content.find('!'):]
                    error_message = error_message[:error_message.find('\n\n')]

        # Log the operation
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "attempt_directory": attempt_dir,
            "success": success,
            "error_code": error_code
        }

        # Append to log file
        with open('log.json', 'a+') as f:
            # If file is empty, start with an empty list
            f.seek(0)
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
            logs.append(log_entry)
            f.seek(0)
            f.truncate()
            json.dump(logs, f, indent=2)

        if success:
            return jsonify({
                "success": True,
                "pdf_file": f"{timestamp}/document.pdf"
            })
        else:
            return jsonify({
                "success": False,
                "error": error_message
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    try:
        file_path = os.path.join('storage', filename)
        if not os.path.isfile(file_path):
            return jsonify({
                "success": False,
                "error": "PDF file not found"
            }), 404
        return send_file(file_path, mimetype='application/pdf')
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 