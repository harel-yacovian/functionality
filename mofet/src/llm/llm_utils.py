import os


class MarkdownLoader:
    def __init__(self, directory="./mofet/src/llm/prompts"):
        """
        Initialize the MarkdownLoader with a directory path.

        Parameters:
        directory (str): The path to the directory containing .md files.
        """
        self.directory = directory
        self.files_content = {}
        self.load_markdown_files()

    def load_markdown_files(self):
        """Load all .md files from the specified directory and its subdirectory."""
        self._load_files_from_directory(self.directory)
        classification_dir = os.path.join(self.directory, "classifications")
        if os.path.exists(classification_dir) and os.path.isdir(classification_dir):
            self._load_files_from_directory(classification_dir)

    def _load_files_from_directory(self, directory):
        """Helper function to load .md files from a given directory."""
        for filename in os.listdir(directory):
            if filename.endswith(".md"):
                file_path = os.path.join(directory, filename)
                encodings = ['utf-8', 'latin-1', 'iso-8859-1']
                file_content = None
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as file:
                            file_content = file.read()
                        break
                    except UnicodeDecodeError:
                        continue
                if file_content is not None:
                    self.files_content[filename] = file_content
                else:
                    print(f"Failed to read {file_path} with available encodings")

    def get_prompt(self, prompt_name):
        """
        Get the content of a loaded .md file by its filename.

        Parameters:
        filename (str): The name of the .md file.

        Returns:
        str: The content of the file if found, else None.
        """
        prompt_name = prompt_name + ".md"
        return self.files_content.get(prompt_name)

    def describe_files(self):
        """
        Describe the available .md files loaded.

        Returns:
        list: A list of filenames of the loaded .md files.
        """
        return [filename.rsplit('.', 1)[0] for filename in self.files_content.keys()]


class SubDomainConverter():
    """
    A class for converting sub-domain numbers to their corresponding domain names.

    Attributes:
        convert_hash (dict): A dictionary containing the mapping of sub-domain numbers to their corresponding domain names.

    Methods:
        __init__(self):
            Initializes the SubDomainConverter object.

        convert_sub_number_to_sub_domain(self, domain:str , number:int)-> str:
            Converts a given sub-domain number to its corresponding domain name.
    """
    def __init__(self):
        self.convert_hash = {
            "credit": {
                1: "ניכויים",
                2: "בירור זכאויות",
                3: "פירעון הלוואה",
                4: "ייעול הלוואות",
                5: "הפניות"
            },
            "sachar_ezrach_oved_zahal": {
                1: "אירועי אי נוכחות",
                2: "אישורים",
                3: "אתר צה\"ל",
                4: "דוחות תעסוקה",
                5: "דיווחים כלליים",
                6: "השלמה לפריסת חוב",
                7: "חובות",
                8: "מס הכנסה",
                9: "מפרעות",
                10: "פנסיה מבטחים הותיקה",
                11: "קופות וקרנות",
                12: "רכב",
                13: "שכר עידוד",
                14: "שעות נוספות",
                15: "תאונת עבודה",
                16: "תלושי שכר"
            },
            "sachar_gimlaim": {
                1: "ביטוח לאומי",
                2: "היוון",
                3: "חלוקת חסכון פנסיוני",
                4: "טפסים",
                5: "מס הכנסה",
                6: "מפרעות",
                7: "קצבת שארים",
                8: "תעסוקה",
                9: "תשלומי פרישה"
            },
            "sachar_hova": {
                1: "אחזקת דירה",
                2: "אישורים",
                3: "בודד",
                4: "החזרי הוצאות",
                5: "הפחתות",
                6: "חגים",
                7: "חובות",
                8: "חייל בודד",
                9: "כלכלה",
                10: "מענקים",
                11: "מפרעות",
                12: "מצבי שירות",
                13: "סוג שירות",
                14: "עתודאים",
                15: "קד\"צ (קורס קדם צבאי)",
                16: "שכר דירה",
                17: "תוספת הוראה",
                18: "תוספת פעילות",
                19: "תשלומי משפחה"
            },
            "sachar_keva": {
                1: "ברור חבויות",
                2: "דמי חכירה",
                3: "דרגת שכר",
                4: "חבר",
                5: "טפסים",
                6: "מס הכנסה",
                7: "מענקים",
                8: "מפרעות",
                9: "מצב שרות",
                10: "סוג שרות",
                11: "תלושי שכר",
                12: "קופות"
            },
            "sachar_meloim": {
                1: "אישורים",
                2: "בנקים",
                3: "גביית חובות",
                4: "חרבות ברזל (מלחמת חרבות ברזל)",
                5: "מענק רשות המיסים",
                6: "נסיעות",
                7: "קצבאות",
                8: "תגמול",
                9: "תלושי שכר"
            },
            "vacation": {
                1: "קנסות",
                2: "בירורי זכאויות",
                3: "בקשות חריגות",
                4: "הטבות",
                5: "ערעורים",
                6: "קבלת מידע"
            }
        }

        pass


    def convert(self, domain:str , number:int)-> str:
        """
        Converts a given sub-domain number to its corresponding domain name.

        Parameters:
        domain (str): The domain for which the sub-domain number is given.
        number (int): The sub-domain number to be converted.

        Returns:
        str: The corresponding domain name for the given sub-domain number.

        Raises:
        KeyError: If the given sub-domain number does not exist in the dictionary.
        """
        return self.convert_hash[domain][number]
        pass

def Domain_convert_hash(domain):
    hash = {}
    return hash.get(domain)



tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_conversation_fields",
            "description": "Extract key fields from the conversation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "support_description": {
                        "type": "string",
                        "description": "Provide a 2-3 sentence description of the actions taken by the representative during the call. replay in Hebrew!",
                    },
                    "unusual_events": {
                        "type": "string",
                        "description": "Monitor the conversation for any abnormal language or behavior, such as cursing, bad language, bad attitude, or any unusual events. Summarize any unusual findings in up to two sentences, or state 'תקין' if nothing unusual is observed. replay in Hebrew!",
                    },
                    "representative_level": {
                        "type": "integer",
                        "enum": [1, 2, 3],
                        "description": "Analyze the service level of the representative and choose strictly one digit out of [1, 2, 3]",
                    },
                    "caller_satisfaction_level": {
                        "type": "integer",
                        "enum": [1, 2, 3],
                        "description": "Analyze the satisfaction level of the caller and choose strictly one digit out of [1, 2, 3]",
                    },
                    "issue_resolution_status": {
                        "type": "integer",
                        "enum": [0, 1],
                        "description": "Determine whether the issue was resolved during the call or if further action is needed. Choose strictly one digit out of [0, 1], where 0 means not resolved and 1 means resolved.",
                    },
                },
                "required": ["support_description", "unusual_events", "representative_level", "caller_satisfaction_level", "issue_resolution_status"],
            },
        },
    }
]


markdown_loader_cls = MarkdownLoader()
sub_domain_convertor_cls =SubDomainConverter()