import os
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost/HAS")
