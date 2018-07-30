PARSE_SCRIPT=./parse_yaml_secrets.py

export COSMOS_HOST=`$PARSE_SCRIPT host`
export COSMOS_KEY=`$PARSE_SCRIPT key`
export COSMOS_DATABASE=`$PARSE_SCRIPT database`
export COSMOS_COLLECTION=`$PARSE_SCRIPT collection`