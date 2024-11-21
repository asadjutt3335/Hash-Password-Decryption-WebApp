# Hash Password Decryption Web Application - User Manual

This README file will guide you on how to run the Hash Password Decryption Web Application locally on your machine. This application uses Flask as the backend and includes support for common hash algorithms like MD5, SHA1, and SHA256.

## Prerequisites

1. **Python 3.8 or above**: Ensure you have Python installed on your machine. You can check by running:
   ```bash
   python --version
   ```
2. **pip**: Ensure `pip` is installed for package management. You can check by running:
   ```bash
   pip --version
   ```

## Installation Steps

1. **Clone the Repository**

   First, clone the repository to your local machine.
   ```bash
   git clone <URL>
   ```
   Navigate into the project directory:
   ```bash
   cd <project-direccotry>
   ```

2. **Create a Virtual Environment**

   It’s recommended to create a virtual environment to manage dependencies.
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   Install the required dependencies using the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Once all dependencies are installed, you can run the application with the following command:

```bash
python app.py
```

The application will start a development server, typically accessible at `http://127.0.0.1:5000/`. Open this URL in your web browser to access the application.

## Using the Application

1. **Upload a Dictionary File**: Choose a dictionary file from your machine containing potential passwords.
2. **Enter Hashed Password**: Input the hashed password you want to decrypt.
3. **Select Hash Algorithm**: Choose between MD5, SHA1, and SHA256.
4. **Optional Salt**: If the hashed password is salted, enter the salt value.
5. **Start Decryption**: Click the "Start Decryption" button to begin.
6. **Monitor Progress**: The progress bar will update as the application processes the dictionary entries.
7. **Cancel/Clear**: Use the “Cancel” button to stop decryption mid-process, or “Clear” to reset results.

