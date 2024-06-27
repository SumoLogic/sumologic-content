# Automation Tools

## Whats included:
1. Integration YAML File
2. Action YAML Files (Refer to "Action Descriptions" section below for details)

## Disclaimer
This integration is in active development. Actions, or the parameters defined therin may change in subsequent releases.

## To use the content:
- Download the Integration and Action YAML files to your local device.
- Create a new CloudSOAR integration by logging into CloudSOAR > going to Settings (⚙)(top right) > Automation > Integrations > Plus(+) icon > and selecting the Integration YAML file.
- Add any Actions you downloaded to that Integration by selecting the Upload icon (hover over the newly added integration), and uploading the Action YAML file(s).
- For more information on uploading custom Integrations/Actions and how to test them, please see [Working with integrations](https://help-opensource.sumologic.com/docs/cloud-soar/cloud-soar-integration-framework/#working-with-integrations).

## Action Descriptions
### Data Transform
- Provides various functions to more easily transform data in a playbook:
  - **String Input** - The value to transform.
  - **Transform Function** - Which string operation to use. Valid options are 'Split', 'Strip', 'Replace' or 'Regex'
      - **Split**: Splits a string into an array based on the delimiter provided in the "Transform Argument" parameter.
      - **Strip / lstrip / rstrip**: Removes leading and trailing characters from a string. Space is the default character to remove, unless specified otherwise in the "Transform Argument" parameter.
      - **Append**: Attaches a string to the end of a string (String Input > Transform Argument)
      - **Prepend**: Attaches a string to the beginning of a string (Transform Argument > String Input)
      - **Replace**: Replace a specified string/word/character with the value specified in the "Transform Argument" and "Replace" parameters.
      - **Regex Replace**: Replace a specified string/word/character with the value specified as a regular expression. This allows for user-provided value to be replace within the 'Transform Argument' and an user-provided value to be replace with in the 'Replace' argument.
      - **Regex**: Match a string with a regex pattern (python regex). Currently, this will return only the first capture group/match in an array. Could be further modified to accept an array num input.
      - **Encode UTF8 / Encode ASCII**: Encodes a string in UTF8 or ASCII formats
      - **Lowercase / Uppercase / Title Case / Capitalize**: Converts the case of a string based on the desired case type.
  - **Transform Argument** - Function input (e.g. regex pattern (w/ capture groups), replace argument (a,b) or split delimiter).
  - **Array Element** - Optional: if using 'split' function, select the element to return. Otherwise return the entire array.

### Filter IP Addresses
- Check a single IP, or list of IPs, and return a filtered list of IPs (sort into public IP and private IP lists).

### Signal Filter
-  Deconstructs a CSE Insight based on an assigned filter in order to retrieve specific field elements from the Signal Array that match the criteria.

### Deduplicate List
-  Allows you to deduplicate a list of values.

### Generate Password
- Generates a random password. Length and character makeup are configurable.

### Get Time
- Fetches the current time
  - Optionally returns the time elapsed from "now" when provided a timestamp to compare the current time with.

### Check Time Boundaries
- ALlows an event time input value and evaluates whether that time is within business hours. Configurable start and end times. 24-hour format. Can input different time formats (including Epoch) for the event time and select the timezone of the event (default is UTC).

### Chunk Unix Timestamps
- Evaluates two timestamps and chunks the timestamps based on the chunk value. Ex: Two timestamps (1 year apart) with 1 month chunks, will output 12 chunks

### Build JSON Object
- Provide the action with JSON key placeholder or string to build a new JSON object with the specified key/values.

### Buffer
- Takes a JSON string, or object and returns it as a JSON result. Helpful for dumping a JSON blob in string format and rendering in JSON format.

### Sleep
- Adds a configurable wait time to the execution of a playbook.

### Get Time
- Returns the current time and provides an option to compare this time to a user-provided timestamp, returning elapsed time.

### Add Prefix Suffix
- This action will allow a user to pass an input string and add a prefix and/or a suffix
  
### Escape String
- Escapes Input Strings that contain specific special characters

### Extract Domain from URL
- Extract the root domain from a URL or Email Address

### Render TextArea Field
- Uses a _textarea_ field to build a string using dynamic placeholders.

### String Regex
- Searches for the specified regular expression pattern and identifies all occurences. 

### Validate JSON
- Takes a text field and validates if the input is a valid JSON. If it is not a valid JSON then out puts the error and the exact input that it tested.

### Build Signal Output
- Must be used after a Get Insight V2 action from the the Sumo Logic CSE integration and then takes all signals from the output and converts it into a formated signal output to be used (example the output has been used in an email, ticketing system, or a notes section of the CSOAR incident) You can choose to either exclude or include any CSE schema fields: https://github.com/SumoLogic/cloud-siem-content-catalog/blob/master/schema/full_schema.md

- Exlude fields take precedence over include fields

- Must add the field singals to the output section of the Get Insight V2 action from the the Sumo Logic CSE integration

### Build Signal Output Break Lines
- This is the same as the Build Signal Output, but replaces break lines with new lines and properly escapes special characters to be used in a JSON value.

### Check Internal IP
- Allows an input of an IP or IP range to check weather it is internal or an external IP. Allows for additional user-provided IP's or ranges that should be classify as internal.

### Filter JSON Array
- When supplied with a array or JSON array, this action will filter based on a provided key/value.

### Render JSON Data
- Build a JSON payload using a 'Textarea' field; enables the use of placeholders to populate JSON.

### Decode Base64
- When supplied with a JSON payload containing a base64 encoded string (requires output.raw), this action will decode it into usable data. Uses 'upload' field type.

## To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).

## To add review/comment to content:
Please provide a review/comment for this content by following the guidelines below:

- Select the **Comments** folder.
- Open the **Comments.json** file.
- Select Edit (pen icon).
- Add a new line below the current comments, and paste in your review/comment using the following schema:

        {
            "reviewer":"[githubid/name]",
            "ratings":{
                "overall":4,
                "use-case":5,
                "design":4,
                "technical":4
            },
            "review":"This app is very useful for knowing x, y, and z. It would be great if the dashboards were broken out by use case instead of being one big dashboard."
        }


- Select **Propose New Changes**.
- Submit **Pull Request**.

Code owners will review and merge your comments on the content to the repo.

Please see [How to add a review/comment to an app](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#how-do-i-add-a-reviewrating-to-an-app) for more information.