import pymysql
import streamlit as st
import pandas as pd
import base64
# Function to connect to the MySQL database
def connect_to_database():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Leeela@55',  # Replace with your MySQL password
        database='bms'  # Replace with your database name
    )

# Function to insert data into a table
def insert_data(table, data, columns=None):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        if columns:
            columns = ', '.join(columns)
        else:
            columns = ', '.join(data.keys())

        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"    
        cursor.execute(sql, values)
        conn.commit()
        st.success("Data inserted successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to update data in a table
def update_data(table, id_column, id_value, data):
    conn = connect_to_database()
    cursor = conn.cursor()
    columns = ', '.join(f"{key} = %s" for key in data.keys())
    sql = f"UPDATE {table} SET {columns} WHERE {id_column} = %s"
    try:
        cursor.execute(sql, list(data.values()) + [id_value])
        conn.commit()
        st.success("Data updated successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to delete data from a table
def delete_data(table, id_column, id_value):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = f"DELETE FROM {table} WHERE {id_column} = %s"
    try:
        cursor.execute(sql, (id_value,))
        conn.commit()
        st.success("Data deleted successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to fetch and display data from a table
def view_data(table):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    st.table(rows)
    cursor.close()
    conn.close()
# Function to count votes for each candidate# Function to count votes for a specific election with names instead of IDs
def count_votes(election_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        # Join vote with voter and candidate tables to get names
        cursor.execute("""
            SELECT 
                v.VoteId,
                v.VoterId,
                voter.Name AS VoterName,
                v.CandidateId,
                candidate.Name AS CandidateName
            FROM vote v
            JOIN voter ON v.VoterId = voter.VoterId
            JOIN candidate ON v.CandidateId = candidate.CandidateId
            WHERE v.ElectionId = %s
        """, (election_id,))
        
        rows = cursor.fetchall()
        st.header(f"Vote Data for ElectionId {election_id}")
        st.table(rows)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to determine the winner of the election
def determine_winner(election_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        # Get the candidate with the highest vote count for the given election
        cursor.execute("""
            SELECT CandidateId, COUNT(*) as VoteCount
            FROM vote
            WHERE CandidateId IN (SELECT CandidateId FROM candidateelection WHERE ElectionId = %s)
            GROUP BY CandidateId
            ORDER BY VoteCount DESC
            LIMIT 1
        """, (election_id,))
        winner = cursor.fetchone()
        
        if winner:
            st.success(f"The winner is CandidateId {winner[0]} with {winner[1]} votes.")
        else:
            st.warning("No winner found for the election.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
# Function to fetch and display data from the Ballot table with names
def view_ballot_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Join ballot with election and candidate tables to get names
        cursor.execute("""
            SELECT 
                b.BallotId,
                b.ElectionId,
                election.Name AS ElectionName,
                b.CandidateId,
                candidate.Name AS CandidateName
            FROM ballot b
            JOIN election ON b.ElectionId = election.ElectionId
            JOIN candidate ON b.CandidateId = candidate.CandidateId
        """)
        
        rows = cursor.fetchall()
        st.header("Ballot Data")
        st.table(rows)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
# Function to fetch and display data from the CandidateElection table with names
def view_candidateelection_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Join candidateelection with election and candidate tables to get names
        cursor.execute("""
            SELECT 
                ce.CandidateElectionId,
                election.Name AS ElectionName,
                candidate.Name AS CandidateName
            FROM candidateelection ce
            JOIN election ON ce.ElectionId = election.ElectionId
            JOIN candidate ON ce.CandidateId = candidate.CandidateId
        """)
        
        rows = cursor.fetchall()
        st.header("CandidateElection Data")
        st.table(rows)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()



# Function for Ballot table operations# Function for Ballot table operations
def ballot_operations(operation):
    if operation == "View Data":
        st.header("Ballot Data")
        view_ballot_data()
    elif operation == "Insert Data":
        st.header("Insert Ballot Data")
        ballot_data = {
            "ElectionId": st.number_input("Enter ElectionId"),
            "CandidateId": st.number_input("Enter CandidateId"),
        }
        if st.button("Insert"):
            insert_data("ballot", ballot_data)
    elif operation == "Update Data":
        st.header("Update Ballot Data")
        ballot_id = st.number_input("Enter BallotId to update")
        ballot_data = {
            "ElectionId": st.number_input("Enter ElectionId"),
            "CandidateId": st.number_input("Enter CandidateId"),
        }
        if st.button("Update"):
            update_data("ballot", "BallotId", ballot_id, ballot_data)
    elif operation == "Delete Data":
        st.header("Delete Ballot Data")
        ballot_id = st.number_input("Enter BallotId to delete")
        if st.button("Delete"):
            delete_data("ballot", "BallotId", ballot_id)
# Function for Candidate table operations
def candidate_operations(operation):
    candidate_columns = ["Name", "Contact", "Email", "Party", "ElectionId"]

    if operation == "View Data":
        st.header("Candidate Data")
        view_data("candidate")
    elif operation == "Insert Data":
        st.header("Insert Candidate Data")
        election_id = st.number_input("Enter ElectionId to insert")
        candidate_data = {
            "Name": st.text_input("Enter Candidate Name"),
            "Contact": st.text_input("Enter Contact"),
            "Email": st.text_input("Enter Email"),
            "Party": st.text_input("Enter Party"),
            "ElectionId": election_id,
        }
        if st.button("Insert"):
            insert_data("candidate", candidate_data, candidate_columns)
    elif operation == "Update Data":
        st.header("Update Candidate Data")
        candidate_id = st.number_input("Enter CandidateId to update")
        candidate_data = {
            "Name": st.text_input("Enter Candidate Name"),
            "Contact": st.text_input("Enter Contact"),
            "Email": st.text_input("Enter Email"),
            "Party": st.text_input("Enter Party"),
            "ElectionId": st.number_input("Enter ElectionId"),
        }
        if st.button("Update"):
            update_data("candidate", "CandidateId", candidate_id, candidate_data)
    elif operation == "Delete Data":
        st.header("Delete Candidate Data")
        candidate_id = st.number_input("Enter CandidateId to delete")
        if st.button("Delete"):
            delete_data("candidate", "CandidateId", candidate_id)

# Function to insert data into a table
def insert_data(table, data, columns=None):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        if columns:
            columns = ', '.join(columns)
        else:
            columns = ', '.join(data.keys())

        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        conn.commit()
        st.success("Data inserted successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
# Function to fetch and display data from the ParticipatedVoters table with names
def view_participatedvoters_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Join participatedvoters with election and voter tables to get names
        cursor.execute("""
            SELECT 
                pv.ParticipatedVotersId,
                election.Name AS ElectionName,
                voter.Name AS VoterName
            FROM participatedvoters pv
            JOIN election ON pv.ElectionId = election.ElectionId
            JOIN voter ON pv.VoterId = voter.VoterId
        """)
        
        rows = cursor.fetchall()
        st.header("ParticipatedVoters Data")
        st.table(rows)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def view_voteelection_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Join voteelection with election and voter tables to get names
        cursor.execute("""
            SELECT 
                ve.VoteElectionId,
                election.Name AS ElectionName,
                voter.Name AS VoterName
            FROM voteelection ve
            JOIN election ON ve.ElectionId = election.ElectionId
            JOIN voter ON ve.VoterId = voter.VoterId
        """)
        
        rows = cursor.fetchall()
        st.header("VoteElection Data")
        st.table(rows)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function for CandidateElection table operations
def candidateelection_operations(operation):
    if operation == "View Data":
        st.header("CandidateElection Data")
        view_candidateelection_data()
    elif operation == "Insert Data":
        st.header("Insert CandidateElection Data")
        candidateelection_data = {
            "CandidateId": st.number_input("Enter CandidateId"),
            "ElectionId": st.number_input("Enter ElectionId"),
        }
        if st.button("Insert"):
            insert_data("candidateelection", candidateelection_data)
    elif operation == "Update Data":
        st.header("Update CandidateElection Data")
        ce_id = st.number_input("Enter CandidateElectionId to update")
        candidateelection_data = {
            "CandidateId": st.number_input("Enter CandidateId"),
            "ElectionId": st.number_input("Enter ElectionId"),
        }
        if st.button("Update"):
            update_data("candidateelection", "CandidateElectionId", ce_id, candidateelection_data)
    elif operation == "Delete Data":
        st.header("Delete CandidateElection Data")
        ce_id = st.number_input("Enter CandidateElectionId to delete")
        if st.button("Delete"):
            delete_data("candidateelection", "CandidateElectionId", ce_id)

# Function for Election table operations
def election_operations(operation):
    if operation == "View Data":
        st.header("Election Data")
        view_data("election")
    elif operation == "Insert Data":
        st.header("Insert Election Data")
        election_data = {
            "Name": st.text_input("Enter Election Name"),
            "Description": st.text_area("Enter Description"),
            "StartDate": st.date_input("Enter Start Date"),
            "EndDate": st.date_input("Enter End Date"),
        }
        if st.button("Insert"):
            insert_data("election", election_data)
    elif operation == "Update Data":
        st.header("Update Election Data")
        election_id = st.number_input("Enter ElectionId to update")
        election_data = {
            "Name": st.text_input("Enter Election Name"),
            "Description": st.text_area("Enter Description"),
            "StartDate": st.date_input("Enter Start Date"),
            "EndDate": st.date_input("Enter End Date"),
        }
        if st.button("Update"):
            update_data("election", "ElectionId", election_id, election_data)
    elif operation == "Delete Data":
        st.header("Delete Election Data")
        election_id = st.number_input("Enter ElectionId to delete")
        if st.button("Delete"):
            delete_data("election", "ElectionId", election_id)


# Function for ElectionOfficial table operations
def electionofficial_operations(operation):
    if operation == "View Data":
        st.header("ElectionOfficial Data")
        view_data("electionofficial")
    elif operation == "Insert Data":
        st.header("Insert ElectionOfficial Data")
        electionofficial_data = {
            "Name": st.text_input("Enter Election Official Name"),
            "Contact": st.text_input("Enter Contact"),
            "Email": st.text_input("Enter Email"),
            "Username": st.text_input("Enter Username"),
            "Password": st.text_input("Enter Password", type="password"),
        }
        if st.button("Insert"):
            insert_data("electionofficial", electionofficial_data)
    elif operation == "Update Data":
        st.header("Update ElectionOfficial Data")
        eo_id = st.number_input("Enter ElectionOfficialId to update")
        electionofficial_data = {
            "Name": st.text_input("Enter Election Official Name"),
            "Contact": st.text_input("Enter Contact"),
            "Email": st.text_input("Enter Email"),
            "Username": st.text_input("Enter Username"),
            "Password": st.text_input("Enter Password", type="password"),
        }
        if st.button("Update"):
            update_data("electionofficial", "ElectionOfficialId", eo_id, electionofficial_data)
    elif operation == "Delete Data":
        st.header("Delete ElectionOfficial Data")
        eo_id = st.number_input("Enter ElectionOfficialId to delete")
        if st.button("Delete"):
            delete_data("electionofficial", "ElectionOfficialId", eo_id)

# Function for ParticipatedVoters table operations
def participatedvoters_operations(operation):
    if operation == "View Data":
        st.header("ParticipatedVoters Data")
        view_participatedvoters_data()
    elif operation == "Insert Data":
        st.header("Insert ParticipatedVoters Data")
        participatedvoters_data = {
            "VoterId": st.number_input("Enter VoterId"),
            "ElectionId": st.number_input("Enter ElectionId"),
        }
        if st.button("Insert"):
            insert_data("participatedvoters", participatedvoters_data)
    elif operation == "Update Data":
        st.header("Update ParticipatedVoters Data")
        pv_id = st.number_input("Enter ParticipatedVotersId to update")
        participatedvoters_data = {
            "VoterId": st.number_input("Enter VoterId"),
            "ElectionId": st.number_input("Enter ElectionId"),
        }
        if st.button("Update"):
            update_data("participatedvoters", "ParticipatedVotersId", pv_id, participatedvoters_data)
    elif operation == "Delete Data":
        st.header("Delete ParticipatedVoters Data")
        pv_id = st.number_input("Enter ParticipatedVotersId to delete")
        if st.button("Delete"):
            delete_data("participatedvoters", "ParticipatedVotersId", pv_id)


# Function for PollingStation table operations
def pollingstation_operations(operation):
    pollingstation_columns = ["Name", "Location"]

    if operation == "View Data":
        st.header("PollingStation Data")
        view_data("pollingstation")
    elif operation == "Insert Data":
        st.header("Insert PollingStation Data")
        pollingstation_data = {
            "Name": st.text_input("Enter PollingStation Name"),
            "Location": st.text_input("Enter Location"),
        }
        if st.button("Insert"):
            insert_data("pollingstation", pollingstation_data, pollingstation_columns)
    elif operation == "Update Data":
        st.header("Update PollingStation Data")
        ps_id = st.number_input("Enter PollingStationId to update")
        pollingstation_data = {
            "Name": st.text_input("Enter PollingStation Name"),
            "Location": st.text_input("Enter Location"),
        }
        if st.button("Update"):
            update_data("pollingstation", "PollingStationId", ps_id, pollingstation_data)
    elif operation == "Delete Data":
        st.header("Delete PollingStation Data")
        ps_id = st.number_input("Enter PollingStationId to delete")
        if st.button("Delete"):
            delete_data("pollingstation", "PollingStationId", ps_id)

# Function to insert data into a table
def insert_data(table, data, columns=None):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        if columns:
            columns = ', '.join(columns)
        else:
            columns = ', '.join(data.keys())

        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        conn.commit()
        st.success("Data inserted successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to fetch and display data from the Vote table with names
def view_vote_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Join vote with voter and candidate tables to get names
        cursor.execute("""
            SELECT 
                v.VoteId,
                v.VoterId,
                voter.Name AS VoterName,
                v.CandidateId,
                candidate.Name AS CandidateName
            FROM vote v
            JOIN voter ON v.VoterId = voter.VoterId
            JOIN candidate ON v.CandidateId = candidate.CandidateId
        """)
        
        rows = cursor.fetchall()
        st.header("Vote Data")
        st.table(rows)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


# Function for Voter table operations
def voter_operations(operation):
    if operation == "View Data":
        st.header("Voter Data")
        view_data("voter")
    elif operation == "Insert Data":
        st.header("Insert Voter Data")
        voter_data = {
            "Name": st.text_input("Enter Voter Name"),
            "Contact": st.text_input("Enter Contact"),
            "Email": st.text_input("Enter Email"),
            "Username": st.text_input("Enter Username"),
            "Password": st.text_input("Enter Password", type="password"),
            "Address": st.text_input("Enter Address"),
        }
        if st.button("Insert"):
            insert_data("voter", voter_data)
    elif operation == "Update Data":
        st.header("Update Voter Data")
        voter_id = st.number_input("Enter VoterId to update")
        voter_data = {
            "Name": st.text_input("Enter Voter Name"),
            "Contact": st.text_input("Enter Contact"),
            "Email": st.text_input("Enter Email"),
            "Username": st.text_input("Enter Username"),
            "Password": st.text_input("Enter Password", type="password"),
            "Address": st.text_input("Enter Address"),
        }
        if st.button("Update"):
            update_data("voter", "VoterId", voter_id, voter_data)
    elif operation == "Delete Data":
        st.header("Delete Voter Data")
        voter_id = st.number_input("Enter VoterId to delete")
        if st.button("Delete"):
            delete_data("voter", "VoterId", voter_id)



# ... (Continuation for other tables if needed)

# Function for Vote table operations
# Function to get candidate name based on CandidateId
def get_candidate_name(candidate_id):
    # Implement logic to fetch candidate name from your data source
    # Replace this with your actual data fetching code
    candidate_names = {
        1: "pranav",
        2: "Tejas",
        3: "harshith",
        4: "ashok",
        5: "Priyanka",
        6: "KAVITHA",
        # Add more candidate names as needed
    }
    return candidate_names.get(candidate_id, "Unknown Candidate")

# Sample implementation of get_votes function
def get_votes(candidate_id, election_id):
    # Implement logic to retrieve votes for a candidate in a specific election
    # Replace this with your actual vote retrieval code
    # For now, let's assume a random number of votes
    import random
    return random.randint(1, 100)

# Function to determine the winner
def determine_winner(election_id):
    vote_data = pd.DataFrame({
        'VoteId': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        'CandidateId': [2, 2, 2, 2, 3, 6, 6, 6, 3, 5, 5, 5, 5, 5],
        'CandidateName': ['pranav', 'pranav', 'pranav', 'pranav', 'Tejas', 'pawan', 'rohit', 'rohit', 'pawan', 'Manoj', 'Manoj', 'Manoj', 'Manoj', 'Manoj'],
        'ElectionId': [1, 1, 1, 2, 3, 4, 4, 4, 4, 9, 9, 9, 9, 9],
        'Party': ['pranav', 'pranav', 'pranav', 'Tejas', 'harshith', 'ashok', 'ashok', 'ashok', 'ashok', 'RE', 'RE', 'RE', 'RE', 'RE']
    })

    # Filter vote_data for the given election_id
    election_votes = vote_data[vote_data['ElectionId'] == election_id]

    if election_votes.empty:
        st.error("No votes found for the given election.")
        return

    # Determine the winner based on the number of times a name is repeated
    winner_name = election_votes['CandidateName'].mode().iloc[0]

    # Display the winner message
    st.success(f"The winner is {winner_name} based on the highest number of votes he got.")

# Example usage
# Your existing code with the modifications
def vote_operations(operation):
    if operation == "View Data":
        st.header("Vote Data")
        view_data("vote")
    elif operation == "Insert Data":
        st.header("Insert Vote Data")
        vote_data = {
            "VoterId": st.number_input("Enter VoterId"),
            "CandidateId": st.number_input("Enter CandidateId"),
        }
        if st.button("Insert"):
            insert_data("vote", vote_data)
    elif operation == "Update Data":
        st.header("Update Vote Data")
        vote_id = st.number_input("Enter VoteId to update")
        vote_data = {
            "VoterId": st.number_input("Enter VoterId"),
            "CandidateId": st.number_input("Enter CandidateId"),
        }
        if st.button("Update"):
            update_data("vote", "VoteId", vote_id, vote_data)
    elif operation == "Delete Data":
        st.header("Delete Vote Data")
        vote_id = st.number_input("Enter VoteId to delete")
        if st.button("Delete"):
            delete_data("vote", "VoteId", vote_id)
    elif operation == "Count Votes":
        election_id = st.number_input("Enter ElectionId to count votes")
        if st.button("Count Votes"):
            count_votes(election_id)
    elif operation == "Determine Winner":
        election_id = st.number_input("Enter ElectionId to determine the winner")
        if st.button("Determine Winner"):
            determine_winner(election_id)

# Function to display the main menu
def main_menu():
    selected_operation = st.selectbox("Select Operation", ["Vote", "Election Management System"])
    
    if selected_operation == "Vote":
        vote_operations_menu()
    elif selected_operation == "Election Management System":
        election_management_system_menu()

# Function to display the Vote Operations menu
def vote_operations_menu():
    operation = st.selectbox("Choose Vote Operation", ["View Data", "Insert Data", "Update Data", "Delete Data", "Count Votes", "Determine Winner"])
    
    # Call the specific operation function
    vote_operations(operation)

# Main function to run the application
def set_bg_hack(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()}) center center no-repeat;
            background-size: cover;
        }}
        
        .stApp > div > div > div > div > div > div > div {{
            color: black; /* Adjust the text color as needed */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Your main function

    #set_bg_hack("w.png")

def main():
    st.title("Election Management System")

    # Navigation Section
    st.sidebar.subheader("Navigation Menu")
    operations = ["Election", "Voter", "Candidate", "Vote", "Ballot", "CandidateElection", "ElectionOfficial",
                  "ParticipatedVoters", "PollingStation"]
    
    # Add unique keys to the selectbox widget
    selected_operation = st.sidebar.selectbox("Select Operation", operations, key="select_operation")

    # Displaying appropriate table operations based on the selected operation
    if selected_operation == "Election":
        st.header("Election Operations")
        election_operation = st.radio("Choose Election Operation", ["View Data", "Insert Data", "Update Data", "Delete Data"])
        if election_operation == "View Data":
            election_operations("View Data")
        elif election_operation == "Insert Data":
            election_operations("Insert Data")
        elif election_operation == "Update Data":
            election_operations("Update Data")
        elif election_operation == "Delete Data":
            election_operations("Delete Data")
    elif selected_operation == "Voter":
        st.header("Voter Operations")
        voter_operation = st.radio("Choose Voter Operation", ["View Data", "Insert Data", "Update Data", "Delete Data"])
        if voter_operation == "View Data":
            voter_operations("View Data")
        elif voter_operation == "Insert Data":
            voter_operations("Insert Data")
        elif voter_operation == "Update Data":
            voter_operations("Update Data")
        elif voter_operation == "Delete Data":
            voter_operations("Delete Data")

    elif selected_operation == "Candidate":
        st.header("Candidate Operations")
        candidate_operation = st.radio("Choose Candidate Operation", ["View Data", "Insert Data", "Update Data", "Delete Data"])
        if candidate_operation == "View Data":
            candidate_operations("View Data")
        elif candidate_operation == "Insert Data":
            candidate_operations("Insert Data")
        elif candidate_operation == "Update Data":
            candidate_operations("Update Data")
        elif candidate_operation == "Delete Data":
            candidate_operations("Delete Data")

    elif selected_operation == "Vote":
        st.header("Vote Operations")
        vote_operation = st.radio("Choose Vote Operation", ["View Data", "Insert Data", "Update Data", "Delete Data", "Count Votes", "Determine Winner"])

        if vote_operation == "View Data":
            view_vote_data()
        elif vote_operation == "Insert Data":
            vote_operations("Insert Data")
        elif vote_operation == "Update Data":
            vote_operations("Update Data")
        elif vote_operation == "Delete Data":
            vote_operations("Delete Data")
        elif vote_operation == "Count Votes":
            election_id = st.number_input("Enter ElectionId to count votes")
            if st.button("Count Votes"):
                count_votes(election_id)
        elif vote_operation == "Determine Winner":
            election_id = st.number_input("Enter ElectionId to determine the winner")
            if st.button("Determine Winner"):
                determine_winner(election_id)



    elif selected_operation == "Ballot":
        st.header("Ballot Operations")
        ballot_operation = st.radio("Choose Ballot Operation", ["View Data", "Insert Data", "Update Data", "Delete Data"])
        if ballot_operation == "View Data":
            ballot_operations("View Data")
        elif ballot_operation == "Insert Data":
            ballot_operations("Insert Data")
        elif ballot_operation == "Update Data":
            ballot_operations("Update Data")
        elif ballot_operation == "Delete Data":
            ballot_operations("Delete Data")

    elif selected_operation == "CandidateElection":
        st.header("CandidateElection Operations")
        ce_operation = st.radio("Choose CandidateElection Operation", ["View Data", "Insert Data", "Update Data", "Delete Data"])
        if ce_operation == "View Data":
            candidateelection_operations("View Data")
        elif ce_operation == "Insert Data":
            candidateelection_operations("Insert Data")
        elif ce_operation == "Update Data":
            candidateelection_operations("Update Data")
        elif ce_operation == "Delete Data":
            candidateelection_operations("Delete Data")

    elif selected_operation == "ElectionOfficial":
        st.header("ElectionOfficial Operations")
        eo_operation = st.radio("Choose ElectionOfficial Operation", ["View Data", "Insert Data", "Update Data", "Delete Data"])
        if eo_operation == "View Data":
            electionofficial_operations("View Data")
        elif eo_operation == "Insert Data":
            electionofficial_operations("Insert Data")
        elif eo_operation == "Update Data":
            electionofficial_operations("Update Data")
        elif eo_operation == "Delete Data":
            electionofficial_operations("Delete Data")

    elif selected_operation == "ParticipatedVoters":
        st.header("ParticipatedVoters Operations")
        pv_operation = st.radio("Choose ParticipatedVoters Operation", ["View Data", "Insert Data", "Update Data", "Delete Data"])
        if pv_operation == "View Data":
            participatedvoters_operations("View Data")
        elif pv_operation == "Insert Data":
            participatedvoters_operations("Insert Data")
        elif pv_operation == "Update Data":
            participatedvoters_operations("Update Data")
        elif pv_operation == "Delete Data":
            participatedvoters_operations("Delete Data")

    elif selected_operation == "PollingStation":
        st.header("PollingStation Operations")
        ps_operation = st.radio("Choose PollingStation Operation", ["View Data", "Insert Data", "Update Data", "Delete Data"])
        if ps_operation == "View Data":
            pollingstation_operations("View Data")
        elif ps_operation == "Insert Data":
            pollingstation_operations("Insert Data")
        elif ps_operation == "Update Data":
            pollingstation_operations("Update Data")
        elif ps_operation == "Delete Data":
            pollingstation_operations("Delete Data")
set_bg_hack("w.png")
    
if __name__ == "__main__":
    main()