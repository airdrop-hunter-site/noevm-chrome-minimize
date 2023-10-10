import os
import time
import sys
import traceback
from automation.ah_decode import get_metamask_wallet
from automation.selenium_driver import SeleniumDriver
from automation.logger import LogParams, print_log, get_time
from noevm.common.db_handler import DatabaseHandler

script_name = os.path.basename(__file__)
username = sys.argv[1]
use_local_db = sys.argv[2] if len(sys.argv) > 2 else None
script_status = 2
error = None

db_handler = DatabaseHandler('debank', username, use_local_db)

#############################################################
METAMASK_URL = 'chrome-extension://nfimekehkclodckkfiegpljgdbhbobfp/home.html'
URL = 'https://debank.com/ranking'


def test(selenium):
    selenium.driver.get(URL)
    time.sleep(2)
    selenium.close_windows_except(URL)



if __name__ == "__main__":
    start_time, start_utime = get_time()
    selenium = SeleniumDriver(debug_port=db_handler.debug_port).selenium

    try:
        db_handler.create_log('INFO', f'Starting {script_name}')
        ############################
        selenium.minimize_window(db_handler)
        test(selenium)

    except Exception as ex:
        db_handler.create_log('CRITICAL ERROR', f'{ex} for {username}')
        error_trace = traceback.format_exc().strip().split('\n')
        error = '\n'.join(error_trace)
        script_status = -1

    finally:
        db_handler.create_log('INFO', f'{script_name} finished')
        selenium.minimize_window(db_handler)
        end_time, end_utime = get_time()

        params = LogParams(
            table='Tx', db_handler=db_handler, status=script_status, error=error,
            script_name=script_name, username=username, wallet=get_metamask_wallet(username),
            start_time_tuple=(start_time, start_utime), end_time_tuple=(end_time, end_utime),
            summary='TEST'
        )

        print_log(params)
        if script_status == -1:
            sys.exit(1)
