Secure File Transfer System

This repository contains server and client Python scripts for a secure file transfer system over a network using SSL/TLS encryption. The system allows users to perform various operations such as listing files, downloading, uploading, and deleting files securely between the server and client.
Features

    Secure Communication: Utilizes SSL/TLS encryption for secure communication between the server and client, ensuring data confidentiality and integrity.
    Multiple Operations: Supports operations like listing available files, downloading files from the server, uploading files to the server, and deleting files from the server.
    Error Handling: Implements error handling mechanisms to deal with various exceptions and provide informative error messages to the users.
    User-Friendly Interface: Offers a simple command-line interface for users to interact with the system easily.

Prerequisites

    Python 3.x
    OpenSSL library
    Certificates: Both server and client require valid SSL/TLS certificates for secure communication. Ensure that the certificates are generated and stored correctly.

Usage

    Clone the repository to your local machine.
    Configure the server and client scripts with appropriate settings such as server IP address, port number, file paths, and certificate files.
    Run the server script on the designated server machine.
    Run the client script on the client machine and follow the prompts to perform desired file transfer operations.
    Ensure proper network connectivity between the server and client for successful communication.

Security Considerations

    Certificate Management: Proper management of SSL/TLS certificates is crucial for secure communication. Ensure that certificates are generated, stored, and configured correctly on both the server and client sides.
    Secure File Handling: Implement secure file handling practices to prevent unauthorized access or tampering of files during transfer.

Disclaimer

This project is developed for educational and learning purposes. Use it responsibly and ensure compliance with applicable laws and regulations regarding data privacy and security. The developers are not liable for any misuse or unauthorized use of this software.
Contributors

    Kurumeti Prajval

License

This project is licensed under the MIT License. Feel free to modify and distribute the code for personal and commercial use.
