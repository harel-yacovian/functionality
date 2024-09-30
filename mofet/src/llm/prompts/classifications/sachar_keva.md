# GOAL: 
Given a conversation between soldiers/pre-recruits and a 'IDF' representative, classify the conversation into the most appropriate category based on the list provided below. Use the keywords and definition in Hebrew associated with each category to guide your classification.
The conversation topic is about: """Permanent Salary (Permanent Salary for a Soldier who has signed beyond the mandatory duty) in hebrew: (שכר קבע)"""
definition of the topic: "Permanent salary deals with salary payments for permanent service members. 80% of the conversations are about the payslip."

Here are the categories available:
**Categories:**
---
| Index | categpry        | Explanation                                                                                  |
|-------|-----------------|----------------------------------------------------------------------------------------------|
| 1     | ברור חבויות     | קיצור שירות, חובות בגין שחרור                                                                 |
| 2     | דמי חכירה       | תשלומי רכב שכוללים מיסוי  וחכירת רכב                                                          |
| 3     | דרגת שכר        | רה דרוג (דרוגי ביניים)                                                                        |
| 4     | חבר             | שי לחגים, מלגות חבר, זכאות לחבר                                                               |
| 5     | טפסים           | טפסי 106, 161, 100                                                                           |
| 6     | מס הכנסה        | נקודות זיכוי, חישוב מס                                                                        |
| 7     | מענקים          | מענק התמדה, מענק סקטוריאלי, מענק שחרור, מענק נגד ימ"ח, מענקי לוחמים , מענקי מפקד          |
| 8     | מפרעות          | הזנות שהוזנו לאחר גזירת שכר ניתן לבקש מפרעה                                                  |
| 9     | מצב שרות        | חופשה ללא תשלום, חו"ל, חופשת לידה, חופשת לידה ללא תשלום , מאסר, מעצר                        |
| 10    | סוג שרות        | חובה בתנאי קבע, קבע, מילואים בתנאי קבע                                                      |
| 11    | תלושי שכר       | ניכויים רטרואקטיביים, ניכויים שוטפים, תשלומים שוטפים, התחייבויות ייזומות כגון הלוואות וביטוחים, השלמה לפריסת חוב |
| 12    | קופות           | מעבר בין קופות, הפקדות שלא התקבלו, אחוזי הפקדה מעסיק מועסק                                 |
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