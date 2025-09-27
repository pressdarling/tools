#!/usr/bin/env python3
import json
import sys
import argparse


def extract_json_structures(text):
    """
    Extract all valid JSON objects or arrays from text using a state machine parser.

    Returns a list of valid JSON objects/arrays as Python objects.
    """
    result = []
    i = 0
    text_length = len(text)

    while i < text_length:
        # Look for the start of a potential JSON object or array
        if text[i] == "{":
            # Try to parse a complete JSON object starting at this position
            potential_json, end_pos = parse_json_object(text, i)
            if potential_json is not None:
                try:
                    # Directly parse without fixing - invalid JSON will be rejected
                    parsed_obj = json.loads(potential_json)
                    result.append(parsed_obj)
                except json.JSONDecodeError:
                    pass
                # Skip to the end of this object to avoid finding nested objects
                i = end_pos
            else:
                i += 1
        elif text[i] == "[":
            # Try to parse a complete JSON array starting at this position
            potential_json, end_pos = parse_json_array(text, i)
            if potential_json is not None:
                try:
                    # Directly parse without fixing - invalid JSON will be rejected
                    parsed_obj = json.loads(potential_json)
                    result.append(parsed_obj)
                except json.JSONDecodeError:
                    pass
                # Skip to the end of this array to avoid finding nested objects
                i = end_pos
            else:
                i += 1
        else:
            i += 1

    return result


def parse_json_object(text, start_pos):
    """
    Parse a JSON object starting at start_pos.

    Returns (json_string, end_position) if successful, or (None, start_pos) if not.
    """
    i = start_pos
    if i >= len(text) or text[i] != "{":
        return None, start_pos

    # State variables
    brace_count = 1  # We already found the first '{'
    in_string = False
    escape_next = False

    # Start accumulating the JSON string
    json_str = text[i]
    i += 1

    while i < len(text) and brace_count > 0:
        char = text[i]
        json_str += char

        # Handle string state
        if in_string:
            if escape_next:
                escape_next = False
            elif char == "\\":
                escape_next = True
            elif char == '"':
                in_string = False
        else:
            # Only count braces outside of strings
            if char == '"':
                in_string = True
            elif char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                # If we've closed all braces, we have a potential complete JSON object
                if brace_count == 0:
                    return json_str, i + 1

        i += 1

    # If we got here, we didn't find a complete JSON object
    return None, start_pos


def parse_json_array(text, start_pos):
    """
    Parse a JSON array starting at start_pos.

    Returns (json_string, end_position) if successful, or (None, start_pos) if not.
    """
    i = start_pos
    if i >= len(text) or text[i] != "[":
        return None, start_pos

    # State variables
    bracket_count = 1  # We already found the first '['
    in_string = False
    escape_next = False

    # Start accumulating the JSON string
    json_str = text[i]
    i += 1

    while i < len(text) and bracket_count > 0:
        char = text[i]
        json_str += char

        # Handle string state
        if in_string:
            if escape_next:
                escape_next = False
            elif char == "\\":
                escape_next = True
            elif char == '"':
                in_string = False
        else:
            # Only count brackets outside of strings
            if char == '"':
                in_string = True
            elif char == "[":
                bracket_count += 1
            elif char == "]":
                bracket_count -= 1
                # If we've closed all brackets, we have a potential complete JSON array
                if bracket_count == 0:
                    return json_str, i + 1

        i += 1

    # If we got here, we didn't find a complete JSON array
    return None, start_pos


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Extract JSON objects and arrays from text."
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=str,
        default=None,
        help="File to read (defaults to stdin)",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Output all JSON structures found, not just the best one",
    )
    args = parser.parse_args()

    # Read the input
    if args.file:
        try:
            with open(args.file, "r") as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()

    # Extract JSON structures
    json_structures = extract_json_structures(text)

    # Output the results
    if not json_structures:
        print("No valid JSON structures found.", file=sys.stderr)
        sys.exit(1)

    if args.all:
        # Output all objects
        output = json_structures
    else:
        # Output the best (most complex) object
        output = max(json_structures, key=lambda x: len(json.dumps(x)))

    # Always print with 2-space indent
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()