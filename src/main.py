from textnode import TextNode, TextType

def main():
    # Create a TextNode instance with example values
    node = TextNode("Example text", TextType.LINK_TEXT, "https://example.com")
    # Print its representation
    print(repr(node))

# Call the main function to execute the script
if __name__ == "__main__":
    main()
