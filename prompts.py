PROMPTS = {
    "ic": (
        "You are an OCR JSON extractor.\n"
        "Extract the following fields from this Malaysian IC image:\n"
        "  - fullName\n"
        "  - icNumber\n"
        "  - address\n"
        "  - nationality\n"
        "  - gender\n\n"
        "Then analyze whether the IC looks genuine or counterfeit and include:\n"
        "  - authenticityConfidence  (float 0.0–1.0)\n\n"
        "Respond with valid JSON only.\n\n"
    ),

    "passport": (
        "You are an OCR JSON extractor.\n"
        "Extract these fields from this passport image:\n"
        "  - fullName\n"
        "  - passportNumber\n"
        "  - nationality\n"
        "  - dateOfBirth\n"
        "  - expiryDate\n\n"
        "Then analyze whether the passport appears authentic or fabricated and include:\n"
        "  - authenticityConfidence  (float 0.0–1.0)\n\n"
        "Respond with valid JSON only.\n\n"
    ),

    "receipt": (
        "You are an OCR JSON extractor.\n"
        "Extract these fields from this cash-deposit or bank-transfer receipt image:\n"
        "  - date\n"
        "  - time\n"
        "  - referenceNumber\n"
        "  - totalAmount\n"
        "  - currency\n"
        "  - senderAccountNumber\n"
        "  - senderName\n"
        "  - receiverAccountNumber\n"
        "  - receiverName\n"
        "  - accountType\n"
        "  - transactionType\n"
        "  - branchName\n\n"
        "Respond with valid JSON only.\n\n"
    ),
}
