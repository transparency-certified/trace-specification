# TRACE Server Setup Guide

## Before you begin

This guide assumes that you have a system running Ubuntu 24.04 LTS. If you are using a different operating system, you may need to adjust the commands accordingly. We also assume that you can execute commands as the root user. Places where you need to run a command as the root user will be indicated with `sudo`. We recommend that you create a dedicated user for running the TRACE Server. In our example we will use the username `ubuntu`.

Before you begin, you need to have the following installed on your system:

- [GPG](https://gnupg.org/)
- [Python 3.8+](https://www.python.org/)

You can do this by running the following commands:

```bash
$ sudo apt update
$ sudo apt install -y gnupg python3
```

## Getting started

### Generating a GPG key pair

To generate a GPG key pair, run the following command:

```bash
$ gpg --full-generate-key
gpg (GnuPG) 2.4.4; Copyright (C) 2024 g10 Code GmbH
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (9) ECC (sign and encrypt) *default*
  (10) ECC (sign only)
  (14) Existing key from card
Your selection? 9
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (4) NIST P-384
   (6) Brainpool P-256
Your selection? 1
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 2y
Key expires at Fri Jan 15 15:05:04 2027 UTC
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: Example Trace System
Email address: valid.email@my.organization.com
Comment: 
You selected this USER-ID:
    "Example Trace System <valid.email@my.organization.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
```

At this stage you will be asked to enter a passphrase. This passphrase will be used to unlock your private key when you need to use it. Make sure you remember this passphrase, as you will need it later on. For this example we are going to use `s3cr3tkey`.

```bash

We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: /home/ubuntu/.gnupg/trustdb.gpg: trustdb created
gpg: directory '/home/ubuntu/.gnupg/openpgp-revocs.d' created
gpg: revocation certificate stored as '/home/ubuntu/.gnupg/openpgp-revocs.d/9A5209A464B9E0CFCCD108C96FB96730E419869C.rev'
public and secret key created and signed.

pub   ed25519 2025-01-15 [SC] [expires: 2027-01-15]
      9A5209A464B9E0CFCCD108C96FB96730E419869C           <-------- THIS IS YOUR FINGERPRINT
uid                      Example Trace System <valid.email@my.organization.com>
sub   cv25519 2025-01-15 [E] [expires: 2027-01-15]

```

Please note that the key that we just generated has a fingerprint of `9A5209A464B9E0CFCCD108C96FB96730E419869C`. You will need this fingerprint for signing TROs. You can ensure that proper fingerprint and secret is used during the signing process by adding the following to your `~/.bashrc` file:

```bash
export GPG_FINGERPRINT="9A5209A464B9E0CFCCD108C96FB96730E419869C"
export GPG_PASSPHRASE="s3cr3tkey"
```

## Setting up the TRACE Server Environment

This part of the guide will vary depending on your site's specific needs. Our example relies on R and Python for data processing, Docker for workflow execution, and `git` for accessing user contributed code that we are going to run. In general, your setup should rely on existing practices at your site. Additionally we are going to use [tro-utils](https://pypi.org/project/tro-utils/) to simplify the generation of TROs.

### Installing System Dependencies

```bash
$ sudo apt install -y git python3-pip python3-venv
```

### Installing tro-utils

```bash
$ python3 -m venv ~/trs-env   # Create a virtual environment for the TRACE Server
$ . ~/trs-env/bin/activate    # Activate the virtual environment
(trs-env) $ pip install tro-utils       # Install tro-utils
```

### Define the TRACE Server capabilities

TROs contain by default basic information about the TRS that was used to generate them. In order to specify your system
basic info and capabilities create a file `~/trs.jsonld` with the following content:

```json
  {
    "rdfs:comment": "TRS that can monitor netowork accesses or provide Internet isolation",
    "trov:hasCapability": [
      {
        "@id": "trs/capability/1",
        "@type": "trov:CanRecordInternetAccess"
      },
      {
        "@id": "trs/capability/2",
        "@type": "trov:CanProvideInternetIsolation"
      }
    ],
    "trov:owner": "My Organization",
    "trov:description": "Example TRACE Server",
    "trov:contact": "valid_email@my.organization.com",
    "trov:url": "http://127.0.0.1/",
    "trov:name": "myorg-trs",
  }
```

## Executing example TRO generation

1. Download the repository containing the example user code for creating TRO:

```bash
$ git clone https://github.com/transparency-certified/sample-trace-workflow
```

2. Activate the virtual environment and initiate TRO before executing user code:

```bash
$ . ~/trs-env/bin/activate
(trs-env) $ tro-utils --declaration sample_tro.jsonld \
    --profile ~/trs.jsonld \
    arrangement add sample-trace-workflow \
    -m "Before executing workflow" -i .git
Loading profile from /home/ubuntu/trs.jsonld
```

At this point, the intial TRO has been created. You can now execute the user code:

```bash
(trs-env) $ cd sample-trace-workflow
(trs-env) $ docker build -t trace-example/sample-trace-workflow .
(trs-env) $ bash run_locally.sh latest trace-example
(trs-env) $ cd ..
```

3. Record the changes made by the user code:

```bash
(trs-env) $ tro-utils --declaration sample_tro.jsonld arrangement add sample-trace-workflow \
    -m "After executing workflow" -i .git
```

4. Verify that the TRO contains two arrangements:

```bash
(trs-env) $ tro-utils --declaration sample_tro.jsonld arrangement list
Arrangement(id=arrangement/0): Before executing workflow
Arrangement(id=arrangement/1): After executing workflow
```

5. Add details about the workflow execution:

```bash
(trs-env) $ tro-utils --declaration sample_tro.jsonld performance add \
  -m "My magic workflow" \
  -s 2025-01-15T09:22:01 \
  -e 2024-01-15T10:00:11 \
  -c trov:InternetIsolation \
  -c trov:InternetAccessRecording \
  -a arrangement/0 \
  -M arrangement/1
```

5. Timestamp and sign the TRO:

```bash
(trs-env) $ tro-utils --declaration sample_tro.jsonld sign
```

6. (Optional) Verify the TRO:

```bash
(trs-env) $ tro-utils --declaration sample_tro.jsonld verify
Using configuration from /usr/lib/ssl/openssl.cnf
Warning: certificate from '/tmp/tmp2607sx0l' with subject '/O=Free TSA/OU=TSA/description=This certificate digitally signs documents and time stamp requests made using the freetsa.org online services/CN=www.freetsa.org/emailAddress=busilezas@gmail.com/L=Wuerzburg/C=DE/ST=Bayern' is not a CA cert
Verification: OK
```

You should now have a TRO in the file `sample_tro.jsonld` along with it signature in `sample_tro.sig` and TSR in `sample_tro.tsr`. Now we can proceed to publish the TRO.

## Publishing the TRO

TRS should provide a landing page where TROs can be accessed and TRS capabilities can be viewed.

To publish the TRO, you need to have a web server running on your system. We are going to use a simple Flask app with a template webpage capable of listing TROs and basic info about TRS. You can download it by running the following command:

```bash
$ git clone https://github.com/transparency-certified/trs-template
$ cd trs-template
$ python3 -m venv server-env
$ . ./server-env/bin/activate
(server-env) $ python3 -m pip install -r requirements.txt
```

Now you need to copy the TROs to the web server directory:

```bash
(server-env) $ cp ~/sample_tro.*  ~/trs-template/data/
```

Finally, you can start the web server:

```bash
(server-env) $ python3 app.py
```

Webserver should be available at `http://localhost:5000/`.

