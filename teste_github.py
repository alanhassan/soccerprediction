import pandas as pd
import requests
import base64
from io import StringIO
import creds


# Step 3: Create or load your Pandas DataFrame
data = {'Column1': [1, 2, 3, 4, 5, 6], 'Column2': ['A', 'B', 'C', 'D', 'E', 'F']}
df_test_github2 = pd.DataFrame(data)

# Convert DataFrame to CSV in-memory
csv_data = StringIO()
df_test_github2.to_csv(csv_data, index=False)
csv_content = csv_data.getvalue()

# Encode content to Base64
encoded_content = base64.b64encode(csv_content.encode()).decode()

# GitHub repository details
username = 'alanhassan'
repository = 'soccerprediction'
file_name = 'df_test_github2.csv'  # Specify the desired file name

# Check if the file exists
url_get = f'https://api.github.com/repos/{username}/{repository}/contents/{file_name}'
headers_get = {'Authorization': f'token {creds.token}'}

response_get = requests.get(url_get, headers=headers_get)
response_get_json = response_get.json()

# Extract the SHA from the response
current_sha = response_get_json.get('sha')

# Step 4: Push data directly to GitHub using GitHub API
url_put = f'https://api.github.com/repos/{username}/{repository}/contents/{file_name}'
headers_put = {
    'Authorization': f'token {creds.token}',
    'Content-Type': 'application/json'
}

data_put = {
    'message': f'Update {file_name}',
    'content': encoded_content
}

# If the file exists, update it; otherwise, create it
if current_sha is not None:
    data_put['sha'] = current_sha

response_put = requests.put(url_put, headers=headers_put, json=data_put)

if response_put.status_code == 200:
    print(f'Data pushed to {file_name} on GitHub successfully!')
elif response_put.status_code == 201:
    print(f'{file_name} created on GitHub successfully!')
else:
    print(f'Error: {response_put.status_code}, {response_put.text}')
