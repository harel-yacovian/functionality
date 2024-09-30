import os
import json
from dotenv import load_dotenv
from logs.logger import setup_logger, log_decorator, session_gid_var
from mofet.src.llm.llm_utils import markdown_loader_cls, sub_domain_convertor_cls, tools
from openai.lib.azure import AzureOpenAI
load_dotenv()

logger = setup_logger()
client = AzureOpenAI(
    api_version=os.getenv("MOFET_AZURE_OPENAI_API_VERSION"),
    api_key=os.getenv("MOFET_AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("MOFET_AZURE_OPENAI_ENDPOINT"),
)

@log_decorator(show_args_calling=False, show_args_returning=False)
def classify_referral_reason_by_domain(domain: tuple, conversation_text: str) -> str:
    """
    Given the conversation topic, classify the conversation to the appropriate field.

    Parameters:
    - domain (tuple): A tuple containing the topic of the call and the field of interest.
    - conversation_text (str): The text of the conversation to be analyzed.

    Returns:
    - str: The classified sub-domain based on the conversation topic.

    This function uses a predefined prompt to classify the conversation to the appropriate field. It sends the conversation topic and text to the OpenAI API and receives a classification number. The classification number is then converted to a sub-domain using the `sub_domain_convertor_cls.convert` function.
    """
    system_prompt: str = markdown_loader_cls.get_prompt(domain[1])
    messages = [{'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': conversation_text}]

    response = client.chat.completions.create(model=os.getenv('MOFET_OPENAI_MODEL_ENGINE'),
                                              messages=messages,
                                              temperature=0,
                                              max_tokens=10)
    sub_domain_field_alias = int(response.choices[0].message.content)
    sub_domain = sub_domain_convertor_cls.convert(domain=domain[1], number=sub_domain_field_alias)
    return sub_domain
    pass

@log_decorator(show_args_calling=False, show_args_returning=False)
def summarize_conversation(domain: tuple, sub_domain: str, conversation_text: str) -> str:
    """
    Generates a summary of the conversation in 4 sentences.

    Parameters:
    - domain (tuple): A tuple containing the topic of the call and the field of interest.
    - sub_domain (str): The classified sub-domain based on the conversation topic.
    - conversation_text (str): The text of the conversation to be analyzed.

    Returns:
    - str: A summary of the conversation in 4 sentences.

    This function uses a predefined prompt to generate a summary of the conversation. It sends the conversation topic, classified sub-domain, and text to the OpenAI API and receives a summary.
    """
    system_prompt: str = markdown_loader_cls.get_prompt("summary")
    values = {
        "domain": domain[0],
        "Field of interest": sub_domain,
    }
    system_prompt = system_prompt.format(**values)
    messages = [{'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': conversation_text}]

    response = client.chat.completions.create(model=os.getenv('MOFET_OPENAI_MODEL_ENGINE'),
                                              messages=messages,
                                              temperature=0,
                                              max_tokens=500)
    conversation_summary = response.choices[0].message.content
    return conversation_summary
    pass

@log_decorator(show_args_calling=False, show_args_returning=False)
def extract_other_fields(domain: tuple, sub_domain: str, conversation_text: str) -> dict:
    """
    Extract other fields from the conversation.

    This function uses a predefined prompt to extract the following fields from the conversation:
    - support_description: A 1-2 sentence description of the actions taken by the representative during the call.
    - unusual_events: A summary of any abnormal language or behavior (such as cursing, bad language, bad attitude, or any unusual events) in up to two sentences, or 'תקין' if nothing unusual is observed.
    - representative_level: The service level of the representative, which can be either [1, 2, 3].
    - caller_satisfaction_level: The satisfaction level of the caller, which can be either [1, 2, 3].
    - issue_resolution_status: The issue resolution status, which can be either [0, 1] where 0 means not resolved and 1 means resolved.

    Parameters:
    - domain (tuple): A tuple containing the topic of the call and the field of interest.
    - sub_domain (str): The classified sub-domain based on the conversation topic.
    - conversation_text (str): The text of the conversation to be analyzed.

    Returns:
    - dict: A dictionary containing the extracted fields and their values.

    This function sends the conversation topic, classified sub-domain, and text to the OpenAI API and receives a summary. It then uses the extracted fields to create a dictionary and returns it.
    """
    system_prompt: str = markdown_loader_cls.get_prompt("conversation_other_fields_tool")
    system_prompt = system_prompt % (domain[0], sub_domain)
    messages = [{'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': conversation_text}]

    response = client.chat.completions.create(
        model=os.getenv('MOFET_OPENAI_MODEL_ENGINE'),
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "extract_conversation_fields"}},
        temperature=0,
        max_tokens=500
    )

    using_tool = response.choices[0].message.tool_calls
    if using_tool:
        tool_calls = response.choices[0].message.tool_calls[0]
        extracted_fields = json.loads(tool_calls.function.arguments)
        return extracted_fields
    else:
        raise ValueError("The model did not call the function or provide the necessary fields.")

@log_decorator(show_args_calling=False, show_args_returning=False)
def llm_pipline(domain: tuple, conversation_text: str) -> dict:
    """
     This function is a pipeline that takes a domain and a conversation text as input,
     and returns a dictionary containing the classified sub-domain, summary, and other extracted fields.

     Parameters:
     - domain (tuple): A tuple containing the topic of the call and the field of interest.
     - conversation_text (str): The text of the conversation to be analyzed.

     Returns:
     - dict: A dictionary containing the classified sub-domain, summary, and other extracted fields.

     This function first calls the `classify_referral_reason_by_domain` function to classify the conversation to the appropriate field.
     Then, it calls the `summarize_conversation` function to generate a summary of the conversation.
     Finally, it calls the `extract_other_fields` function to extract other fields from the conversation.
     The extracted fields are then added to the dictionary along with the classified sub-domain and summary.
     """
    sub_domain = classify_referral_reason_by_domain(domain=domain, conversation_text=conversation_text)
    summary = summarize_conversation(domain=domain, sub_domain=sub_domain, conversation_text=conversation_text)
    other_fields = extract_other_fields(domain=domain, sub_domain=sub_domain, conversation_text=conversation_text)
    other_fields["sub_domain"]= sub_domain
    other_fields["summary"] = summary
    return other_fields
