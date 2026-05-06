import re
from enum import Enum

from parentnode import ParentNode
from textnode import TextType, TextNode
from textnode import text_node_to_html_node, TextNode
from leafnode import LeafNode

class BlockType(Enum):
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'
    PARAGRAPH = 'paragraph'

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(
                f"Invalid Markdown syntax: missing closing delimiter '{delimiter}' in text: '{node.text}'"
            )

        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                if part:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last = 0
        for m in pattern.finditer(text):
            if m.start() > last:
                prefix = text[last:m.start()]
                if prefix:
                    new_nodes.append(TextNode(prefix, TextType.TEXT))
            alt = m.group(1)
            url = m.group(2)
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last = m.end()

        if last < len(text):
            tail = text[last:]
            if tail:
                new_nodes.append(TextNode(tail, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = re.compile(r'(?<!\!)\[(.*?)\]\((.*?)\)')

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last = 0
        for m in pattern.finditer(text):
            if m.start() > last:
                prefix = text[last:m.start()]
                if prefix:
                    new_nodes.append(TextNode(prefix, TextType.TEXT))
            link_text = m.group(1)
            url = m.group(2)
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last = m.end()

        if last < len(text):
            tail = text[last:]
            if tail:
                new_nodes.append(TextNode(tail, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    filtered_blocks = []

    for block in blocks:
        block = block.strip()
        if block:
            filtered_blocks.append(block)

    return filtered_blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6}", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    if all(line.startswith(">") or line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("-") or line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r'^\d+\.\s', line) for line in lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    normalized = text.replace("\n", " ")
    text_nodes = text_to_textnodes(normalized)
    html_nodes = [text_node_to_html_node(tn) for tn in text_nodes]
    return html_nodes


def block_to_html_node(block, block_type):
    if block_type == BlockType.HEADING:
        m = re.match(r'^(#{1,6})\s+(.*)', block, re.S)
        if m:
            level = len(m.group(1))
            content = m.group(2).replace("\n", " ")
            children = text_to_children(content)
            return ParentNode(f'h{level}', children)
        else:
            return ParentNode('p', text_to_children(block.replace("\n", " ")))

    if block_type == BlockType.CODE:
        code_text = re.sub(r'^```(\n)?', '', block)
        code_text = re.sub(r'```$', '', code_text)
        code_leaf = LeafNode('code', code_text)
        return ParentNode('pre', [code_leaf])

    if block_type == BlockType.QUOTE:
        lines = [line.lstrip('>').strip() for line in block.split("\n")]
        content = " ".join(lines)
        children = text_to_children(content)
        return ParentNode('blockquote', children)

    if block_type == BlockType.UNORDERED_LIST:
        items = []
        for line in block.split("\n"):
            item_text = re.sub(r'^-\s*', '', line).strip()
            item_text = item_text.replace("\n", " ")
            items.append(ParentNode('li', text_to_children(item_text)))
        return ParentNode('ul', items)

    if block_type == BlockType.ORDERED_LIST:
        items = []
        for line in block.split("\n"):
            item_text = re.sub(r'^\d+\.\s*', '', line).strip()
            item_text = item_text.replace("\n", " ")
            items.append(ParentNode('li', text_to_children(item_text)))
        return ParentNode('ol', items)

    return ParentNode('p', text_to_children(block.replace("\n", " ")))


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        children.append(node)
    return ParentNode('div', children)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("No title found")
