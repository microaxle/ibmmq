import subprocess
import re
from datetime import datetime
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# This package helps us to accept and validate input flag values
import argparse
parser = argparse.ArgumentParser()

def get_certlist(prog, kdb_path):

    # Run gsk8capicmd command to list certificates
    command = [
        prog,
        '-cert',
        '-list',
        '-db', kdb_path,
        '-stashed'
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        lines = result.stdout.split('\n')
        certlist = []

        for line in lines:
        # Check if the line starts with '*', '-', '!', or '#' and doesn't contain the word 'key'
            if line.strip() and line[0] in ['*', '-', '!', '#'] and 'key' not in line.lower():
        # Extract the certificate label
                certificate_label = line.split()[-1]

              # Store the certificate label in the list
                certlist.append(certificate_label)
        return certlist


    except subprocess.CalledProcessError as e:
        print(f"Error executing gsk8capicmd: {e}")
        print("Make sure gsk8capicmd is available on your system and the paths are correct.")


def get_expiry(prog, kdb_path, certs, expiry):
    is_expiry_found = 'No'
    email_subject = f"QA - TLS-EXPIRY Report"

    # Create the HTML content dynamically based on the data
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }

            h2 {
                text-align: center;
                margin-top: 20px;
                color: #333;
            }

            table {
                border-collapse: collapse;
                width: 80%;
                margin: 0 auto;
                background-color: GhostWhite;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            th, td {
                border: 3px solid #ddd;
                padding: 12px;
                text-align: center;
            }

            th {
                background-color: #2196F3; /* Blue header background color */
                color: white; /* Header text color */
                font-weight: bold; /* Bold header text */
                text-transform: uppercase; /* Uppercase header text */
            }
        </style>
    </head>
    <body>
    """
    html_content += f"<h2>MQ TLS-EXPIRY Report</h2>"
    html_content += """
        <table>
            <tr>
                <th>Server</th>
                <th>Cert Name</th>
                <th>KDB Location</th>
                <th>Expiry Date</th>
                <th>Number of Days Remain</th>
            </tr>
        """

    for label in certs:
        command = [
        prog,
        '-cert',
        '-details',
        '-db', kdb_path,
        '-label', label,
        '-stashed'
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            expiry_date = re.search(r'Not After : (.+?[APMapm]{2})', result.stdout)

            if expiry_date:
                hostname = socket.gethostname()
                extracted_date_time = expiry_date.group(1)
                target_date = datetime.strptime(extracted_date_time, "%B %d, %Y %I:%M:%S %p")
                # Current date and time (replace this with the current date and time in your code)
                current_date = datetime.now()

                # Calculate the time difference
                time_difference = target_date - current_date

                # Extract the number of days
                remaining_days = time_difference.days

                #print(f"{hostname}  -- > {label}  -- > {extracted_date_time} -- > {remaining_days} days to expire")

                if int(remaining_days) <= int(expiry):
                    is_expiry_found = 'Yes'
                    html_content += f"""
                            <tr>
                                <td>{hostname}</td>
                                <td>{label}</td>
                                <td>{kdb_path}</td>
                                <td>{extracted_date_time}</td>
                                <td style="background-color: #f44336; color: white;">{remaining_days}</td>
                            """

            else:
                print("Date and time information not found.")


        except subprocess.CalledProcessError as e:
            print(f"Error executing gsk8capicmd: {e}")
            print("Make sure gsk8capicmd is available on your system and the paths are correct.")

    html_content += """
        </table>
        </body>
        </html>
     """

    if is_expiry_found == 'Yes':
         send_mail(html_content, email_subject)

def send_mail(html_content, emailsubject):
    msgPart = MIMEText(html_content, 'html')
    sendFrom = 'TLS-EXPIRY-Report@poloralphlauren.com'
    #sendTo = ['annu.singh@ralphlauren.com','akshit.gokhru@ralphlauren.com','sreekanth.gonugunta@ralphlauren.com']
    sendTo = ['DL-Group-IT-ESB-Middleware-Support@RalphLauren.com', 'annu.singh@ralphlauren.com', 'annu.singh@prolifics.com']
    # Create the root message and fill in the from, to, and subject headers
    msg = MIMEMultipart('alternative')
    msg['Subject'] = emailsubject
    msg['From'] = sendFrom
    msg['To'] = ', '.join(sendTo)
    msg.attach(msgPart)

    smtp = smtplib.SMTP('smtp1.poloralphlauren.com:25')
    smtp.sendmail(sendFrom, sendTo, msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    parser.add_argument("-b", "--binary", help="runmqakm command location  - It is Required Argument", required=True)
    parser.add_argument("-l", "--location", help="Location of the tls database - It is Required Argument", required=True)
    parser.add_argument("-e", "--expiry", help="expiry days  - It is Required Argument", required=True)

    # parse and store all the user arguments into 'args' variable
    args = parser.parse_args()

    certlist = get_certlist(args.binary, args.location)
    get_expiry(args.binary, args.location, certlist, args.expiry)


