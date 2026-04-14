#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def _runserver_links(argv):
    """Return host/port display values for runserver quick links."""
    host = "127.0.0.1"
    port = "8000"
    addrport = None

    for token in argv[2:]:
        if token.startswith("-"):
            continue
        addrport = token
        break

    if addrport:
        if ":" in addrport:
            host_part, port_part = addrport.rsplit(":", 1)
            host = host_part or host
            port = port_part or port
        elif addrport.isdigit():
            port = addrport
        else:
            host = addrport

    host = host.strip("[]")
    if host in {"0.0.0.0", "::"}:
        host = "127.0.0.1"

    return host, port


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        host, port = _runserver_links(sys.argv)
        base_url = f"http://{host}:{port}/"
        print("\nQuick links:")
        print(f"Web:   {base_url}")
        print(f"Admin: {base_url}admin/\n")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
