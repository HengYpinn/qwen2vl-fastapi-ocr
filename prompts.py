# prompts.py

PROMPTS = {
    "ic": (
        "Analyze the image and respond with key information in RESTful API JSON format. If the image is a Malaysian IC, extract: fullName, icNumber, address, nationality, and gender."
    ),

    "passport": (
        "Input: a scan or photo of a passport.\n"
        "Task: Extract exactly these fields as JSON:\n"
        "  \"fullName\": string,\n"
        "  \"passportNumber\": string,\n"
        "  \"nationality\": string,\n"
        "  \"dateOfBirth\": string (ISO 8601 date),\n"
        "  \"expiryDate\": string (ISO 8601 date),\n"
        "Then assess authenticity and include:\n"
        "  \"authenticityConfidence\": float  (0.0=fake, 1.0=real)\n"
        "Output: Valid JSON only. No markdown, no prose, no explanations.\n"
    ),

    "receipt": (
        "Input: a photo or PDF of a cash-deposit or bank-transfer receipt.\n"
        "Task: Extract exactly these fields as JSON:\n"
        "  \"date\": string (ISO 8601 date),\n"
        "  \"time\": string (HH:MM:SS),\n"
        "  \"referenceNumber\": string,\n"
        "  \"totalAmount\": number,\n"
        "  \"currency\": string (ISO 4217 code),\n"
        "  \"senderAccountNumber\": string,\n"
        "  \"senderName\": string,\n"
        "  \"receiverAccountNumber\": string,\n"
        "  \"receiverName\": string,\n"
        "  \"accountType\": string,\n"
        "  \"transactionType\": string,\n"
        "  \"branchName\": string\n"
        "Output: Valid JSON only. No markdown, no prose, no explanations.\n"
    ),
}
