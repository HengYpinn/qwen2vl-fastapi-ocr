# prompts.py

PROMPTS = {
    "ic": (
        "Extract ONLY JSON with keys:"
        "cardType,idNumber,name,status,isIslam,gender,expiryDate,addressRaw,address."
        "address = {houseNumber,street,locality,postcode,city,state}. Date format DD-MM-YYYY."
        ""
        "Rules (critical):"
        "1) idNumber must match \\d{6}-\\d{2}-\\d{4}. If not visible, set null."
        "2) cardType ∈ {MyKad,MyPR,MyKAS,MyTentera,MyKid}. "
        "   Do NOT use headers like \"KAD PENGENALAN MALAYSIA\" as cardType."
        "   If uncertain, set null."
        "3) name = the person's name near the portrait (may include BIN/BINTI/A/L/A/P). "
        "   Never use words like WARGANEGARA, LELAKI, PEREMPUAN, MALAYSIA, MyKad as name."
        "4) gender: map LELAKI→Male, PEREMPUAN→Female. If not printed, null."
        "5) status: if the word WARGANEGARA appears, set \"Citizen\"; else null."
        "6) isIslam: true only if the word ISLAM is printed on the card; else false if a different religion is printed; null if not shown."
        "7) expiryDate: set null unless an explicit expiry date is printed on the IC."
        "8) Address:"
        "   - addressRaw = the full address block exactly as printed (preserve tokens like \"No\", \"Lot\", \"Jalan\", \"Taman\"), join lines with commas, no translation."
        "   - Parse address into components; if a component is missing, set null. "
        "   - houseNumber must include prefixes if printed (e.g., \"No 1\", \"Lot 12A\")."
        "   - postcode = 5 digits when present."
        "   - Prefer the lower-left text block for the address; include vertical lines if used."
        "9) Never invent or infer text. If unreadable, return null for that field."
        ""
        "Return only the JSON object."
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