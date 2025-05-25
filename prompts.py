PROMPTS = {
    "ic": (
        "Extract the following fields as JSON from this Malaysian IC image:\n"
        "  • fullName\n"
        "  • icNumber\n"
        "  • address\n"
        "  • nationality\n"
        "  • gender\n\n"
        "Then analyze whether this IC looks genuine or counterfeit, and include:\n"
        "  • authenticityConfidence  (a float between 0.0 [fake] and 1.0 [genuine])\n\n"
        "Respond with valid JSON only."
    ),

    "passport": (
        "Extract the following fields as JSON from this passport image:\n"
        "  • fullName\n"
        "  • passportNumber\n"
        "  • nationality\n"
        "  • dateOfBirth\n"
        "  • expiryDate\n\n"
        "Then analyze whether this passport appears authentic or fabricated, and include:\n"
        "  • authenticityConfidence  (a float between 0.0 [fake] and 1.0 [genuine])\n\n"
        "Respond with valid JSON only."
    ),

    "receipt": (
        "Extract the following fields as JSON from this cash‐deposit or bank‐transfer receipt image:\n"
        "  date, time, referenceNumber, totalAmount, currency,\n"
        "  senderAccountNumber, senderName,\n"
        "  receiverAccountNumber, receiverName,\n"
        "  accountType, transactionType, branchName\n"
        "Respond with valid JSON only."
    ),
}
