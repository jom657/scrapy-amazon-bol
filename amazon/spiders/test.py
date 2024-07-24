# from dateutil.parser import parse
# from datetime import datetime
# import re


# def translate_dutch_date(date_str):
#     # Mapping of Dutch month names to English month names
#     dutch_months = {
#         "januari": "January", "februari": "February", "maart": "March",
#         "april": "April", "mei": "May", "juni": "June",
#         "juli": "July", "augustus": "August", "september": "September",
#         "oktober": "October", "november": "November", "december": "December"
#     }
#     for dutch, english in dutch_months.items():
#         date_str = date_str.replace(dutch, english)
#     return date_str

# def calculate_delivery_date(date_str):
#     """Calculate delivery date considering different possible formats."""
#     try:
#         # Handle "tomorrow" and "morgen" cases
#         if 'tomorrow' in date_str.lower() or 'morgen' in date_str.lower():
#             return 1
#         else:
#             # Translate Dutch date to English
#             date_str = translate_dutch_date(date_str)
            
#             # Extract date part from the string
#             date_pattern = r'\d{1,2} \w+ \d{4}|\d{1,2} \w+|\w+, \d{1,2} \w+, \d{4}'
#             date_part = re.search(date_pattern, date_str.lower())
#             if date_part:
#                 date_part = date_part.group()
#                 parsed_date = parse(date_part, dayfirst=True).date()
#                 return (parsed_date - datetime.today().date()).days
#             else:
#                 return None
#     except ValueError as e:
#         print(e)
#         return None

# while True:
#     date_str = input("Enter input: ")
#     output = calculate_delivery_date(date_str)

#     print(output)
