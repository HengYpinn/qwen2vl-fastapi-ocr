# prompts.py

PROMPTS = {
    "ic": (
        "Extract JSON with keys cardType(MyKad,MyPR,MyKAS,MyTentera,MyKid),idNumber,name,address,status,isIslam,gender,expiryDate from Malaysian IC image.expiryDate format DD-MM-YYYY.Output only JSON."
    ),

    "passport": (
        "Read the 2-line MRZ; decode per ICAO-9303 for "
        "type,countryCode(3),passportNumber,nationality,fullName,dateOfBirth,sex,dateOfExpiry."
        "From the visual zone get placeOfBirth,dateOfIssue,issuedBy,authority."
        "Use null if a field is unreadable."
        "Date format: DD MMM YYYY."
        "Return ONLY JSON with keys "
        "type,countryCode,passportNumber,fullName,placeOfBirth,nationalId,"
        "dateOfBirth,sex,dateOfIssue,dateOfExpiry,issuedBy,authority."
    ),

    "cash_deposit": (
        "Extract JSON with keys date,time,accountNumber,name,total,transactionStatus from cash-deposit receipt.Output only JSON.",
    ),

    "bank_transfer": (
            "Return *only* JSON with keys: status, date, time, amount, referenceCode, toName, toBank, toAccNo, transferType, remarks. Missing values ⇒ null. Strictly no extra keys, only English for keys.JSON only."
    ),
}