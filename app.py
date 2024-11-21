from flask import Flask, render_template, request, jsonify
import hashlib
import os
import time
import threading
import re

app = Flask(__name__)

# Global variables for cancellation, progress, and results
is_cancelled = False
current_progress = 0
results = []
decryption_thread = None


def is_valid_hash(hash_value, algorithm):
    """Validate hash format based on the selected algorithm."""
    hash_patterns = {
        "md5": r"^[a-fA-F0-9]{32}$",        # MD5: 32 hexadecimal characters
        "sha1": r"^[a-fA-F0-9]{40}$",        # SHA1: 40 hexadecimal characters
        "sha256": r"^[a-fA-F0-9]{64}$",      # SHA256: 64 hexadecimal characters
    }

    pattern = hash_patterns.get(algorithm)
    if not pattern:
        return False  # Unsupported algorithm, shouldn't happen if checked earlier

    return re.match(pattern, hash_value) is not None

def decrypt_hashes(hashes, dictionary, algorithm, salt=""):
    global is_cancelled, current_progress, results
    is_cancelled = False  # Reset the cancel flag at the beginning of a new task
    current_progress = 0  # Reset progress
    results.clear()  # Clear any previous results
    print("[DEBUG] Starting decryption process...")  # Debug statement

    total_hashes = len(hashes)
    print(f"[DEBUG] Total number of hashes to process: {total_hashes}")  # Debug statement

    for index, hash_value in enumerate(hashes):
        if is_cancelled:
            results.append('Decryption cancelled by the user.')
            print("[DEBUG] Decryption process was cancelled by the user.")  # Debug statement
            return

        hash_value = hash_value.strip()
        found = False
        with open(dictionary, 'r', encoding='latin-1') as f:
            for word in f:
                word = word.strip()
                if salt:
                    print("salt", salt)
                    print("before salt", word)
                    word = salt + word
                    print("after salt", word)


                if algorithm == "md5":
                    hash_obj = hashlib.md5(word.encode())
                elif algorithm == "sha1":
                    hash_obj = hashlib.sha1(word.encode())
                elif algorithm == "sha256":
                    hash_obj = hashlib.sha256(word.encode())

                # print("hash obj",hash_obj.hexdigest())
                if hash_obj.hexdigest() == hash_value:
                    results.append(f'{hash_value}: {word}')

                    found = True
                    print(f"[DEBUG] Found match for hash {hash_value}: {word}")  # Debug statement
                    break

        if not found:
            results.append(f'{hash_value}: Not found')
            print(f"[DEBUG] No match found for hash {hash_value}")  # Debug statement

        # Update progress after processing each hash
        current_progress = int((index + 1) / total_hashes * 100)
        print(f"[DEBUG] Processed {index + 1}/{total_hashes} hashes. Progress: {current_progress}%")  # Debug statement
        time.sleep(1)  # Simulate time taken for processing

    current_progress = 100  # Set progress to 100% when done
    print("[DEBUG] Decryption process completed.")  # Debug statement

@app.route('/', methods=['GET', 'POST'])
def index():
    global is_cancelled, current_progress, decryption_thread, results
    if request.method == 'POST':
        is_cancelled = False
        current_progress = 0
        results.clear()  # Clear previous results
        print("[DEBUG] Received POST request to start decryption...")  # Debug statement

        hashes = request.form['hashes'].split(',')
        algorithm = request.form['algorithm']
        salt = request.form.get('salt', '')
        dictionary = request.files['dictionary']
        dictionary_path = './dictionary_files/dictionary.txt'
        dictionary.save(dictionary_path)


        # Validate each hash in the input
        for hash_value in hashes:
            if not is_valid_hash(hash_value.strip(), algorithm):
                error_message = f"Invalid {algorithm} hash: '{hash_value}'. Please enter a valid hash."
                print(error_message)  # Debug statement
                results.append(error_message)
                current_progress = 100  # Set progress to 100% since we're not processing further
                return jsonify({'status': 'error', 'results': error_message})
            
        # Start the decryption in a separate thread
        decryption_thread = threading.Thread(target=decrypt_hashes, args=(hashes, dictionary_path, algorithm, salt))
        decryption_thread.start()

        return jsonify({'status': 'started'})

    # For GET requests, ensure that results are empty and render the main page
    return render_template('index.html', results=None)

@app.route('/progress', methods=['GET'])
def progress():
    global current_progress
    print(f"[DEBUG] Current progress requested: {current_progress}%")  # Debug statement
    return jsonify({'progress': current_progress})

@app.route('/results', methods=['GET'])
def get_results():
    global results
    if len(results) == 0:
        print("[DEBUG] Results requested but still in-progress.")  # Debug statement
        return jsonify({'status': 'in-progress'})
    else:
        results_html = '<ul>'
        for result in results:
            results_html += f'<li>{result}</li>'
            print(f"[DEBUG] Adding result to results_html: {result}")  # Debug statement
        results_html += '</ul>'
        print("[DEBUG] Results ready to be sent.")  # Debug statement
        return jsonify({'status': 'completed', 'results': results_html})

@app.route('/cancel', methods=['POST'])
def cancel():
    global is_cancelled
    is_cancelled = True  # Set the flag to cancel the ongoing process
    print("[DEBUG] Received request to cancel decryption.")  # Debug statement
    return jsonify({'status': 'cancelled'})

if __name__ == '__main__':
    app.run(debug=True)
