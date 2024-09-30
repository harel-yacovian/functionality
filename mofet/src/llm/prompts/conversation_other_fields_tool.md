# Context
You're given a conversation between a client and a 'מופת' representative regarding %s. The 'מופת' call center is responsible for providing financial information and assistance to all military personnel, including regular soldiers, reservists, permanent service members, and IDF civilian employees. The conversation pertains to %s.

## Your Task
You must call the function "extract_conversation_fields" to perform the following actions on the given text:

- **support_description**: Provide a 2-3 sentence description of the actions taken by the representative during the call.
- **unusual_events**: Monitor the conversation for any abnormal language or behavior, such as cursing, bad language, bad attitude, or any unusual events. Summarize any unusual findings in up to two sentences, or state "תקין" if nothing unusual is observed.
- **representative_level**: Analyze the service level of the representative and choose strictly one digit out of [1, 2, 3].
- **caller_satisfaction_level**: Analyze the satisfaction level of the caller and choose strictly one digit out of [1, 2, 3].
- **issue_resolution_status**: Determine whether the issue was resolved during the call or if further action is needed. Choose strictly one digit out of [0, 1], where 0 means not resolved and 1 means resolved.

## **Notes**:
- An example of an output for "unusual_events" could be: "The client used offensive language and showed signs of frustration."
- Always make sure to output this schema! or else I'll be MAD!
- Fill the fields in Hebrew! or else I'll be MAD!