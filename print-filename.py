import subprocess
from pathlib import Path

def generate_tree_lines(directory: Path, prefix: str = "") -> list[str]:
    lines = []
    try:
        entries = sorted(list(directory.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        return [f"{prefix}└── [存取權限不足]"]

    total = len(entries)
    for index, entry in enumerate(entries):
        is_last = (index == total - 1)
        connector = "└── " if is_last else "├── "
        sub_prefix = prefix + ("    " if is_last else "│   ")

        if entry.is_dir():
            lines.append(f"{prefix}{connector} [{entry.name}]")
            lines.extend(generate_tree_lines(entry, sub_prefix))
        else:
            lines.append(f"{prefix}{connector} {entry.name}")
    return lines

def copy_to_clipboard(text: str):
    """使用 Windows 內建 clip 指令將文字寫入剪貼簿"""
    try:
        process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, close_fds=True)
        process.communicate(input=text.encode("utf-8"))
        print("\n已成功複製到剪貼簿！")
    except Exception as e:
        print(f"\n複製失敗: {e}")

def save_to_markdown(directory: Path, content: str):
    """將樹狀清單輸出為 Markdown 檔案"""
    folder_name = directory.resolve().name or "root"
    output_file = directory / f"[{folder_name}]file-name.md"
    try:
        md_content = f"# {folder_name}\n\n```text\n{content}\n```\n"
        output_file.write_text(md_content, encoding="utf-8")
        print(f"\n已成功輸出 Markdown 檔案：{output_file.resolve()}")
    except Exception as e:
        print(f"\n輸出 Markdown 失敗: {e}")

def main():
    folder_str = input("請輸入資料夾路徑: ").strip('"\'')
    root_path = Path(folder_str)

    if not root_path.is_dir():
        print("指定的路徑不存在或不是資料夾！")
        return

    # 生成樹狀清單
    output_lines = [f"[Root directory] {root_path.resolve()}"]
    output_lines.extend(generate_tree_lines(root_path))
    full_result = "\n".join(output_lines)

    # 螢幕印出
    print("\n" + full_result + "\n")

    # 詢問是否複製
    choice = input("是否將結果複製到剪貼簿？(y/n): ").strip().lower()
    if choice == "y":
        copy_to_clipboard(full_result)
    else:
        print("已略過複製。")

    # 詢問是否輸出為 Markdown 檔案
    choice_md = input("是否輸出為 Markdown 檔案？(y/n): ").strip().lower()
    if choice_md == "y":
        save_to_markdown(root_path, full_result)
    else:
        print("已略過輸出 Markdown。")

if __name__ == "__main__":
    main()

    main()