from pydantic import BaseModel, EmailStr,field_validator
import phonenumbers
import requests

class User(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    
    @field_validator('phone_number')
    def validate_phone(cls, v):
        try:
            phone_number = phonenumbers.parse(v, "RU")
            if not phonenumbers.is_valid_number(phone_number):
                raise ValueError("Некорректный номер")
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Некорректный формат номера")