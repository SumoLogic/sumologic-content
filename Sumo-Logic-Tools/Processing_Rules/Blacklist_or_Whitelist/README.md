You can use blacklisting and whitlisting (include and exclude) processing rules to specify what kind of data is sent to Sumo Logic.

- *Your rule must match the entire message, from the start to the end of any log message rather than addressing only a section.*
  - For single line messages, you must prefix and suffix the regex expression with .* if the matching string pattern is not at the beginning or end of the line
  - For multiline messages, add single line modifiers (?s) to the beginning and end of the expression to simplify matching your string, regardless of where it occurs in the message

- If you specifically exclude a message, it functions as a blacklist filter, and the data will never be sent to Sumo Logic.
- Include filters are whitelist filters, which can be useful when the list of log data you want to send to Sumo Logic is easy to filter. You can set up a whitelist filter instead of setting up exclude filters for all of the types of messages you'd like to exclude

For more information, see the documentation here:

Include and Exclude Rules: https://help.sumologic.com/Manage/Collection/Processing-Rules/Include-and-Exclude-Rules
