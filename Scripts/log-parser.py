import requests
import json

# Splunk API Credentials
splunk_host = "http://localhost:8089"
username = "admin"
password = "yourpassword"

# Queries for different security events
queries = {
    "failed_logins": 'search index=endpoint EventCode=4625 | table _time, Account_Name, Client_IP',
    "admin_logins": 'search index=endpoint EventCode=4672 | table _time, Account_Name, Logon_Type',
    "process_execution": 'search index=endpoint EventCode=1 | table _time, Parent_Process, New_Process, CommandLine'
}

# Function to run a Splunk query
def run_splunk_query(search_query):
    search_url = f"{splunk_host}/services/search/jobs"

    response = requests.post(
        search_url,
        auth=(username, password),
        data={"search": f"search {search_query}", "output_mode": "json", "exec_mode": "blocking"},
        verify=False
    )

    if response.status_code == 201:
        sid = response.json()["sid"]
        results_url = f"{splunk_host}/services/search/jobs/{sid}/results?output_mode=json"
        results_response = requests.get(results_url, auth=(username, password), verify=False)
        return results_response.json()
    else:
        print(f"Error: {response.text}")
        return None

# Run Queries & Store Results
log_data = {}

for key, query in queries.items():
    print(f"\nFetching results for: {key.replace('_', ' ').title()}")
    results = run_splunk_query(query)

    if results and "results" in results:
        log_data[key] = results["results"]

# Save logs to a JSON file
log_file_path = "/opt/splunk/scripts/splunk_log_results.json"
with open(log_file_path, "w") as log_file:
    json.dump(log_data, log_file, indent=4)

print(f"Results logged successfully at {log_file_path}.")
