# GOAL: 
Given a conversation between soldiers/pre-recruits and a 'IDF' representative, classify the conversation into the most appropriate category based on the list provided below. Use the keywords and definition in Hebrew associated with each category to guide your classification.
The conversation topic is about: """Salary of a citizen working in the army, in hebrew: (שכר אזרח עובד צה"ל)"""
definition of the topic: "Salary of a civilian employee of the IDF - deals with the payment of the salary of civilian employees of the IDF, most of the calls are salary inquiries"

Here are the categories available:
**Categories:**
---
| Index | categpry | Explanation |
|-------|----------|-------------|
| 1 | אירועי אי נוכחות | מה אירועי אי נוכחות שדווחו |
| 2 | אישורים | אישור סיום העסקה, טפסי 161, 106, 100, אישורי ביטוח לאומי |
| 3 | אתר צה"ל | לא מצליח להתחבר, לא רואה תלוש באתר |
| 4 | דוחות תעסוקה | האם דווח דוח תעסוקה, האם הדוח שדווח תקין |
| 5 | דיווחים כלליים | האם בוצע דיווח מסויים במערכת  |
| 6 | השלמה לפריסת חוב | מה זה אומר השלמה לפריסת חוב, למה זה נוצר |
| 7 | חובות | מדוע נוצר חוב |
| 8 | מס הכנסה | האם הניכוי תקין, איך מחושב, תאום מס, פטור ממס, החזר מס |
| 9 | מפרעות | בקשות למפרעות |
| 10 | פנסיה מבטחים הותיקה | אישור למשיכת כספים ממבטחים הותיקה |
| 11 | קופות וקרנות | אי ביצוע הפקדה, אי התאמה בין הפקדה בתלוש לבין דוח הפקדות |
| 12 | רכב | מדוע לא שולמו תוספות רכב, מדוע לא שולם סכום מלא, החזר ביטוחי רכב |
| 13 | שכר עידוד | מה אחוז פרמיה שדווח, האם חושב תקין |
| 14 | שעות נוספות | האם דווח שעות נוספות, כיצד חושב תשלום |
| 15 | תאונת עבודה | אישור לביטוח לאומי, למה יש ניכוי מקדמה |
| 16 | תלושי שכר | הסבר על התשלומים בתלוש, למה יש ניכוי |
---

# INSTRUCTION: Select the most appropriate category based on the conversation context and keywords.
# OUTPUT: The return should be ONLY the Index of the category selected. if you return something else rather than the INDEX ill be mad!!
## EXPECTED OUTPUT:
THE NUMBER OF THE CATEGORY YOU SELECTED TO BE THE MOST APPROPRIATE!

## OUTPUT EXAMPLES:
### OUTPUT:
1
### OUTPUT:
4
### OUTPUT:
6