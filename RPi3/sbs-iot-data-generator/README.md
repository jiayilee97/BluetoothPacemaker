# Sample Data Generator for AWS IoT Simple Beer Service

This is the code repository for sample code to locally generate IoT device data similar to what is generated by the [AWS Simple Beer Service](https://github.com/awslabs/simplebeerservice) devices, and feed it to AWS IoT service.

### Pre-requisites

* Amazon Web Services account
* [AWS Command Line Interface (CLI)](https://aws.amazon.com/cli/)
* Python
* boto3

### Script Details

The script generates random values (within a reasonable range) for each of the four parameters- Flow, Temperature, Humidity and Sound. You can tweak the values by changing the *`random.randint(min, max)`* values corresponding to each parameter. 

The script is set to generate messages of each of the four types in a fixed percentage. If you want more or less messages of a particular parameter, you can change the values of *`rnd`* in the *`if...else`* part of the code. 

### Running Example

`$ python sbs.py` 

## Run the script on Amazon EC2 Instance

If for some reason you are unable to run this script on your local machine, or prefer to host it externally, you can run it from an Amazon EC2 instance. Follow these steps:

1. Create an IAM role with a policy that gives access to IoT (example: AWSIoTFullAccess)
2. Launch a new EC2 instance and assign it the IoT IAM role at launch
3. Login to the EC2 instance and change to root user `sudo su`
4. Set your default region and output format in `aws configure`
5. Upload `sbs.py` file to EC2, or `nano sbs.py`, copy the entire script, save and exit
6. Make sure you have boto3 installed. If not, type `pip install boto3`
7. Run `python sbs.py`
