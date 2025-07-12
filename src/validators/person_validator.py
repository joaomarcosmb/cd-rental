import re
from typing import Dict
from .base_validator import BaseValidator, ValidationError


class PersonValidator(BaseValidator):
    @staticmethod
    def validate_cpf(cpf: str) -> str:
        PersonValidator.validate_required(cpf, "CPF")

        cpf_clean = re.sub(r"[^0-9]", "", cpf)

        PersonValidator.validate_exact_length(cpf_clean, 11, "CPF")

        if not cpf_clean.isdigit():
            raise ValueError("CPF must be a number")

        if cpf_clean == cpf_clean[0] * 11:
            raise ValueError("CPF cannot have all the same digits")

        return cpf_clean

    @staticmethod
    def validate_name(name: str) -> str:
        PersonValidator.validate_required(name, "Name")
        PersonValidator.validate_min_length(name, 2, "Name")

        return name.strip().title()

    @staticmethod
    def validate_phone(phone: str) -> str:
        PersonValidator.validate_required(phone, "Phone")

        phone_clean = re.sub(r"[^0-9]", "", phone)

        if len(phone_clean) != 11:
            raise ValueError("Phone must be in the format 85999999999")

        return phone_clean

    @staticmethod
    def validate_email(email: str) -> str:
        PersonValidator.validate_required(email, "Email")

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        PersonValidator.validate_regex(
            email, email_pattern, "Email", "must be a valid email address"
        )

        return email.strip().lower()

    @staticmethod
    def validate_person_data(
        cpf: str, name: str, phone: str, email: str
    ) -> Dict[str, str]:
        validation_functions = [
            lambda: PersonValidator.validate_cpf(cpf),
            lambda: PersonValidator.validate_name(name),
            lambda: PersonValidator.validate_phone(phone),
            lambda: PersonValidator.validate_email(email),
        ]

        errors = []
        results = {}

        # Validate CPF
        try:
            results["cpf"] = PersonValidator.validate_cpf(cpf)
        except ValueError as e:
            errors.append(str(e))

        # Validate name
        try:
            results["name"] = PersonValidator.validate_name(name)
        except ValueError as e:
            errors.append(str(e))

        # Validate phone
        try:
            results["phone"] = PersonValidator.validate_phone(phone)
        except ValueError as e:
            errors.append(str(e))

        # Validate email
        try:
            results["email"] = PersonValidator.validate_email(email)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
