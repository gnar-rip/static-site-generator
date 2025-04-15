from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

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
    
def split_markdown_into_blocks(markdown):
    blocks = []
    current_block = []
    lines = markdown.strip().split("\n")
    in_code_block = False

    for line in lines:
        if line.strip() == "```":
            in_code_block = not in_code_block
            current_block.append(line)  
            if not in_code_block:
                blocks.append("\n".join(current_block))
                current_block = []      
        elif in_code_block:
            current_block.append(line)   
        elif not line.strip():
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []        
        else:
            current_block.append(line)
    if current_block:
        blocks.append("\n".join(current_block))
        
    return blocks

def markdown_to_html_node(markdown):
    # Split the markdown into blocks
    blocks = split_markdown_into_blocks(markdown)
    
    # Create a parent div to hold all blocks
    parent_node = HTMLNode("div", None, None, [])
    
    # Process each block
    for block in blocks:
        # Determine the type of block
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.paragraph:
            # Strip leading/trailing whitespace and create paragraph node
            text = block.strip()
            paragraph_node = HTMLNode("p", None, None, text_to_children(text))
            parent_node.children.append(paragraph_node)
            
        elif block_type == BlockType.heading:
            # Count the number of # at the beginning to determine heading level
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
                    
            # Strip the # and whitespace, then create heading node
            text = block[level:].strip()
            heading_node = HTMLNode(f"h{level}", None, None, text_to_children(text))
            parent_node.children.append(heading_node)
        elif block_type == BlockType.code:
            # For code blocks, we don't process inline markdown
            # Extract code without the ``` markers
            lines = block.split('\n')
            code_text = '\n'.join(lines[1:-1]) if lines[-1].strip() == "```" else '\n'.join(lines[1:])
            
            # Create text node for code content (no inline parsing)
            code_text_node = TextNode(code_text, TextType.NORMAL_TEXT)
            code_html_node = text_node_to_html_node(code_text_node)
            
            # Create code and pre nodes
            code_node = HTMLNode("code", None, None, [code_html_node])
            pre_node = HTMLNode("pre", None, None, [code_node])
            parent_node.children.append(pre_node)
            
        elif block_type == BlockType.quote:
            # Strip leading > and whitespace, then create quote node
            lines = block.split('\n')
            quote_lines = []
            for line in lines:
                if line.startswith('>'):
                    # Remove the > and one space if it exists
                    if len(line) > 1 and line[1] == ' ':
                        quote_lines.append(line[2:])
                    else:
                        quote_lines.append(line[1:])
                else:
                    quote_lines.append(line)
            
            quote_text = '\n'.join(quote_lines).strip()
            quote_node = HTMLNode("blockquote", None, None, text_to_children(quote_text))
            parent_node.children.append(quote_node)
            
        elif block_type == BlockType.unordered_list:
            list_node = HTMLNode("ul", None, None, [])
            lines = block.split('\n')
            
            for line in lines:
                # Remove the leading "- " or "* " and create list item
                if line.strip().startswith("- ") or line.strip().startswith("* "):
                    # Extract the text after the marker
                    item_text = line.strip()[2:].strip()
                    item_node = HTMLNode("li", None, None, text_to_children(item_text))
                    list_node.children.append(item_node)
            
            parent_node.children.append(list_node)
            
        elif block_type == BlockType.ordered_list:
            list_node = HTMLNode("ol", None, None, [])
            lines = block.split('\n')
            
            for line in lines:
                # Check for pattern like "1. " and create list item
                stripped = line.strip()
                if len(stripped) >= 3 and stripped[0].isdigit() and stripped[1] == '.' and stripped[2] == ' ':
                    # Find where the actual content starts
                    start_idx = stripped.find(' ') + 1
                    item_text = stripped[start_idx:].strip()
                    item_node = HTMLNode("li", None, None, text_to_children(item_text))
                    list_node.children.append(item_node)
            
            parent_node.children.append(list_node)
    
    return parent_node

def text_to_children(text):
    # Convert text to TextNodes with inline markdown processing
    text_nodes = text_to_textnodes(text)
    
    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    
    return html_nodes
