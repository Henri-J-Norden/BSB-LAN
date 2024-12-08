import sys
import argparse
import requests
import os

from translate_abbrev import get_abbrev


def split_file(file_path, *, chunk_size=400, skip_lines=0):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    return [lines[i:i + chunk_size] for i in range(skip_lines, len(lines), chunk_size)]


def process_chunk(chunk, api_key):
    abbrev_str = ''.join(f'\n\t{a}' for a in get_abbrev())
    system_message = (
        "Translate the given Siemens Boiler-System-Bus parameters from German to English. "
        "This is for a safety-critcal system, so there is zero tolerance for inaccuracies in any technical terms. "
        "For any lines where the an accurate translation cannot be guaranteed "
        "(e.g. because the meaning is not clear), output a comment (`// ...`) instead. "
        "\n\nHere is a list of known abbreviations in the format `((<German abbreviation>, <German explanation>), (<English abbreviation>, <English explanation>))`: "
        f"```{abbrev_str}\n```"
        "\nUse the given English abbreviation where appropriate. "
        "If the English abbreviation is empty (`""`), then DO NOT ABBREVIATE - use the English explanation instead."
        "\n\nOnly capitalize the first word. Output ONLY the complete translated lines (e.g. `#define ...`) plus comments & whitespace, without any other text (no introductions). Do not truncate.")
    chunk_text = ''.join(chunk)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": chunk_text}
        ],
        # for best/deterministic output
        "temperature": 0,
        "top_p": 1,
        "top_k": 1,
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']


def main():
    parser = argparse.ArgumentParser(description="Process file with OpenRouter API")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument("--lines_per_chunk", default=300, type=int, help="Number of lines per chunk sent to OpenRouter API")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Please set the OPENROUTER_API_KEY environment variable.")
        sys.exit(1)

    if os.path.exists(args.output_file):
        with open(args.output_file, 'r') as existing_file:
            skip_lines = len(existing_file.readlines())
    else:
        skip_lines = 0

    chunks = split_file(args.input_file, chunk_size=args.lines_per_chunk, skip_lines=skip_lines)

    with open(args.output_file, 'a') as out_file:
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}/{len(chunks)}...")
            result = process_chunk(chunk, api_key)
            for c, r in zip(chunk, result.split("\n")):
                print(f"{c.strip(): <60.60}  ->  {r}")

            out_file.write(result + "\n")
            out_file.flush()
            # TODO: remove last line from result, if following check fails
            assert len(result.split("\n")) == len(chunk)
            pass

    print(f"Results written to {args.output_file}")


if __name__ == "__main__":
    main()
