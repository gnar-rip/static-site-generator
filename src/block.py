from enum import Enum

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if markdown.startswith(("#", "##", "###", "####", "#####", "######") and markdown[markdown.find('#') + 1] == " "):
        return BlockType.heading
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.code
    elif all(line.startswith(">") for line in lines):
        return BlockType.quote
    elif all(line.startswith("- ") for line in lines):
        return BlockType.unordered_list
    elif markdown[0].isdigit() and markdown[1] == ".":
        for i, line in enumerate(lines, 1):
            expected_prefix = f"{i}. "
            if not line.startswith(expected_prefix):
                break   
    else:
        return BlockType.paragraph

