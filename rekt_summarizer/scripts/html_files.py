filename_template = "{}.html"

for i in range(0, 19):
    filename = filename_template.format(i)

    with open(filename, "w") as file:
        pass  # No content to write
