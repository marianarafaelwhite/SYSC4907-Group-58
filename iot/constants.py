"""
File to store constants
"""

LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Hardware related
POLL_TIME_SECS = 2
HUMIDITY_MIN = 20
HUMIDITY_MAX = 80
HUMIDITY_THRESHOLD = 40
CO2_MIN = 400
CO2_MAX = 8192
CO2_THRESHOLD = 750
GENERATE_DANGER = 1

# Thingspeak related
AIR_QUALITY_WRITE_KEY = 'ROK806WNRUKNAUZ0'
AIR_QUALITY_READ_KEY = 'S79PK540791M3LGE'
AIR_QUALITY_FEED = '1293661'
CO2_FIELD = 'field2'
HUMIDITY_FIELD = 'field3'
GOOD_STATUS = 200
READ_URL = 'https://api.thingspeak.com/channels/' + \
           '{CHANNEL_FEED}/feeds.json?api_key=' + \
           '{READ_KEY}&timezone=America%2FNew_York'

# Thingspeak is limited in how many writes (15 sec interval)
# Consider multithreading or a queue to eliminate
# This sleep on the Pi's side
# Or consider paying for 1 sec delay
# Set to 20 to leave room since
THINGSPEAK_DELAY_SECS = 20

# DB related
HUMIDITY_DB_FILE = 'humidity.db'
HUMIDITY_TABLE = 'humidity'
CO2_DB_FILE = 'co2.db'
CO2_TABLE = 'co2'

# Email related
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_PASSWORD = 'MC&Dx78K'
GMAIL_USERNAME = 'covid.smart.home.alert@gmail.com'
CO2_SUBJECT = 'COVID Risk: High CO2 levels'
CO2_CONTENT = """
    CO2 is {co2} ppm, which is high.<br>
    High CO2 increases the risk of COVID19 transmission.<br>
    Take action to prevent the spread of COVID19."""
HUMIDITY_SUBJECT = 'COVID Risk: Low humidity levels'
HUMIDITY_CONTENT = """
    Humidity is {humidity} %, which is low.<br>
    Low humidity increases the risk of COVID19 transmission.<br>
    Take action to prevent the spread of COVID19."""
SENDER = 'COVID Risk Alert System'
CONTENT_HTML = """
    <html>
      <head></head>
      <body>
        <p>Hi,<br><br>
           {body}<br><br>
           Best,<br>
           {sender}</b>
        </p>
      </body>
    </html>"""

# TODO: Find a better way to register individuals for notifications
RECIPIENTS = ['marianarafaelwhite@cmail.carleton.ca']
