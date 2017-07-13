# stop script on error
set -e

# Check to see if root CA file exists, download if not
if [ ! -f ./root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from Symantec...\n"
  curl https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem > root-CA.crt
fi

# install AWS Device SDK for Python if not already installed
# if [ ! -d ./aws-iot-device-sdk-python ]; then
#   printf "\nInstalling AWS SDK...\n"
#   git clone https://github.com/aws/aws-iot-device-sdk-python.git
#   pushd aws-iot-device-sdk-python
#   python setup.py install
#   popd
# fi

# run pub/sub sample app using certificates downloaded in package
printf "\nRunning pub/sub sample application...\n"
python binOperation.py -e a1irgsu21jifu4.iot.us-east-1.amazonaws.com -r root-CA.crt -c bls_demo.cert.pem -k bls_demo.private.key
