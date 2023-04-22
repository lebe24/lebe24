# Introduction

A good Git commit message is crucial for effective collaboration and maintaining a high-quality codebase. It provides context, clarity, and understanding of the changes made to the code, which helps other developers understand the purpose and reasoning behind those changes

## Anatomy of a Git commit message
A Git commit message typically consists of three parts: the subject line, the body, and the footer.

## Subject Line
The subject line is the first and most important part of a commit message. It should be a brief summary of the changes made in the commit. The subject line should be no more than 50 characters long and should be written in the imperative tense (e.g., Add feature X rather than Added feature X). It should also be specific and informative, indicating what the commit does, rather than why it does it.

## Body
The body of a commit message should provide more detailed information about the changes made in the commit. It should be written in complete sentences and paragraphs, and should explain the reasoning behind the changes made. The body should be wrapped at 72 characters per line, and should be separated from the subject line by a blank line.

## Footer
The footer of a commit message is optional but can be used to provide additional information about the commit, such as the issue or bug tracker ID that the commit resolves, or any breaking changes that may have been introduced.

## Best practices for writing a good Git commit message

Use imperative mood in the title
Your commit message title should be written in the imperative mood, which gives it a clear and direct tone. This is because the title is essentially a command that tells other developers what the commit does.

## Example: Add new feature to dashboard

Use conventional commits
Conventional commits are a set of guidelines that help standardize commit messages across different projects. Following these guidelines can help make your commit messages more consistent and easier to read.

Example: ``` feat: add new feature to dashboard ```

## Provide context in the body
The body of your commit message should provide additional context about the changes made. This can include details about why the changes were made, how they were implemented, and any potential side effects.

Example:

``  Fix typo in README.md ``

## The typo was causing confusion for new users, so I corrected it to improve readability.

Use the footer for metadata and related issues
The footer of your commit message can be used to provide metadata about the changes made, such as related issues or pull requests. This can help other developers understand the context of the changes and find related information more easily.

Example:

```js
 Add new feature to dashboard

 Resolves #123 
 

This feature adds a new widget to the dashboard that displays real-time data about user activity.

````

## Using Git hooks to enforce commit message format

Git hooks are scripts that are run automatically by Git at certain points in the commit process. You can use Git hooks to enforce a specific commit message format, so that all messages follow a consistent structure. This can be helpful in ensuring that your commit messages are informative and easy to read.

To set up a Git hook to enforce a commit message format, you can create a pre-commit hook that checks the message and rejects the commit if it doesn't meet the specified format. For example, you can enforce a message format that includes a short summary of the changes, followed by a more detailed explanation of the changes, like this:

```
[summary] Brief summary of changes

[details] Detailed explanation of changes, including any relevant context or background information.

````

To create a pre-commit hook that enforces this format, you can create a script in the .git/hooks directory called pre-commit and add the following code:

````
#!/bin/sh

commit_msg_file=$1

if ! grep -q "\[summary\]" "$commit_msg_file"; then
    echo "Commit message must include [summary] tag"
    exit 1
fi

if ! grep -q "\[details\]" "$commit_msg_file"; then
    echo "Commit message must include [details] tag"
    exit 1
fi

````

This script will check that the commit message includes both a [summary] and a [details] tag, and will reject the commit if either tag is missing.

## Setting up a commit message template

Another way to ensure consistent commit messages is to set up a commit message template. This can be especially helpful if you have a large team working on the same codebase, as it ensures that everyone is following the same message format.

To set up a commit message template, you can create a file called .gitmessage in your home directory, and add the following content:

```
[summary]

[details]
```
Then, you can tell Git to use this file as a template for commit messages by running the following command:

git config ``--global commit.template ~/.gitmessage``

Now, every time you run git commit, Git will open your text editor with the commit message template pre-filled, making it easy to write a consistent message.