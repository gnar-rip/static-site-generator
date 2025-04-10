from block import *

def test_block_to_block_type():
    # Test for heading
    assert block_to_block_type("# Heading") == BlockType.heading
    assert block_to_block_type("## Subheading") == BlockType.heading

    # Test for code block
    assert block_to_block_type("```\nCode\n```") == BlockType.code

    # Test for quote
    assert block_to_block_type("> This is a quote") == BlockType.quote

    # Test for unordered list
    assert block_to_block_type("- Item 1\n- Item 2") == BlockType.unordered_list

    # Test for ordered list
    assert block_to_block_type("1. Item 1\n2. Item 2") == BlockType.ordered_list

    # Test for paragraph
    assert block_to_block_type("This is a paragraph.") == BlockType.paragraph
    assert block_to_block_type("Another paragraph.") == BlockType.paragraph
    assert block_to_block_type("This is a paragraph\nwith multiple lines.") == BlockType.paragraph
    assert block_to_block_type("This is a paragraph with a list:\n- Item 1\n- Item 2") == BlockType.paragraph