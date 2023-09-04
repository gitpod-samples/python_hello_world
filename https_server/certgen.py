from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import datetime


def generate_cert_and_key(keyfile_path: str, certfile_path: str):
    if not Path(keyfile_path).exists() or not Path(certfile_path).exists():
        key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        subject = issuer = x509.Name(
            [
                x509.NameAttribute(NameOID.COUNTRY_NAME, "BD"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Dhaka"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "Savar"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Gitpod"),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "Community"),
                x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
            ]
        )

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .add_extension(
                x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False
            )
            .sign(key, hashes.SHA256(), default_backend())
        )

        with open(keyfile_path, "wb") as f:
            f.write(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        with open(certfile_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
