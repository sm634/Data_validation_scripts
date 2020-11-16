import pandas as pd
import re


class CheckContact:
    """A class that is designed to validate the formats of contact such as email addresses and UK phone numbers
    (landlines or mobile number)."""

    def __init__(self, contactinfo):
        self.email_address = contactinfo
        self.phone_number = contactinfo

    def __area_code_buckets(self, area_codes_set):
        """ A function that creates buckets for the area codes so that when the area code checks for an array of
        phone numbers are taken, this can be processed faster by only working on the buckets that match the input
        phone number (as opposed to checking all the possible area code types). """
        all_batches = [[] for i in range(10)]

        for area in area_codes_set:
            if re.match(r'^011', area):
                all_batches[0].append(area)
            elif re.match(r'^012', area):
                all_batches[1].append(area)
            elif re.match(r'^013', area):
                all_batches[2].append(area)
            elif re.match(r'^014', area):
                all_batches[3].append(area)
            elif re.match(r'^015', area):
                all_batches[4].append(area)
            elif re.match(r'^016', area):
                all_batches[5].append(area)
            elif re.match(r'^017', area):
                all_batches[6].append(area)
            elif re.match(r'^018', area):
                all_batches[7].append(area)
            elif re.match(r'^019', area):
                all_batches[8].append(area)
            elif re.match(r'^02', area):
                all_batches[9].append(area)
        return all_batches

    def __bucket_index(self):
        """ A function that creates area code bucket index to show which bucket of the area coe the matching between
        the input phone number and the list of codes should be made for."""
        batch_n = 0
        if re.match(r'^011', self.phone_number):
            batch_n = 0
        elif re.match(r'^012', self.phone_number):
            batch_n = 1
        elif re.match(r'^013', self.phone_number):
            batch_n = 2
        elif re.match(r'^014', self.phone_number):
            batch_n = 3
        elif re.match(r'^015', self.phone_number):
            batch_n = 4
        elif re.match(r'^016', self.phone_number):
            batch_n = 5
        elif re.match(r'^017', self.phone_number):
            batch_n = 6
        elif re.match(r'^018', self.phone_number):
            batch_n = 7
        elif re.match(r'^019', self.phone_number):
            batch_n = 8
        elif re.match(r'^02', self.phone_number):
            batch_n = 9
        return batch_n

    def uk_area_codes_check(self, area_code_list):

        # remove brackets and spaces for check.
        phone_number = self.phone_number.replace(' ', '').replace('(', '').replace(')', '')
        buckets = self.__area_code_buckets(area_code_list)
        bucket_idx = self.__bucket_index()

        response = ''
        for code in buckets[bucket_idx]:
            match = re.match(r'^{}'.format(code), phone_number)
            if match and len(phone_number) == 11:
                response = 'Valid Area Code Format'

        if len(response) == 0:
            response = 'Invalid Phone Format'
        return response

    def uk_mobile_format_check(self):
        """Checks the input to see if it matches UK mobile number format, including extension."""

        # remove brackets and spaces for check.
        self.phone_number = self.phone_number.replace(' ', '').replace('(', '').replace(')', '')

        alpha_match = re.search(r'[a-z]', self.phone_number)
        numeric_match = re.search(r'[0-9]', self.phone_number)
        extension_match = re.match(r'^[+]447', self.phone_number)
        extension_bracket_match = re.match(r'^[+]4407', self.phone_number)
        mob_match = re.match(r'^07', self.phone_number)

        if len(self.phone_number) == 0 or str(self.phone_number) == 'nan':
            response = 'Null'
        elif (len(self.phone_number) == 11) and mob_match and numeric_match and not alpha_match:
            response = 'Valid Mobile Format'
        elif len(self.phone_number) == 13 and extension_match and numeric_match and not alpha_match:
            response = 'Valid Mobile Format'
        elif (len(
                self.phone_number) == 14) and extension_match and extension_bracket_match and numeric_match and not alpha_match:
            response = 'Valid Mobile Format'
        else:
            response = 'Invalid Mobile Format'
        return response

    def email_validation(self):
        """A method that validates email format. Does not validate against existing domains, only the structure."""

        email = str(self.email_address)
        email = email.replace(' ', '')
        email_pattern_check = re.search(r'^[a-z]+[._]?[a-z0-9]+[@]\w+[.]\w+[.]?\w{2,3}$', email)
        start1 = email.find('<')
        end1 = email.find(r'>')
        start2 = email.find('[')
        end2 = email.find(']')
        email_inside_bracket1 = email[start1 + 1:end1]
        email_inside_bracket2 = email[start2 + 1:end2]
        email_pattern_check_bracket1 = re.search(r'^[a-z]+[._]?[a-z0-9]+[@]\w+[.]\w+[.]?\w{2,3}$', email_inside_bracket1)
        email_pattern_check_bracket2 = re.search(r'^[a-z]+[._]?[a-z0-9]+[@]\w+[.]\w+[.]?\w{2,3}$', email_inside_bracket2)
        if email_pattern_check:
            validation_status = 'Valid'
        elif len(email) == 0 or email == 'nan':
            validation_status = 'Null'
        elif email_pattern_check_bracket1 or email_pattern_check_bracket2:
            validation_status = 'Valid (inside brackets)'
        else:
            validation_status = 'Not Valid'
        return validation_status
