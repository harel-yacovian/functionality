# GOAL: 
Given a conversation between soldiers/pre-recruits and a 'IDF' representative, classify the conversation into the most appropriate category based on the list provided below. Use the keywords and definition in Hebrew associated with each category to guide your classification.
The conversation topic is about: """Salary of a soldier serving in mandatory service salary in hebrew: (שכר שירות חובה)"""
definition of the topic: "Mandatory Service pay - subsistence allowances paid to soldiers in their mandatory service."

Here are the categories available:
**Categories:**
---
|   Index | categpry             | Explanation                                                                         |
|--------:|:---------------------|:------------------------------------------------------------------------------------|
|       1 | אחזקת דירה           | זכאויות בודד, זכאויות נשוי, הוצאת מפרעה.                                            |
|       2 | אישורים              | שליחת תלושים, ריכוז תשלומים                                                         |
|       3 | בודד                 | מענקים, שכר דירה, הוצאת מפרעה.                                                      |
|       4 | החזרי הוצאות         | החזרי הוצאות נסיעה, החזרי הוצאות לינה, החזרי הוצאות טיסה.                           |
|       5 | הפחתות               | בקשה להפחתה בעקבות הזנת חשבון לא תקין,יצירת חוב לאחר גזירה, העברת מפרעה לאחר גזירה. |
|       6 | חגים                 | תווים לחג, מפרעה על מענק לחג, בודד.                                                 |
|       7 | חובות                | שינוי דיווחים באופי / סוגי / מצבי שירות, תשלום חוב.                                 |
|       8 | חייל בודד            | זכאויות בודד, שכ"ד, אחזקת דיור, מענקים, מפרעות.                                     |
|       9 | כלכלה                | צליאק, משקית ת"ש(תנאי שירות ), הוצאת מפרעה.                                         |
|      10 | מענקים               | מענקי תש, מענקי שחרור, הוצאת מפרעות.                                                |
|      11 | מפרעות               | בקשת מפרעה, מועד תשלום.                                                             |
|      12 | מצבי שירות           | עריקות, מאסר, רגיל, דח"ש(דחיית שירות), הוצאת מפרעה                                  |
|      13 | סוג שירות            | דח"ש, חובה, מילואים, קבע, פטורים, הוצאת מפרעה.                                      |
|      14 | עתודאים              | תשלום / ניכוי מענקי עתידים, הוצאת מפרעה.                                            |
|      15 | קד"צ (קורס קדם צבאי) | תשלום / ניכוי דמי קד"צ(קורס קדם צבאי), הוצאת מפרעה.                                 |
|      16 | שכר דירה             | זכאות לשכ"ד, ירידה בשכ"ד בעקבות תשמ"ש, בודד, הוצאת מפרעה.                           |
|      17 | תוספת הוראה          | זכאות לתשלום, הוצאת מפרעה.                                                          |
|      18 | תוספת פעילות         | תשלום / ניכוי ברטרו, הוצאת מפרעה, זכאות ללוחם חוד.                                  |
|      19 | תשלומי משפחה         | זכאות לתשמ"ש(תשלומי משפחה ), גובה תקרת זכאות, הוצאת מפרעה, שכ"ד.                    |
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