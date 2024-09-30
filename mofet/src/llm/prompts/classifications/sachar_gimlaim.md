# GOAL: 
Given a conversation between soldiers/pre-recruits and a 'מיטב' representative, classify the conversation into the most appropriate category based on the list provided below. Use the keywords and definition in Hebrew associated with each category to guide your classification.
The conversation topic is about: """Pensioners' salary in hebrew: (שכר גמלאים)"""
definition of the topic: "Paying pensioners in salary payments to retirees from the IDF. 80% of the conversations are about the payslip."

Here are the categories available:
**Categories:**
---
| Index | categpry | Explanation |
|-------|----------|-------------|
| 1 | ביטוח לאומי | תאום ביטוח לאומי , ניכוי ביטוח לאומי |
| 2 | היוון | יתרת היוון, סיום היוון, תאריך לקיחת היוון, הפחתה עקב היוון , הלוואה משלימת היוון |
| 3 | חלוקת חסכון פנסיוני | תשלומי קצבה לגרושות |
| 4 | טפסים | טפסי 106, 161, 100  |
| 5 | מס הכנסה | סכום פטור, תאום מס, קיבוע זכויות  |
| 6 | מפרעות | הזנות שהוזנו לאחר גזירת שכר ניתן לבקש מפרעה  |
| 7 | קצבת שארים | חישוב אחוז קצבה |
| 8 | תעסוקה | דיווחים של מצבי תעסוקה כמו עובד, לא עובד |
| 9 | תשלומי פרישה | תשלומים שהתקבלו עקב פרישה כמו מענק פרישה, פדיון ימי מחלה |
---

# INSTRUCTION: Select the most appropriate category based on the conversation context and keywords.
# OUTPUT: The return should be ONLY the Index of the category selected. if you return something else rather than the INDEX ill be mad!!
## EXPECTED OUTPUT:
THE NUMBER OF THE CATEGORY YOU SELECTED TO BE THE MOST APPROPRIATE!

## OUTPUT EXAMPLES:
### OUTPUT:
1
### OUTPUT:
13
### OUTPUT:
6