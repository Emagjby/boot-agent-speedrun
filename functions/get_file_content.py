def get_file_content(working_directory, file_path):
    import os

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        LIMIT = 10000
        content = ""
        with open(target_file, "r") as f:
            content = f.read(LIMIT)
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {LIMIT} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
