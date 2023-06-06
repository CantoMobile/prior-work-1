import re
import dns.resolver
from app.repositories.user_repository import UserRepository


user_repo = UserRepository()

def validate_email_domain(email):
    # Validate email structure using a regular expression
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format."

    # Check if the domain exists using DNS resolution
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
    except dns.resolver.NXDOMAIN:
        return False, "Invalid domain."
    
    exist = user_repo.existsByField('email', email)
    if exist:
        return False, "Email and user all ready exists."

    return True, ""
