# Alexa News Headlines Skill
A simple Alexa Skill that reads the top headlines from BBC News written in Python and runs in AWS Lambda.
https://ewenchou.github.io/blog/2016/04/05/asking-for-news/

## Setup

Clone this repository and install the Python requirements __locally__ so that they can be uploaded to Lamba.

```
git clone https://github.com/ewenchou/alexa-news-headlines.git
cd alexa-news-headlines
pip install -t . -r requirements
```

Create a zip file of the contents of the project directory. You don't need to include:

    .git
    .gitignore
    intent_schema.json
    README.md
    requirements.txt
    utterances.txt

Everything else is needed, including the `.egg-info` directory that is created from the `pip install` command.

Upload the zip file to your AWS Lambda function, and setup your Alexa Skill in the Amazon developer portal.

For more details, refer to my [blog post](https://ewenchou.github.io/blog/2016/03/31/all-you-need-to-do-is-ask/) about developing Alexa Skills using ASK and Lambda, and my [post about this skill](https://ewenchou.github.io/blog/2016/04/05/asking-for-news/).
