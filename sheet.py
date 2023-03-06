import gspread
from oauth2client.service_account import ServiceAccountCredentials

def writeSheet():

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('VisitorLog')

    sheet = spreadsheet.sheet1

    sheet.update_cell(1, 1, "Name")
    sheet.update_cell(1, 2, "Type")
    sheet.update_cell(1, 3, "Time")
    
    with open('log.csv', 'r') as file:
        content = file.read()
        client.import_csv(spreadsheet.id, data=content)
        
writeSheet()