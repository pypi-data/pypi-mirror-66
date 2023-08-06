import pkg_resources
from datetime import datetime

year = datetime.now().year
BRANDING = f"""                            _                _____
      /\                   | |       /\     |_   _|
     /  \     ____   __ _  | |_     /  \      | |
    / /\ \   |_  /  / _` | | __|   / /\ \     | |
   / ____ \   / /  | (_| | | |_   / ____ \   _| |_
  /_/    \_\ /___|  \__,_|  \__| /_/    \_\ |_____|

  Copyright {year} Azat Artificial Intelligence, LLP
  ******v2t:  version {pkg_resources.require('v2t')[0].version}   azat.ai info@azat.ai
"""

if __name__ == '__main__':
    print(BRANDING)