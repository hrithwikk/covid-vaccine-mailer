# covid-vaccine-mailer
- Sends a mail of available no of doses at vaccination centers searched on Cowin website.
- This code is written using python, and utilises the Selenium and SMTP library. 
- The selenium part scrapes the vaccination information from https://www.cowin.gov.in, for the added pincode inside the code.
- SMTP is used to mail the information on a tabular form to a given email id.
- Present version only extracts the information for the current date.
- I made this code to execute only when I do so, however, automation can be done fairly easy using APscheduler or other libraries.
- If you are facing issues in sending mail (authorisation error) allow less secure apps in the security options of your account you're logging in to send the email.


