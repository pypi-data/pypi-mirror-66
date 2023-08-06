"""Create a SSL certificate.

Requirements: OpenSSL.
"""

import argparse
import logging
import os
import subprocess


def get_paths(path):
    """"""
    return [
        os.path.abspath(path) + string
        for string in (".crt", ".key", "csr.cnf")
    ]


def main():
    # noinspection SpellCheckingInspection
    log_formatter = logging.Formatter(
        "%(asctime)s [%(module)-15s %(levelname)-8s]     %(message)s",
        style='%'
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)

    cli_parser = argparse.ArgumentParser(description='Create SSL certificate',
                                         allow_abbrev=False)
    cli_parser.add_argument('-n', '--name',
                            type=str,
                            default=None,
                            required=False,
                            help='Certificate, key and configuration file name')
    cli_parser.add_argument('-d', '--domain',
                            type=str,
                            default=None,
                            required=False,
                            help='Server domain (e.g. example.com)')
    cli_parser.add_argument('-f', '--force', '--overwrite',
                            action='store_true',
                            help='Overwrite certificate and key if they exist')
    arguments = vars(cli_parser.parse_args())
    name = arguments['name']
    if name is None:
        try:
            from config import name
        except ImportError:
            name = None
    while not name or not os.access(os.path.dirname(os.path.abspath(name)),
                                    os.W_OK):
        try:
            name = input(
                "Enter a valid file name for certificate, key and "
                "configuration file. Directory must be writeable.\n"
                "\t\t"
            )
        except KeyboardInterrupt:
            print()
            logging.error("Aborting...")
            return
    certificate_path, key_path, configuration_path = get_paths(
        name
    )
    if not os.access(os.path.dirname(certificate_path), os.W_OK):
        logging.error(f"Invalid path `{certificate_path}`!")
        return
    if any(
            os.path.isfile(path)
            for path in (certificate_path, key_path, configuration_path)
    ) and not arguments['force'] and not input(
        "Do you want to overwrite existing certificate, key and "
        "configuration file?"
        "\n[Y]es or [N]o\t\t\t\t"
    ).lower().startswith('y'):
        logging.error("Interrupted. Provide a different --name.")
        return
    domain = arguments['domain']
    if domain is None:
        try:
            from config import domain
        except ImportError:
            domain = None
    while not domain:
        domain = input("Enter server domain (e.g. example.com)\n\t\t")
    with open(configuration_path, 'w') as configuration_file:
        logging.info("Writing configuration file...")
        configuration_file.write(
            "[req]\n"
            "default_bits = 4096\n"
            "prompt = no\n"
            "default_md = sha256\n"
            "distinguished_name = dn\n"
            "\n"
            "[dn]\n"
            f"CN = {domain}\n"
        )
    logging.info("Generating certificate and key...")
    subprocess.run(
        [
            f"openssl req -newkey rsa:4096 -nodes "
            f"-keyout \"{key_path}\" -x509 -days 365 "
            f"-out \"{certificate_path}\" "
            f"-config \"{configuration_path}\""
        ],
        capture_output=True,
        text=True,
        shell=True
    )
    with open(certificate_path, 'r') as certificate_file:
        logging.info(
            "Certificate:\n\n{certificate}".format(
                certificate=''.join(certificate_file.readlines())
            ),
        )
    logging.info("Done!")


if __name__ == '__main__':
    main()
