# Context
You're given a conversation between soldiers/pre-recruits and a 'מיטב' representative. The military unit 'מיטב' is in charge of carrying out the selection and placement procedures for all those designated for security service ('מלש"ב') and the soldiers in the IDF.

## Your Task
Perform the following actions on the given text:

- **Reason for referral**: A description of the reason for the referral of the soldier/pre-recruit to the service center.
- **Identifying Unusual Events or Behaviors**: Monitor the conversation for any abnormal language or behavior, such as offensive language, signs of distress or a negative emotional state, excessive repetition, or deviation from expected norms like aggression or reluctance to provide information or disagreements. Summarize any unusual findings in up to two sentences, or state "תקין" if nothing unusual is observed.
- **Analyse and report the sentiment of the representative**: Choose strictly one word out of [חיובי, שלילי, ניטרלי].
- **Analyse and report the sentiment of the soldiers/pre-recruit**: Choose strictly one word out of [חיובי, שלילי, ניטרלי].
- **Categorized in a binary way yes/no whether an answer was given in a call or a referral to another party**: [כן, לא].
- **Analyse the service level of the representative**: Choose strictly one digit out of [1, 2, 3].
- **Analyse the soldiers/pre-recruit satisfaction level**: Choose strictly one digit out of [1, 2, 3].

## Output Schema Example
```json
{
    "Reason_for_referral": "String of max 1 sentences",
    "Unusual_events_or_behaviors": "String of max 2 sentences or 'תקין'",
    "sentiment_representative": "[חיובי, שלילי, ניטרלי]",
    "sentiment_caller": "[חיובי, שלילי, ניטרלי]",
    "referral_3_party":  "[כן, לא]",
    "representative_level": "[1, 2, 3]",
    "caller_satisfaction_level": "[1, 2, 3]"
}```

**Notes**:
- An example of an output for "Unusual_events_or_behaviors" could be: "The recruiter sounded stressed and showed signs of impatience"
- Always make sure to output this schema! or else I'll be MAD!
- Fill the fields in Hebrew! or else I'll be MAD!
- Before answering check that you produce the output schema and fill all the fields.
