import re
from pathlib import Path
from bs4 import BeautifulSoup
from pathlib import Path
from bs4 import BeautifulSoup
import re

def keep_only_speaker_from_doc(input_path, output_path, target_speaker="참석자 1"):
    input_path = Path(input_path)
    output_path = Path(output_path)

    raw = input_path.read_text(encoding="utf-8-sig", errors="replace")

    soup = BeautifulSoup(raw, "html.parser")
    text = soup.get_text("\n", strip=True)

    header_pattern = re.compile(
        r"참석자\s+(\d+)\s+((?:\d{1,2}:)?\d{1,2}:\d{2})"
    )

    matches = list(header_pattern.finditer(text))
    result_blocks = []

    for i, match in enumerate(matches):
        speaker = f"참석자 {match.group(1)}"
        time = match.group(2)

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        content = text[start:end].strip()
        content = re.sub(r"\s+", " ", content)

        if speaker == target_speaker:
            result_blocks.append(f"{speaker} {time}\n{content}")

    result = "\n\n".join(result_blocks)
    output_path.write_text(result, encoding="utf-8")

    return result


keep_only_speaker_from_doc(
    input_path="text.doc",
    output_path="attendee_1_only.doc",
    target_speaker="참석자 1"
)