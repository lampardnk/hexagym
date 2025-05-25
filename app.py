import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_file
import subprocess
import re

app = Flask(__name__, static_folder='static')

# Create storage directory if it doesn't exist
os.makedirs('storage', exist_ok=True)
os.makedirs('storage/temp', exist_ok=True)  # Add temp directory for preview compilations

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

def sanitize_filename(name):
    """Convert a string to a safe filename."""
    # Replace spaces and special characters
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    return name.lower()

def create_question_folder(name):
    """Create a unique folder for a question."""
    unique_id = str(uuid.uuid4())[:8]
    safe_name = sanitize_filename(name)
    folder_name = f"{safe_name}_{unique_id}"
    folder_path = os.path.join('storage', 'questions', folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path, unique_id

def compile_latex_for_question(latex_code, folder_path):
    """Compile LaTeX code and save files in the question folder."""
    try:
        # Define file paths
        tex_path = os.path.join(folder_path, 'question.tex')
        pdf_path = os.path.join(folder_path, 'question.pdf')
        log_path = os.path.join(folder_path, 'question.log')

        # Write LaTeX code to file
        full_latex_code = LATEX_PREAMBLE + latex_code + LATEX_ENDING
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(full_latex_code)

        # Compile LaTeX to PDF
        process = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', folder_path, tex_path],
            capture_output=True,
            text=True
        )
        
        # Run second time to resolve references if first run was successful
        if process.returncode == 0:
            process = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', folder_path, tex_path],
                capture_output=True,
                text=True
            )

        success = process.returncode == 0
        error_message = None

        if not success and os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                log_content = f.read()
                if '!' in log_content:
                    error_message = log_content[log_content.find('!'):]
                    error_message = error_message[:error_message.find('\n\n')]

        return {
            'success': success,
            'error': error_message,
            'tex_path': tex_path,
            'pdf_path': pdf_path if success else None
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'tex_path': None,
            'pdf_path': None
        }

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/questions', methods=['GET'])
def get_questions():
    questions_dir = os.path.join('storage', 'questions')
    if not os.path.exists(questions_dir):
        return jsonify([])
    
    questions = []
    for folder in os.listdir(questions_dir):
        json_path = os.path.join(questions_dir, folder, 'metadata.json')
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                question = json.load(f)
                questions.append(question)
    
    return jsonify(questions)

