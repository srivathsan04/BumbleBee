# BumbleBee App

BumbleBee is a project that encompasses both a simple chat application and a Quantum Key Distribution (QKD) simulation. This README provides an overview of both components.

## Chat Application

The chat application allows two users to exchange messages in real-time. Each user is represented as "Person 1" and "Person 2". The application encrypts messages before sending them to the server for processing, and upon receiving the encrypted message, it displays encryption details such as Eve's detection, decimal key, cipher text, and decrypted message. Messages are displayed with different background colors based on whether they were sent or received.

### Functionality

- Users can type messages into a text input field and send them.
- Messages are displayed in their respective chat boxes.
- Messages are encrypted before being sent to the server for processing.
- Encryption details and decrypted messages are displayed upon receiving the encrypted message.
- Messages are displayed with different background colors based on whether they were sent or received.

## Quantum Key Distribution (QKD) Simulation

The QKD simulation involves three parties: Alice, Bob, and Eve. It simulates the process of establishing a secure communication channel between Alice and Bob using quantum principles. Here's a brief overview of the simulation:

1. **Key Generation**: Alice generates a random sequence of bits and encodes them into qubits using different bases.
2. **Interception by Eve**: Eve intercepts the qubits sent by Alice and measures them using her own randomly chosen bases.
3. **Measurement by Bob**: Bob receives the qubits from Alice, measures them using his own randomly chosen bases, and generates a key based on the measurement results.
4. **Error Detection**: Alice and Bob compare a subset of their keys to detect any discrepancies caused by Eve's interception.
5. **Key Resizing and Encryption**: Finally, Bob resizes the shared key and uses it to encrypt and decrypt a message.

### Functionality

- Simulates the QKD protocol involving key generation, interception by Eve, measurement by Bob, error detection, key resizing, and encryption.

## Dependencies

- For the chat application:
  - HTML, CSS, JavaScript
  - Bootstrap
  - Fetch API
  - Django
- For the QKD simulation:
  - Python 3.x
  - Qiskit 0.64.0
  - NumPy
