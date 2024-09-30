import os
from logs.logger import setup_logger, log_decorator, session_gid_var
from meitav.src.helpers.utilities import rtxt_file, extract_json_from_string
from openai.lib.azure import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

logger = setup_logger()
client = AzureOpenAI(
    api_version=os.getenv("MEITAV_AZURE_OPENAI_API_VERSION"),
    api_key=os.getenv("MEITAV_AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("MEITAV_AZURE_OPENAI_ENDPOINT"),
)


class Summarizer:
    """ add the option to return a list of possibilities"""

    def __init__(self, template_path="./meitav/src/prompts/SummerizePrompt_v2.md",
                 load_from_folder=True):
        self.template = rtxt_file(template_path)

    # @log_decorator(show_args_calling=True, show_args_returning=True)
    def run_chain_summarizer(self, prompt: str):
        template = self.template
        template = template.replace("{conversation}", prompt)

        response = client.chat.completions.create(
            model=os.getenv('MEITAV_OPENAI_MODEL_ENGINE'),
            messages=[{"role": "user", "content": template}],
            temperature=0.1,
            top_p=0.95,
            max_tokens=600,
            frequency_penalty=0,
            presence_penalty=0
        )
        res_ = response.choices[0].message.content
        return res_

class Semantics:
    def __init__(self, template_path="./meitav/src/prompts/SentimentPrompt.md",
                 load_from_folder=True):
        self.template = rtxt_file(template_path)
        self.engine = os.getenv("ENGINE")


    @log_decorator(show_args_calling=False, show_args_returning=False)
    def run_chain_semantic(self, prompt: str):
        template = self.template
        response = client.chat.completions.create(
            model=os.getenv('MEITAV_OPENAI_MODEL_ENGINE'),
            messages=[{"role": "system", "content": template},
                      {"role": "user", "content": prompt}],
            temperature=0,
            top_p=0.95,
            max_tokens=800,
            # response_format={"type": "json_object"}
        )
        res_ = response.choices[0].message.content
        return res_
    pass

class Classifier:
    def __init__(self, template_path="./meitav/src/prompts/ClassifierPrompt.md",
                 load_from_folder=True):
        self.template = rtxt_file(template_path)
        self.decoder = ['איתור ומיון', 'בני-ישיבות', 'ברה"ן', 'גיוס', "גיוס שלב ב' וג' חרבות ברזל", 'כללי', 'כנס הבת הדתייה', 'לחימה-נשים', 'מנהל אוכלוסיות', 'מנעד הכשירות', 'מסלול תתקדמו', 'מצטיינים', 'סדיר', 'סיירות ולחימה', 'עתודה אקדמית', 'עתודה טכנולוגית', 'פניה מהאפליקציה', 'פסיכוטכני', 'פרט', 'קהילה', 'רב-קו', 'רפואי', 'תכנון ומיצוי']
        self.engine = os.getenv("ENGINE")

    @log_decorator(show_args_calling=False, show_args_returning=False)
    def run_chain_classifier(self, prompt: str):
        template = self.template
        response = client.chat.completions.create(model=os.getenv('MEITAV_OPENAI_MODEL_ENGINE'),
            messages=[{"role": "system", "content": template},
                      {"role": "user", "content": prompt}],
            temperature=0,
            top_p=0.95,
            max_tokens=100
        )
        res_ = response.choices[0].message.content
        result_category = self.decoder[int(res_)]
        return result_category

    pass


def conversation_summerizer(txt, gid):
    session_gid_var.set(gid)
    summary = Summarizer_.run_chain_summarizer(prompt=txt)
    return summary

def conversation_analyzer(txt, gid):
    session_gid_var.set(gid)

    sentiment = Semantics_.run_chain_semantic(prompt=txt)
    json_file = extract_json_from_string(input_str=sentiment)
    return json_file


def conversation_classifier(txt, gid):
    session_gid_var.set(gid)

    category = Classifier_.run_chain_classifier(prompt=txt)
    return category

Summarizer_ = Summarizer()
Semantics_ = Semantics()
Classifier_ = Classifier()

