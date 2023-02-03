# Welcome to Sumo Logic's Community Ecosystem Content Repository!

This repository and the content within it was created for anyone to use. The goal is to help reduce time to value and shed light on possibilities. Your contributions are welcome.

## DISCLAIMER

Please note the following before using this content:

1. Support for this content is provided by our community on a volunteer basis. Submit [GitHub Issues](https://github.com/SumoLogic/sumologic-content/issues) for bugs and enhancement requests.

2. This content is separate from our official [App Catalog](https://help.sumologic.com/docs/integrations/) unless otherwise noted. The content here is material that is not currently published to the [App Catalog](https://help.sumologic.com/docs/integrations/). Content that is published to the App Catalog or is no longer relevant will me migrated to the Retired Content folder in this repository.

## Table of Contents
- [Getting Started](#getting-started)
- [Using Content](#using-content)
- [Contributing](#Contributing)

## Getting Started
- There are two types of content here
	- Tools: There's a tool for every occasion; from managing your collectors and data volume to processing rules, and everyones favorite: regular expressions.

	- App and Collection Content: Content that helps extract instant value from a variety of data streams. This content typically includes pre-built dashboards, alerts, extraction rules, and steps for collection.

## Using Content
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- [Import](https://help.sumologic.com/docs/get-started/library/#import-content) the content to your desired folder location in Sumo Logic.

## Contributing
Please follow the guidelines outlined in the [Sumo Logic Community Content Submission](https://forms.gle/KQBLBuMuUw85xtRi9) form if you would like to contribute your own content to this repository and have our team review it for publishing.

**Alternative Submission:**

Follow the "fork-and-pull" Git workflow:
- **Fork** the repo on GitHub
- **Clone** the project to your own machine
- **Create** any new folders/subfolders necessary for your content
	- Add your content to these folders
	- Verify that all sensitive data has been removed BEFORE submitting a PR. This includes PII, Credentials, and Network data. Screenshots included (either blurr or mark over).
	- All application, dashboard and search content should be in JSON format (exported from Sumo Logic). Please use a descriptive naming convention (Company-Product-Function. Ex: AWS-Kinesis-Errors.json)
	- When possible, include a screenshot of your dashboards in .png or .jpg format. Name your screenshots the same as their respective JSON content. If there is more than one, please place these images in a Screenshots folder.
	- Create README.md file within each subfolder to track descriptions of the app, guidance on setting up the data collection, authors, versions, dates, and links to 3rd party docs
- **Commit** the changes on your local machine to your own fork/branch
- **Push** your work back up to your fork
- **Submit** a pull request so that we can review your changes and publish

## Commenting, Reviewing, and Rating Content:
Please provide a comment for content by following the guidelines below:

- Select the **Comments** folder within the Vendor/Product.
- Open the **Comments.json** file.
- Select Edit (pen icon).
- Add a new line below the current comments, and paste in your ratings/comments using the following schema:

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

Code owners will review and merge your rating of the content to the repo.

Please see [How to add a review/rating to an app](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#how-do-i-add-a-reviewrating-to-an-app) for more information.

## Frequently Asked Questions:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq) for more information.