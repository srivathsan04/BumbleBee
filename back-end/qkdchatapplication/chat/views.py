from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.views import Response
from rest_framework import status
from .models import chatMsg
from .serializer import chatMsgSerializer
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import *


import qiskit
#print(qiskit.__version__)

from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer

import numpy as np
from numpy.random import randint
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import json

# Create your views here.
class MsgHandling(APIView):
    def get(self, request):
        print("Msg recieved")
        return Response({"msg":"recieve"}, status = status.HTTP_200_OK) 
    
    def post(self, request):
        sender = request.data["sender"]
        message = request.data["message"]
        msg = {
            "sender": sender,
            "message": message,
        }
        serializer = chatMsgSerializer(data=msg)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "give msg is saved"}, status = status.HTTP_201_CREATED)
        else:
            return Response({"msg": serializer.errors})
        
class MsgEncryption(APIView):
    def post(self, request):
        msg = request.data['message']
        def encode_message(bits, bases):
            message = []
            for i in range(n):
                qc = QuantumCircuit(1,1)
                if bases[i] == 0:    # Z-basis encoding
                    if bits[i] == 0:
                        pass 
                    else:
                        qc.x(0)
                else:                # X-basis encoding
                    if bits[i] == 0:
                        qc.h(0)
                    else:
                        qc.x(0)
                        qc.h(0)
                qc.barrier()
                message.append(qc)
            return message, qc
        
        def measure_message(message, bases):
            # backend = Aer.get_backend('aer_simulator')
            measurements = []
            for q in range(n):
                if bases[q] == 0: # measuring in Z-basis
                    message[q].measure(0,0)
                if bases[q] == 1: # measuring in X-basis
                    message[q].h(0)
                    message[q].measure(0,0)
                aer_sim = Aer.get_backend('aer_simulator')
                result = aer_sim.run(message[q], shots=1, memory=True).result()
                measured_bit = int(result.get_memory()[0])
                measurements.append(measured_bit)
            return measurements

        def remove_garbage(a_bases, b_bases, bits):
            good_bits = []
            for q in range(n):
                if a_bases[q] == b_bases[q]:
                    good_bits.append(bits[q])
            return good_bits
        
        def sample_bits(bits, selection):
            sample = []
            for i in selection:
                # use np.mod to make sure that sampled bits always in list range
                i = np.mod(i, len(bits))
                # pop(i) removes the element at index 'i', from the main list as well
                sample.append(bits.pop(i))
            return sample

        n = 100

        # Step 1: Set the qubit sequence to be transmitted, and the basis sequence to be used by Alice
        alice_bits = randint(2, size=n)
        alice_bases = randint(2, size=n)

        # Step 2: Encode the message from Alice's side using the quantum circuit defined before
        message = encode_message(alice_bits, alice_bases)[0]

        # Step 2/3: Interception by Eve
        import numpy as np  # Import NumPy module

        # Generate random bases for Eve
        eve_bases = np.random.randint(2, size=len(message))

        # Print the bases generated for Eve
        print(f"Eve's bases:\n{eve_bases}")

        # Define the function to measure the intercepted message

        def measure_message(message, bases):
            # Initialize a list to store the measured bits
            measured_bits = []
            
            # Measure each bit in the message according to the basis
            for bit, basis in zip(message, bases):
                if basis == 0:  # Measure in the Z basis
                    measured_bits.append(bit)
                elif basis == 1:  # Measure in the X basis
                    measured_bits.append(0 if bit == 0 else 1)  # Flip the bit if the basis is X
            
            return measured_bits

        # Measure the intercepted message
        intercepted_message = measure_message(message, eve_bases)

        # Print the intercepted message
        # print(f'Intercepted message:\n{intercepted_message}')

        # Step 3: Message received and measured by Bob using his basis sequence
        bob_bases = randint(2, size=n)
        bob_results = measure_message(message, bob_bases)


        # Step 4: Discarding qubits with mismatched basis measurements
        bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
        alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)

        # Step 5: The number of qubits broadcasted to verify key integrity
        sample_size = 10   # the lower the sample, the easier for Eve to go undetected
        bit_selection = randint(n, size=sample_size)
        print(f'Verification bits selected from key: {bit_selection}')

        bob_sample = sample_bits(bob_key, bit_selection)
        alice_sample = sample_bits(alice_key, bit_selection)

        # Checking whether the sample matches from both Alice and Bob's side

        if bob_sample != alice_sample:
            print("Eve's interference was detected.")
        else:
            print("Eve went undetected!")

        bob_key = remove_garbage(alice_bases, bob_bases, bob_results)

        bob_key_str = ''.join(str(bit) for bit in bob_key)
        # Filter out non-numeric characters from the string
        bob_key_str = ''.join(filter(str.isdigit, bob_key_str))

        bob_key_dec = int(bob_key_str, 2)
        print(f'Decimal Key: {bob_key_dec}')

        original_key = bob_key_dec.to_bytes(8, byteorder='big')

        desired_key_length = 32  # Length of resized key in bytes (128 bits)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=desired_key_length,
            salt=b'',
            iterations=100000,
            backend=default_backend()
        )

        resized_key = kdf.derive(original_key)
        resized_key

        # Initialising the AES cipher object with expanded key and mode
        cipher = Cipher(algorithms.AES(resized_key), modes.ECB(), backend=default_backend())

        encryptor = cipher.encryptor()
        decryptor = cipher.decryptor()

        # Encrypt plaintext
        plaintext = msg.encode("utf-8")

        # padding added to fit the plaintext to the fixed block lengths required by AES
        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        print("Ciphertext:", ciphertext)

        # Decrypt ciphertext
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_ciphertext = decryptor.update(ciphertext) + decryptor.finalize()
        decrypted = unpadder.update(unpadded_ciphertext) + unpadder.finalize()
        print("Decrypted:", decrypted.decode('utf-8'))        

        response = {
          "eves_bases": str(type(eve_bases)),
          "bit_selection": str(type(bit_selection)),
          "decimal_key": str(type(bob_key_dec)),
          "cipher_text": str(type(ciphertext)),
          "Decrypted": str(type(decrypted)),
        }

        res = {
            "decimal_key": str(bob_key_dec),
          "cipher_text": str(ciphertext),
          "Decrypted": str(decrypted),
        }
        return Response(json.dumps({"msg": res}),status = status.HTTP_200_OK)

        