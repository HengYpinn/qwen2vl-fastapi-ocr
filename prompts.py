# prompts.py

PROMPTS = {
    "ic": (
        "Extract ONLY JSON with keys:"
        "cardType,idNumber,name,status,isIslam,gender,expiryDate,addressRaw,address."
        "addressRaw = full address as printed (no omissions, no translation)."
        "address = {houseNumber,street,locality,postcode,city,state}."
        ""
        "Rules:"
        "- Preserve prefixes/suffixes in houseNumber (e.g., \"No 8\", \"No. 3A-1\", \"Lot 12A\")."
        "- If a field isn't printed, set null; never guess."
        "- For MyKad, set expiryDate=null unless an expiry is explicitly printed; do not infer status."
        ""
        "Date format: DD-MM-YYYY."
    ),

    "passport": (
        "Read the 2-line MRZ; decode per ICAO-9303 for "
        "type,countryCode(3),passportNumber,nationality,fullName,lastName,firstName,dateOfBirth,sex,dateOfExpiry."
        "From the visual zone get placeOfBirth,dateOfIssue,issuedBy,authority."
        "Use null if a field is unreadable."
        "Date format: DD MMM YYYY."
        "Return ONLY JSON with keys "
        "type,countryCode,passportNumber,fullName,lastName,firstName,placeOfBirth,nationalId,"
        "dateOfBirth,sex,dateOfIssue,dateOfExpiry,issuedBy,authority."
    ),

    "cash_deposit": (
        "Extract JSON with keys date,time,accountNumber,name,total,transactionStatus from cash-deposit receipt.Output only JSON.",
    ),

    "bank_transfer": (
        "Return only JSON with 10 keys: status, date, time, amount, referenceCode, toName, toBank, toAccNo, transferType, remarks. Missing values ⇒ null. Strictly no extra keys, only English for keys.JSON only."
    ),

    "ssm_form_d": (
        "Extract JSON with keys companyName,registrationNumber,oldRegistrationNumber,registrationDate,principalPlaceOfBusiness,branchAddress.Output only JSON."
    ),

    "utility_bill": (
        "Extract JSON with keys customerName,customerAddress.Output only JSON."
    ),
}