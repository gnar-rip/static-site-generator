from textnode import TextNode, TextType
import re
from block import BlockType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:  
            result.append(old_node)
            continue
        
        text = old_node.text

        if delimiter not in text:
            result.append(old_node)
            continue

        segments = []
        remaining_text = text

        while delimiter in remaining_text:
            start_index = remaining_text.find(delimiter)
            before_text = remaining_text[:start_index]

            after_opening = remaining_text[start_index + len(delimiter):]
            end_index = after_opening.find(delimiter)
            if end_index == -1:
                raise ValueError(f"No closing delimiter '{delimiter}' found")
            
            between_text = after_opening[:end_index]
            
            remaining_text = after_opening[end_index + len(delimiter):]
            
            if before_text:
                segments.append((before_text, TextType.NORMAL_TEXT))
            segments.append((between_text, text_type))
    
        if remaining_text:
            segments.append((remaining_text, TextType.NORMAL_TEXT))
            
        for text, node_type in segments:
            result.append(TextNode(text, node_type))
    
    return result

def split_nodes_images(old_nodes):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            result.append(old_node)
            continue
        
        matches = list(re.finditer(r'!\[(.*?)\]\((.*?)\)', old_node.text))
        
        if not matches:
            result.append(old_node)
            continue
            
        current_index = 0

        for match in matches:
            start, end = match.start(), match.end()
            alt_text = match.group(1)
            link = match.group(2)
            
            if current_index < start:
                before_text = old_node.text[current_index:start]
                result.append(TextNode(before_text, TextType.NORMAL_TEXT))
                
            result.append(TextNode(alt_text, TextType.IMAGE_TEXT, link))
            current_index = end
        
        if current_index < len(old_node.text):
            remaining_text = old_node.text[current_index:]
            if remaining_text.strip():
                result.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
    
    return result

def split_nodes_link(old_nodes):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            result.append(old_node)
            continue
        
        matches = list(re.finditer(r'\[(.*?)\]\((.*?)\)', old_node.text))
        
        if not matches:
            result.append(old_node)
            continue
            
        current_index = 0

        for match in matches:
            start, end = match.start(), match.end()
            alt_text = match.group(1)
            link = match.group(2)
            
            if current_index < start:
                before_text = old_node.text[current_index:start]
                result.append(TextNode(before_text, TextType.NORMAL_TEXT))
                
            result.append(TextNode(alt_text, TextType.LINK_TEXT, link))
            current_index = end
        
        if current_index < len(old_node.text):
            remaining_text = old_node.text[current_index:]
            if remaining_text.strip():
                result.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
    
    return result