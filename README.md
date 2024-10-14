# Election-Management-System
Developed a robust and efficient solution using a Database Management System. This system is designed to streamline and enhance the entire election process

Key Features:
User-Friendly Interface: The application uses Streamlit to provide an intuitive web-based interface for election officials and administrators to manage the election process efficiently.

Voter and Candidate Management: The system supports adding, updating, and deleting voter and candidate details.

Vote Management: Users can insert and update vote data, and it integrates with MySQL to store and retrieve vote information.

Election Results: The application can count votes for a given election and determine the winner based on the highest number of votes a candidate received.

Polling Station and Election Official Management: Provides a system for managing polling stations and election officials, including inserting, updating, and deleting their details.

Security: MySQL is used for secure data storage, and password fields in the UI are hidden using Streamlit’s password input option.

Database Operations: The backend features include custom SQL queries for inserting, updating, deleting, and fetching data from the MySQL database.

Technologies Used:
Streamlit: For creating the front-end user interface.
Python (PyMySQL): To connect to the MySQL database and perform SQL queries.
MySQL: As the backend database for storing and managing election data.
Pandas: For manipulating and analyzing data, especially in determining election results.
Base64: To handle data encoding for security purposes (if applicable).
Core Functionalities:
CRUD Operations: The system provides functionalities to create, read, update, and delete data from different election-related tables.

Tables include voter, candidate, pollingstation, participatedvoters, electionofficial, and vote.
Vote Counting and Winner Determination:

The system retrieves vote data and counts the number of votes each candidate received.
Based on the highest number of votes, it determines and announces the winner of the election.
Error Handling: Comprehensive error handling mechanisms are built into the system, ensuring that users are notified of issues like database connectivity problems or invalid data entries.

Data Presentation: Election and vote data is presented in a tabular format using Streamlit, making it easy to view the current state of the election.

My Role:
I played a key role in the entire development lifecycle:

Database Design: Designed the MySQL schema to store election-related data efficiently.
Backend Logic: Implemented Python functions to handle database operations, including inserting, updating, deleting, and viewing records.
Frontend Development: Created the user interface using Streamlit to interact with the database.
Testing: Conducted extensive testing to ensure data integrity and functionality across all modules.
