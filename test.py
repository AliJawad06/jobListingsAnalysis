import openai

openai.api_key = ""
# Upload a file
def upload_file(file_path):
    with open(file_path, "rb") as file:
        response = openai.File.create(
            file=file,
            purpose="assistants"  # Or "fine-tune" for model training
        )
    print("Uploaded File ID:", response["id"])
    return response["id"]

file_id = upload_file("your_file.pdf")  # Change to your file
