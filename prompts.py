# prompts.py

PROMPTS = {
    "ic": (
        "Extract JSON with keys cardType(MyKad,MyPR,MyKAS,MyTentera,MyKid),idNumber,name,address,status,isIslam,gender,expiryDate from Malaysian IC image.expiryDate format DD-MM-YYYY.Output only JSON."
    ),

    "passport": (
        "Extract JSON with keys type,countryCode,passportNumber,fullName,placeOfBirth,nationalId,dateOfBirth,sex,dateOfIssue,dateOfExpiry,issuedBy,authority from passport scan.Output only JSON."
    ),

    "cash_deposit": (
        "Extract JSON with keys date,time,accountNumber,name,total,transactionStatus from cash-deposit receipt.Output only JSON.",
    ),

    "bank_transfer": (
        "Extract JSON with keys status,date,time,amount,referenceCode,toName,toBank,toAccountLast4,transferType,remarks from bank-transfer receipt.Output only JSON."
    ),
}