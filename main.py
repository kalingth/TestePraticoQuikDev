from APP import app
from MISC.CONSTANTS import HOST, MAIN_PORT
from MISC import DEPENDENCIES
import warnings

if __name__ == '__main__':
    warnings.simplefilter("ignore")
    DEPENDENCIES.createDatabaseIfNotExist()
    app.run(HOST, MAIN_PORT)

