from textnode import TextNode, TextType

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
            
            # Extract text between delimiters
            between_text = after_opening[:end_index]
            
            # Update remaining text
            remaining_text = after_opening[end_index + len(delimiter):]
            
            # Add segments
            if before_text:
                segments.append((before_text, TextType.NORMAL_TEXT))
            segments.append((between_text, text_type))
        
        # Add any remaining text after the last delimiter
        if remaining_text:
            segments.append((remaining_text, TextType.NORMAL_TEXT))
            
        # Create TextNode objects from segments
        for text, node_type in segments:
            result.append(TextNode(text, node_type))
    
    return result