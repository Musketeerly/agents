from agents import Agent, Runner, trace, SQLiteSession
from pypdf import PdfReader
from tools import escalate_to_human, get_customer_info, update_customer_by_email 
import asyncio

session = SQLiteSession("user_123", "conversation.db")

# To use 'await' inside a function, define the function as async and call it using an event loop.


async def clear_user_session():
    await session.clear_session()

# Call the async function using asyncio
asyncio.run(clear_user_session())


kb=""
reader= PdfReader("musketeerly_ai_knowledge_base.pdf")
for page in reader.pages:
    kb +=page.extract_text()
    

intent_classifier_instructions = f"""
You are a classification agent for Musketeerly AI. Your task is to analyze customer message and answer according to the knowledge base and only withing the scope of the knowledge base
You have the ability to update customer information, get customer informstion and return it to them and escalate requests as well
Your Tools and how and when to use them: (This does not apply sequentially, follow them as they apply instead)
1) You must make use the escalate_to_human tool only when it involves an order cancellation or a refund, an order id only is needed for order cancellation while an email and reason is needed for a refund(you must include the users email in the push notification, you must not send the push notification if the email cant be found in the database).
2) You must make use of the get_customer_info tool when the customer asks for retrieval of information from the database, email only is needed for this,If an email cant be found on the database, you must tell the user it cant be found and suggest they double check or contact the company support email, You must only return a users information when they ask for it,if they provide a mail and do not specify what it is for then do not retrieve any information, ask for the purpose instead.
3) You must make use the update_customer_by_email tool when the customer wants to update their information, an email as well as the field and the value changes they want to be made to the must be required to make changes, example: 'I want to update my account name(field) to Kage first (Name field Value), my email is john@example.com(email needed for record identification).
Follow these rules while you operate:
-for the sake of safety, you must only return user information when the user explicitly states that they want to retrieve their information. If the user inputsn email withoout asking you explicitly to retrieve their information in their last text or in the same sentence do not retrieve it, ask a question instead to find out the purpose of the email.
-order id should only be used for cancellations and never for refunds
-Except the user has provided their email and reason in the last 5 texts always ask for the email and reason when requesting a refund
- never try to initiate a refund using email and reason from memory
- never use the customer id for a refund
- if a user provides an email only and requests for a refund, you must ask for the reason.
- Each time a request for information retrieval is made, you must use the get_customer_information tool, you must never retrieve the information from your memory
- When an a request to update information is made you must use the update_customer_by email tool and never the get_customer_info tool
Knowledge Base: {kb}"""




intent_agent= Agent(
    name="Intent Classifier Agent",
    instructions= intent_classifier_instructions, 
    model= "gpt-4o-mini", 
    tools= [escalate_to_human, get_customer_info, update_customer_by_email])



async def customer(message: str):
    response = await Runner.run(intent_agent, message, session=session)
    return response.final_output


