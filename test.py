import sys

from automation.selenium_driver import SeleniumDriver
from noevm.common.db_handler import DatabaseHandler

username = sys.argv[1]
use_local_db = sys.argv[2] if len(sys.argv) > 2 else None
db_handler = DatabaseHandler('debank', username, use_local_db)

if __name__ == "__main__":
    selenium = SeleniumDriver(debug_port=db_handler.debug_port).selenium
    try:
        selenium.minimize_window(db_handler)
    except Exception as ex:
        print(f'{ex} for {username}')
    finally:
        selenium.minimize_window(db_handler)