@app.route('/questions', methods=['POST'])
def add_question():
    try:
        data = request.json
        name = data.get('name')
        if not name:
            return jsonify({"success": False, "error": "Question name is required"}), 400

        # Create question folder
        folder_path, unique_id = create_question_folder(name)

        # Compile LaTeX
        compilation_result = compile_latex_for_question(data.get('content', ''), folder_path)
        if not compilation_result['success']:
            return jsonify({
                "success": False,
                "error": f"LaTeX compilation failed: {compilation_result['error']}"
            }), 500

        # Create metadata
        metadata = {
            "id": unique_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "tags": data.get('tags', []),
            "points": data.get('points', 0),
            "hints": [
                {
                    "text": hint.get('text', ''),
                    "points_deduction": hint.get('points_deduction', 0)
                }
                for hint in data.get('hints', [])
            ],
            "answer": data.get('answer', ''),
            "content": data.get('content', ''),  # Store raw LaTeX content
            "files": {
                "tex": os.path.relpath(compilation_result['tex_path'], 'storage'),
                "pdf": os.path.relpath(compilation_result['pdf_path'], 'storage')
            }
        }

        # Save metadata
        metadata_path = os.path.join(folder_path, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        return jsonify({"success": True, "id": unique_id, "metadata": metadata})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    try:
        data = request.json
        questions_dir = os.path.join('storage', 'questions')
        
        # Find question folder
        question_folder = None
        for folder in os.listdir(questions_dir):
            if folder.endswith(question_id):
                question_folder = folder
                break
        
        if not question_folder:
            return jsonify({"success": False, "error": "Question not found"}), 404

        folder_path = os.path.join(questions_dir, question_folder)
        
        # Compile new LaTeX if content changed
        if 'content' in data:
            compilation_result = compile_latex_for_question(data['content'], folder_path)
            if not compilation_result['success']:
                return jsonify({
                    "success": False,
                    "error": f"LaTeX compilation failed: {compilation_result['error']}"
                }), 500

        # Update metadata
        metadata_path = os.path.join(folder_path, 'metadata.json')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        # Update fields
        metadata.update({
            "name": data.get('name', metadata['name']),
            "tags": data.get('tags', metadata['tags']),
            "points": data.get('points', metadata['points']),
            "hints": data.get('hints', metadata['hints']),
            "answer": data.get('answer', metadata['answer']),
            "content": data.get('content', metadata['content']),  # Update raw LaTeX content
            "updated_at": datetime.now().isoformat()
        })

        if 'content' in data:
            metadata['files'] = {
                "tex": os.path.relpath(compilation_result['tex_path'], 'storage'),
                "pdf": os.path.relpath(compilation_result['pdf_path'], 'storage')
            }

        # Save updated metadata
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        return jsonify({"success": True, "metadata": metadata})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        questions_dir = os.path.join('storage', 'questions')
        
        # Find question folder
        question_folder = None
        for folder in os.listdir(questions_dir):
            if folder.endswith(question_id):
                question_folder = folder
                break
        
        if not question_folder:
            return jsonify({"success": False, "error": "Question not found"}), 404

        folder_path = os.path.join(questions_dir, question_folder)
        
        # Delete all files in the folder
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

        # Delete the folder
        os.rmdir(folder_path)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    return send_file(os.path.join('storage', filename), mimetype='application/pdf')

@app.route('/compile', methods=['POST'])
def compile_latex():
    try:
        data = request.json
        latex_code = data.get('latex_code')
        if not latex_code:
            return jsonify({"success": False, "error": "No LaTeX code provided"}), 400

        # Create a temporary folder for this compilation
        temp_folder = os.path.join('storage', 'temp', str(uuid.uuid4())[:8])
        os.makedirs(temp_folder, exist_ok=True)

        # Compile the LaTeX code
        result = compile_latex_for_question(latex_code, temp_folder)

        if not result['success']:
            return jsonify({
                "success": False,
                "error": result['error'] or "Compilation failed"
            }), 500

        # Return the path to the generated PDF
        pdf_path = os.path.relpath(result['pdf_path'], 'storage')
        return jsonify({
            "success": True,
            "pdf_file": pdf_path
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    try:
        questions_dir = os.path.join('storage', 'questions')
        
        # Find question folder
        question_folder = None
        for folder in os.listdir(questions_dir):
            if folder.endswith(question_id):
                question_folder = folder
                break
        
        if not question_folder:
            return jsonify({"success": False, "error": "Question not found"}), 404

        # Read metadata
        metadata_path = os.path.join(questions_dir, question_folder, 'metadata.json')
        with open(metadata_path, 'r') as f:
            question = json.load(f)
            
        return jsonify(question)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/submit-attempt', methods=['POST'])
def submit_attempt():
    try:
        data = request.json
        question_id = data.get('questionId')
        answer = data.get('answer')
        time_spent = data.get('timeSpent')
        points_earned = data.get('pointsEarned')

        # Get the question to check the answer
        questions_dir = os.path.join('storage', 'questions')
        question_folder = None
        for folder in os.listdir(questions_dir):
            if folder.endswith(question_id):
                question_folder = folder
                break
        
        if not question_folder:
            return jsonify({"success": False, "error": "Question not found"}), 404

        # Read metadata to get correct answer
        metadata_path = os.path.join(questions_dir, question_folder, 'metadata.json')
        with open(metadata_path, 'r') as f:
            question = json.load(f)
            
        # Simple string comparison for now
        # In a real application, you might want more sophisticated answer checking
        is_correct = answer.strip().lower() == question['answer'].strip().lower()

        # In a real application, you would:
        # 1. Save the attempt to a database
        # 2. Mark the question as completed if correct
        # 3. Store the points earned and time spent
        # 4. Store failed attempts count

        return jsonify({
            "success": True,
            "isCorrect": is_correct,
            "message": "Correct answer!" if is_correct else "Incorrect answer",
            "points_earned": points_earned if is_correct else 0,
            "time_spent": time_spent
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) 