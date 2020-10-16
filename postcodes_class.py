import requests
import urllib3
import re
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PostcodesClass:
    """A class for validating UK postcode formats and verifying it against a reference
    postcode data from office of national statistics"""

    def __init__(self, postcode, path='http://api.postcodes.io/postcodes/'):
        self.path = path
        if isinstance(postcode, list) or isinstance(postcode, set) or isinstance(postcode, tuple) \
                or isinstance(postcode, pd.Series):
            self.postcodes = pd.Series(postcode)
        else:
            try:
                self.postcodes = str(postcode)
            except TypeError:
                print('Please insert a list of postcodes or a single postcode!')
                raise

    def verify_postcode_api(self):
        """A postcode verifier method through the use of API"""

        assert type(self.postcodes) == str, "To use this method, the postcode cannot be an iterable."
        request_path = requests.get(self.path + self.postcodes, verify=False)
        response_code = str(request_path)

        if response_code == '<Response [200]>':
            verification_status = 'Verified'
        elif response_code == '<Response [404]>':
            verification_status = 'Invalid Postcode'
        elif response_code == '<Response [400]':
            verification_status = 'No Postcode Submitted'
        elif response_code == '<Response [500]':
            verification_status = 'Server error'
        else:
            verification_status = 'Invalid Postcode'
        return verification_status

    def validate_postcode_format(self):
        """A test to get the valid postcode format. The rules are based on 'ILR Specification 2017 to 2018 - Appendix C - Valid postcode format'.
        Source: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/611951/Appendix_C_ILR_2017_to_2018_v1_Published_28April17.pdf
        Different from postcode verifier."""

        assert type(self.postcodes) == str, "To use this method, the postcode cannot be an iterable."
        pcd = self.postcodes.replace(' ', '')
        # The following regular expression matches are in order to adhere to the rules for UK postcodes given in the
        # documentation.
        first_char_alpha = re.match(r'^[a-zA-Z]', pcd)
        last_char_match = re.match(r'[a-zA-Z]', pcd[-1])
        alpha_match = re.search(r'[a-zA-Z]', pcd)
        numeric_match = re.search(r'[0-9]', pcd)
        special_chars_match = re.search(r'[!#,£$%^&*¬-]', pcd)
        if len(pcd) == 0:
            response = 'Null'
        elif (5 <= len(pcd) <= 7) and first_char_alpha and alpha_match and numeric_match \
                and last_char_match and not special_chars_match:
            response = 'Valid Postcode Format'
        else:
            response = 'Invalid Postcode Format'
        return response

    def verify_postcode_ref_data(self, ref_data_path='C:\\Users\\sm634\\OneDrive\\Desktop\\Folder\\python\\Github'
                                                     '\\ONSPD_NOV_2019_UK\\Data\\ONSPD_NOV_2019_UK.csv'):

        assert type(self.postcodes) == pd.Series, "To use this method, the postcode input has to be a pandas Series."

        def get_postcode_ref_data(ref_data, postcode_col):
            ref_data = pd.read_csv(ref_data, dtype=str)
            postcodes_series = ref_data.iloc[:, (postcode_col - 1)]
            return postcodes_series

        def postcode_null_unverified(postcode):
            verification_status = ''

            if str(postcode).lower() == 'nan':
                verification_status += 'Null'
            else:
                verification_status += 'Not Verified'
            return verification_status

        postcode_col = 'Postcode'  # Assigning a name for the postcode column.

        postcode_ref_data = get_postcode_ref_data(ref_data_path, 3)  # Get the ONS postcode data.
        pcds_ref_data = pd.DataFrame(data=postcode_ref_data.values, columns=[postcode_col])  # Create a new
        # ref_data series.
        pcds_ref_data[postcode_col] = pcds_ref_data[postcode_col].apply(
            lambda x: str(x).replace(' ', ''))  # getting rid of spaces.

        df_postcodes = pd.DataFrame()  # instantiate a new postcode dataframe where the final output will be saved.
        df_postcodes[postcode_col] = self.postcodes.apply(lambda x: str(x).replace(' ', ''))  # getting rid of spaces.

        verified_postcodes = pd.merge(df_postcodes, pcds_ref_data,
                                      on=postcode_col)  # merge the ref data with postcodes.
        verified_postcodes['verification_status'] = 'verified'  # Successfully merged postcodes are verified postcodes.
        unverified_postcodes = df_postcodes[~df_postcodes[postcode_col].isin(verified_postcodes[postcode_col])].copy(
            deep=True)  # Get the set of data that did not merge - this is the unverified postcode.
        unverified_postcodes['verification_status'] = unverified_postcodes[postcode_col].apply(
            lambda x: postcode_null_unverified(x))  # Get rid of any null data (that will be stored as 'nan' strings).

        return verified_postcodes.append(unverified_postcodes, sort=False)
