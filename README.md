# Data_validation_scripts
Python scripts that validate postcodes, email formats and phone number formats in the UK. 

### Postcode format Validation and Verification 

postcodes_class has a class methods that can be used to validate postcode format following the standard UK postcode format rules (see: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/611951/Appendix_C_ILR_2017_to_2018_v1_Published_28April17.pdf)
It also has two methods for verifying postcodes - one with API and the other using the ONS postcode data as a validation reference. 
The API used to verify through a request to this website: postcodes.io.
The ONS reference data was downloaded in .csv format from here: https://geoportal.statistics.gov.uk/datasets/ons-postcode-directory-november-2019

#### Postcode Format Validation

The postcode format validation is done through regular expression pattern matching. The rules built are those that satisfy the requirements for valid UK postcodes. 
The following is an output of the when you run the postcodes_test.py script, which calls the class and methods from postcodes_class.py on a small sample of random postcodes:

SE18 0E1:  Invalid Postcode Format

1GR 48C:  Invalid Postcode Format

ET15 1TK:  Valid Postcode Format

K$Cd 4:  Invalid Postcode Format

ZE1 4:  Invalid Postcode Format

EC1A 1BB:  Valid Postcode Format

W1A 0AX:  Valid Postcode Format

M1 1AE:  Valid Postcode Format

B33 8TH:  Valid Postcode Format

CR2 6XH:  Valid Postcode Format

DN55 1PT:  Valid Postcode Format

As would be expcted the obvious ones (where the postcode starts with a number or has fewer than 5 letter or numbers and a special character) are found to not have a valid format. 

#### Post Verification 

We can use the API script to verify the postcodes that were found to have valid formats. The following is the outcome: 

ET15 1TK:  Invalid Postcode

EC1A 1BB:  Verified

W1A 0AX:  Invalid Postcode

M1 1AE:  Verified

B33 8TH:  Verified

CR2 6XH:  Verified

DN55 1PT:  Verified

As you can see, two postcodes that had the correct format do not actually exist in the database used to verify the postcode using the API. 

The same postcodes can also be verified using the ONS postcode reference data (in .csv) format. 

ET15 1TK:  Invalid Postcode

EC1A 1BB:  Verified

W1A 0AX:  Invalid Postcode

M1 1AE:  Verified

B33 8TH:  Verified

CR2 6XH:  Verified

DN55 1PT:  Verified

The result is the same. The difference between the two methods is most noticeable when verifying a large set of postcodes. The API call to verify one postcode at a time is highly time consuming, whereas the ONS reference data method merges the postcodes to be verified with the curated or verified set of postcodes (both post standardisation). This is substantially faster than the API method. 

### Contact Information - Email and Phone - format validation 

Email and Phone format validation is also a regular expression pattern matching exercise. ContactInfo_validation_class.py has the CheckContact class with methods for checking the validity of the formats for phone numbers or email using the appropriate methods. 

#### Email format validation 

The email format validation script (email_formats_validation.py) when run against a sample of made up email-like data yeilds the following result: 

      email                     email_format_validation
sk432@gmail.com                        Valid
ss.kr@hotmail.co.uk                    Valid
134fds@gmail.com                       Not Valid
lsjfdasljf@2rwe.csd...casd             Not Valid
no_one@here.org                        Valid
sfsasdf@                               Not Valid
s.s.s.m.@gmail.com                     Not Valid
Sam Clint <sam_clint@gmail.com>        Valid (inside brackets)

As can be seen from the output, the format validation script does not check for existing domains, but does ensure that the organisation of the characters (letter, number, '@', '.') occur in the stardard manner. It also picks up email addresses to validate that are enclosed within a bigger set of strings so long as they are embedded withing brackets with '<', '>', or '[', ']'. 

#### Phone format validation 

The phone format validation script when run against phone-number like data checks to see if it has the correct extension for mobile numbers or area codes within the UK, along with the requirement for its area length. The output of that when tested against a sample data (phone_format_validation.py script) is: 

   Phone Numbers            phone_format
    07719133871       Valid Mobile Format

  +447712347824       Valid Mobile Format

    02012358765       Valid Area Code Format

    01132346845       Valid Area Code Format

       12432534       Invalid Phone Format

  +232323455666       Invalid Phone Format

        2335223       Invalid Phone Format

As can be seen, it validates phone numbers of the correct length and correct extension codes, while also differentiating between mobile nmbers and land lines with extension codes. 

