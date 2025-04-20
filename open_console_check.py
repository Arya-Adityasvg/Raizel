import os
import webbrowser

# Get the absolute path to the HTML file
html_path = os.path.abspath("browser_console_check.html")

# Convert to file:// URL
file_url = "file:///" + html_path.replace("\\", "/")

# Open in default browser
print(f"Opening {file_url} in your default browser...")
webbrowser.open(file_url)

print("If the browser didn't open automatically, please manually open this file:")
print(html_path) 