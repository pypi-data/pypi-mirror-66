# twilio-sendsms

A command-line tool for sending bulk SMS using Twilio.

The utility lets you define a mustache template and provide a CSV file with matching columns for bulk SMS sends.

## Installation

The utility requires `python3.7`

```
python -m pip install twilio_sendsms
```

## Setup

The first time you run, you will be prompted to provide your Twilio account details.

All configuration settings get stored in `~/.twilio-sendsms.config`. To reconfigure you can delete this file. 

## Running 

First, you need to define a mustache template and save to a file, e.g. example.mustache:

```
Hi {{first_name}}, this is a test SMS. 
```

Next, you need to create a bulk send CSV file. The file must have a `mobile_number` column. The mobile number must be in the international format, e.g. +614XXXXXXXX. The other column names need to match the variable names used in the mustache template.

buld_send.csv
```
"mobile_number","first_name"
"+614XXXXXXXX","Joe"
```

To process the batch file:

```
sendsms --template example.mustache test.csv 
```

## Testing

Before processing a bulk CVS file, it's a good idea to sample some entries and send them to yourself first. Testing is useful to confirm the formatting and the number of segments are as expected.

To sample and override the mobile_number in the CSV file:

```
sendsms --template example.mustache --sample 1 --sendto +614XXXXXXXX test.csv
```

The command outputs destination mobile number, the Twilio message identifier and the SMS message sent.

```
+614XXXXXXXX,SM8c6335fdcffe4bb88313a16fabc9234d,Hi Joe, this is a test SMS. 
```
