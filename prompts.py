# prompts.py

PROMPTS = {
    "ic": (
        "Extract JSON with keys cardType(MyKad,MyPR,MyKAS,MyTentera,MyKid),idNumber,name,address,status,religion,gender,expiryDate,blurIntensity(in percentage),glareIntensity(in percentage) from Malaysian IC image.expiryDate format DD-MM-YYYY.Output only JSON."
    ),

    "passport": (
        "Extract JSON with keys type,countryCode,passportNumber,fullName,placeOfBirth,nationalId,dateOfBirth,sex,dateOfIssue,dateOfExpiry,issuedBy,authority,blurIntensity(in percentage),glareIntensity(in percentage) from passport scan.Output only JSON."
    ),

    "receipt": (
        "Extract JSON with keys: if cash deposit receipt -> date,time,accountNumber,name,total,transactionStatus; "
        "if bank transfer receipt -> status,date,time,amount,referenceCode,toName,toBank,toAccountLast4,transferType,remarks.Output only JSON."
    ),
}