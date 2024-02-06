import requests
import os
from bs4 import BeautifulSoup

server_url = 'http://localhost:12349'

while True:
    operation_prompt = "Please select a operation.\n1.list\n2.upload\n3.download"
    print(operation_prompt)

    operation = input()

    if operation == 'list':
        response = requests.get(f'{server_url}/list')
        files = response.json()
        print("files:")
        for file in files:
            print(file)
    elif operation == 'upload':
        filename = input('Enter the filename: ')
        with open(filename, 'rb') as file:
            response = requests.post(f'{server_url}/upload/{filename}', data=file)
        print(response.text)
    elif operation == 'download':
        filename = input('Enter the filename: ')
        response = requests.get(f'{server_url}/download/{filename}')
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print('File downloaded successfully')
        else:
            print('Failed to download file')