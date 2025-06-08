# prompts.py

PROMPTS = {
    "ic": (
        "Extract JSON with keys cardType,idNumber,name,address,status,religion,gender,expiryDate,documentAuthenticity from Malaysian IC image.expiryDate format DD-MM-YYYY.documentAuthenticity:integer 0–100 representing confidence(%) that the ID is genuine and legible."
    ),

    "passport": (
        "Extract JSON with keys fullName,countryCode,passportNumber,nationality,nationalId,dateOfBirth,sex,dateOfIssue,dateOfExpiry,issuedBy,documentAuthenticity from passport scan.documentAuthenticity:integer 0–100 representing confidence(%) that the ID is genuine and legible."
    ),

    "receipt": (
        "Extract JSON with keys: if cash deposit receipt -> date,time,accountNumber,name,total,transactionStatus; "
        "if bank transfer receipt -> status,date,time,amount,referenceCode,toName,toBank,toAccountLast4,transferType,remarks."
    ),
}