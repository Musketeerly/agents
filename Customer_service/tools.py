from pydantic import BaseModel
from typing import Optional
import requests
import os
from dotenv import load_dotenv
from agents import function_tool

load_dotenv(override=True)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

airtable_token= os.getenv("AIRTABLE_TOKEN")
table_name= os.getenv("TABLE_NAME")
base_id= os.getenv("BASE_ID")

AIRTABLE_URL = f"https://api.airtable.com/v0/{base_id}/{table_name}"
HEADERS = {
    "Authorization": f"Bearer {airtable_token}",
    "Content-Type": "application/json"
}

@function_tool
def escalate_to_human(issue_summary:str):
    """Sends a Push Notification For escalation of issues."""
    payload = {"user": pushover_user, "token": pushover_token, "message": issue_summary}
    requests.post(pushover_url, data=payload)



# Tool 1: Get Customer by Email
# ----------------------------
@function_tool
def get_customer_info(email: str):
    
    params = {
        "filterByFormula": f"{{Email}}='{email}'",
        "maxRecords": 1
    }
    response = requests.get(AIRTABLE_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    
    if data.get("records"):
        return data["records"][0]  # Return first matching record
    else:
        return None

class FieldUpdate(BaseModel):
    Name: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Address: Optional[str] = None  # Add more fields as needed
    # Example:
    # Name: Optional[str] = None
    # Email: Optional[str] = None

@function_tool
def update_customer_by_email(email: str, fields: FieldUpdate) -> dict:
    """
    Look up a customer by email and update their information in the database.

    Args:
        email (str): Customer's email address.
        fields (dict): Fields to update.

    Returns:
        dict: Result of the update or an error message.
    """
    try:
        # Step 1: Search for the record by email
        search_url = f"{AIRTABLE_URL}?filterByFormula=LOWER(Email)='{email.lower()}'"
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()

        records = response.json().get("records", [])
        if not records:
            return {
                "status": "not_found",
                "message": f"No customer found with email: {email}. Please verify and try again or contact support."
            }

        # Step 2: Extract the record ID
        record_id = records[0]["id"]

        # Step 3: Update the customer record
        update_url = f"{AIRTABLE_URL}/{record_id}"
        payload = {"fields": fields.dict(exclude_none=True)}
        update_response = requests.patch(update_url, headers=HEADERS, json=payload)
        update_response.raise_for_status()

        updated_fields = update_response.json().get("fields", {})
        return {
            "status": "success",
            "message": "Customer record updated successfully.",
            "updated_fields": updated_fields
        }

    except requests.exceptions.HTTPError:
        return {
            "status": "error",
            "message": "A problem occurred while accessing the database. Please try again or escalate."
        }

