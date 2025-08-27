import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Replace environment variables
    config['aixplain']['api_key'] = os.getenv('AIXPLAIN_API_KEY')
    return config

CONFIG = load_config()