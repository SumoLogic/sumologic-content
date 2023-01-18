Sumo Logic allows you to add Hashing rules to any source. You must specify a capture group so that the rule know which piece of the regex to mask.

Use Hashing instead of masking if you need to retain the uniquness of each value for use in reporting, for example (rather than making all values #### with a Maksing rule.)

Common use cases include masking Personally identifiable Information (PII) like:

Mask a credit card number
Mask a Social Security Number
Mask a Phone number, email, address, etc
For documentation, see here:

Hash Rules: https://help.sumologic.com/Manage/Collection/Processing-Rules/Hash-Rules
