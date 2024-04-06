from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    action = data['action']
    user_input = data['user_input']
    
    # Process the input based on the selected action
    if action == 'encrypt':
        # Perform encryption here
        result = f"Encrypted: {user_input}"  # Placeholder for actual encryption
    elif action == 'decrypt':
        # Perform decryption here
        result = f"Decrypted: {user_input}"  # Placeholder for actual decryption
    
    return result

if __name__ == '__main__':
    app.run(debug=True)
