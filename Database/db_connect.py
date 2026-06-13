import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Dynamically locate the folder where this script lives
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "connection.env")

# 2. Load your custom environment file explicitly from that folder
load_dotenv(env_path)

# 3. Extract the credentials securely
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Safety check: ensure the keys are actually loading
if not url or not key:
    raise ValueError(f"Missing SUPABASE_URL or SUPABASE_KEY\nChecked: {env_path}")

# 4. Initialize the live connection client
supabase: Client = create_client(url, key)

print(" Successfully linked your backend to the live Supabase cloud!")