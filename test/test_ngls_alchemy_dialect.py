import os
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect

####
# This simple test can be run as follows:
# 1. bash ngls.sh build superset --shillelagh
# 2. pushd /opt/ngls/build/shillelagh
# 3. . venv/bin/activate
# 4. export NGLS_API_KEY=<your NGLS api key>
# 5. export NGLS_SERVER=<your Ubuntu VM IP address or FQDN (ngls.mshome.net)>
# 6. python test/test_ngls_alchemy_dialect.py
# 7. deactivate
# 8. popd
# You can also load NGLS_API_KEY (step 4) and NGLS_SERVER (step 5) permanently in /etc/environment.
####

print("Starting test...")

if not os.getenv('NGLS_API_KEY'):
    os.environ['NGLS_API_KEY'] = '54c9681f44d544f1ac8fa48602081817'
ngls_api_key = os.getenv('NGLS_API_KEY')
print(f"Using api_key={ngls_api_key}")

if not os.getenv('NGLS_SERVER'):
    os.environ['NGLS_SERVER'] = '192.168.64.9'
ngls_server = os.getenv('NGLS_SERVER')
print(f"Using server={ngls_server}")

os.environ['CA_CERT_FILE'] = 'certs/ca.crt'

url = f"ngls://{ngls_server}:4443/reporting"
print(f"Creating engine with URL: {url}")
engine = create_engine(url)

print("Connecting the database engine")
connection = engine.connect()

print("list tables")
inspector = inspect(engine)
print(inspector.get_table_names())

print("get data")
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM calls_per_hour"))
    for row in result:
        print(row)

print("Test successfully completed")
