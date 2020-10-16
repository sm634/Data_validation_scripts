from DMS_GitHub.postcodes_class import PostcodesClass

# generating invalid sample postcodes for test be validated and verified.
invalid_pcds = ['SE18 0E1', '1GR 48C', 'ET15 1TK', 'K$Cd 4', 'ZE1 4']
# a sample of valid postcodes.
valid_pcds = ['EC1A 1BB', 'W1A 0AX', 'M1 1AE', 'B33 8TH', 'CR2 6XH', 'DN55 1PT']

postcodes_sample = invalid_pcds + valid_pcds
# instantiate the postcode class.

# first we validate the formats of each postcodes. Then store the valid formats into the empty list valid_formats.
print("Validating Postcode Formats")
valid_formats = []
for postcode in postcodes_sample:
    check_postcodes = PostcodesClass(postcode)
    format_status = check_postcodes.validate_postcode_format()
    print('postcode: ', format_status)
    if format_status == 'Valid Postcode Format':
        valid_formats.append(postcode)

print("Verifying postcodes using API")
# Now we try to verify the postcodes with valid formats to see if it is verified (e.g. actually exists) using API.
for postcode in valid_formats:
    check_postcodes = PostcodesClass(postcode)
    verification_status = check_postcodes.verify_postcode_api()
    print('postcode: ', verification_status)

print("Verifying postcodes using ONS reference data.")
# Verifying postcodes using the reference data instead. This method is much more efficient when we have a large set of
# postcodes that needs to be verified.
check_postcodes = PostcodesClass(postcodes_sample)
verification_status = check_postcodes.verify_postcode_ref_data()
print(verification_status)

