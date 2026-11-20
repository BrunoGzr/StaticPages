import os

from markdown import extract_title, markdown_to_html_node


def generate_page(
    from_path: str,
    template_path: str,
    dest_path: str,
    basepath: str,
) -> None:
    print(
        f"Generating page from {from_path} to {dest_path} "
        f"using {template_path}"
    )

    with open(from_path, encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    basepath: str,
) -> None:
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(source_path):
            if source_path.endswith(".md"):
                generate_page(
                    source_path,
                    template_path,
                    dest_path[:-3] + ".html",
                    basepath,
                )
        else:
            generate_pages_recursive(
                source_path,
                template_path,
                dest_path,
                basepath,
            )
