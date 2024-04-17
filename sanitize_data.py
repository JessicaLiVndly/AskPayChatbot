import json
import sys
import os

CHANNEL_ID = 'CTL6NALUF'


def sanitize_data(absolute_file_path):
    with open(absolute_file_path, 'r') as f:
        data = json.load(f)

    sanitized_data = []

    for item in data:

        if "replies" in item:
            messages = [reply["text"] for reply in item["replies"]]
            url = f"https://vndly.slack.com/archives/{CHANNEL_ID}/p{item['ts'].replace('.', '')}"
            sanitized_item = {
                "url": url,
                "messages": messages
            }
            # ignore threads with no replies
            if len(messages) > 1:
                sanitized_data.append(sanitized_item)

    directory, _ = os.path.split(absolute_file_path)
    output_file = os.path.join(directory, 'slack_sanitized.json')
    with open(output_file, 'w') as f:
        json.dump(sanitized_data, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sanitize.py input_file.json")
        sys.exit(1)

    filename = sys.argv[1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'slack_data', filename)
    sanitize_data(file_path)
