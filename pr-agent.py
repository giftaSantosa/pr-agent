from anthropic import Anthropic
import os

client = Anthropic()

tools = [
    {
        "name": "read_file",
        "description": "Read a text file and return its contents. Use this when the user asks about a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path to the file, e.g. notes.txt"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "draft_comment",
        "description": "Save the final PR comment as a draft for human approval. Call this once when the comment is complete.",
        "input_schema": {
            "type": "object",
            "properties": {
                "body": {"type": "string", "description": "The full PR comment in markdown"}
            },
            "required": ["body"],
        }
    }
]

SYSTEM_PROMPT = """
You are a Senior Engineer reviewing a pull request. You write PR comments that summarize changes for reviewers.
When finished, call draft_comment with the final comment. Do not write the comment as plain text.

From the diff, write a comment with these sections:
- **Summary**: one sentence on what this PR does.
- **Why**: the problem it solves. Only state what the diff supports; if unclear, write "Not clear from the diff."
- **Changes**: bullets per file, describing behavior, not line-by-line edits.
- **Review focus**: risky spots a reviewer should check (edge cases, side effects).

Rules:
- Use read_file if the diff lacks context.
- Max 8 bullets total. No praise, no filler.
- Don't invent intent or tickets that aren't in the diff.
- If you cannot read the diff, do not call draft_comment. Reply in plain text explaining what failed.

<example>
**Summary**
Adds rate limiting to the login endpoint.

**Why**
Repeated failed logins were not throttled, which allows brute-force attempts.

**Changes**
- `sessions_controller.rb`: blocks login for 15 minutes after 5 failed attempts per email.
- `user.rb`: adds `failed_attempts` counter and `locked_until` timestamp.
- `db/migrate/...`: adds both columns to `users`.

**Review focus**
- Counter resets only on successful login. Confirm that's intended.
- Lockout is per email, not per IP, so one attacker can lock out any user.
</example>
"""

# response = client.messages.create(
#     model="claude-sonnet-5-5",
#     max_tokens=1000,
#     tools=tools,
#     messages=[{"role": "user", "content": "notes.txt"}],
# )

# file_text = open(response.content[0].input["path"]).read()

# messages = [
#     {"role": "user", "content": "Summarize notes.txt"},
#     {"role": "assistant", "content": response.content},
#     {"role": "user", "content": [
#         {"type": "tool_result", "tool_use_id": response.content[0].id, "content": file_text}
#     ]},
# ]

# response2 = client.messages.create(
#     model="claude-sonnet-5-5",
#     max_tokens=1000,
#     tools=tools,
#     messages=messages,
# )

# for block in response2.content:
#     if block.type == "text":
#         print(block.text)

# refactor

messages = [{"role": "user", "content": "Review diff2.txt"}]

drafts = []

for i in range(10):
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason != "tool_use":
        break

    results = []
    for block in response.content:
        if block.type == "tool_use":
            print(block.name, block.input)
            if block.name == "read_file":
                path = os.path.normpath(block.input["path"])
                if path.startswith(("..", "/")):
                    output = "Access denied: path is outside the project."
                else:
                    try:
                        output = open(path).read()
                    except FileNotFoundError:
                        output = "File not found."
            elif block.name == "draft_comment":
                drafts.append(block.input["body"])
                output = "Draft saved"
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})

    messages.append({"role": "user", "content": results})

for block in response.content:
    if block.type == "text":
        print(block.text)

for draft in drafts:
    print(draft)
    if input("Post? (y/n) ").strip().lower() == "y":
        print("Posted!")
    else:
        print("Skipped.")
