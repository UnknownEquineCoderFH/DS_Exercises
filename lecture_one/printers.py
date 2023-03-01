from __future__ import annotations


from multiprocessing import Manager
from multiprocessing.pool import Pool
from queue import Queue
from time import sleep
from uuid import uuid4, UUID

from random import random

from enum import IntFlag, auto

from typing import NamedTuple, Final


QUEUE_SIZE: Final = 10
PROCESSES: Final = 2


class PrinterResult(IntFlag):
    SUCCESS = auto()
    NOT_AUTHORIZED = auto()
    QUEUE_FULL = auto()
    NOT_AVAILABLE = auto()
    PRINTER_NOT_FOUND = auto()
    ERR_GENERAL = auto()


class User(NamedTuple):
    id: UUID
    name: str
    password: str


class Printer(NamedTuple):
    name: str
    queue: Queue


class PrintJob(NamedTuple):
    printer: Printer
    job: str


def sleep_random() -> None:
    sleep(random() * 3)


def authenticate(user_name: str, password: str) -> UUID:
    """
    Returns a token as an int.
    -1 if not authorized.
    """
    print(f"Authenticating {user_name}...")
    sleep_random()
    return uuid4()


def perform_print(
    printer_id: UUID, document: str, settings: dict[str, str], token: int
) -> PrinterResult:
    """
    Returns a PrinterResult enum.
    """
    print(f"Printing {document} on {printer_id}...")
    sleep_random()
    return PrinterResult.SUCCESS


def logout(token: int, user_id: UUID) -> None:
    """
    Invalidates the token.
    """
    print(f"Logging out {user_id}...")
    sleep_random()


def queue_length(printer_id: UUID) -> int:
    """
    Returns the number of jobs in the queue.
    """
    print(f"Getting queue length for {printer_id}...")
    sleep_random()
    return 0


def printer_ids() -> list[UUID]:
    """
    Returns a list of printer ids.
    """
    print("Getting printer ids...")
    sleep_random()
    return []


def main() -> int:
    with Manager() as manager, Pool(processes=PROCESSES) as pool:
        printers = manager.list(
            [Printer(f"printer_{i}", manager.Queue(QUEUE_SIZE)) for i in range(1, 6)]
        )

        jobs = manager.list(
            [PrintJob(printer, f"job_{i}") for i, printer in enumerate(printers)]
        )

        users = manager.list(
            [User(uuid4(), f"user_{i}", f"password_{i}") for i in range(1, 6)]
        )

        tokens = pool.starmap(
            authenticate, [(user.name, user.password) for user in users]
        )
        results = pool.starmap(
            perform_print,
            [
                (job.printer.name, job.job, {}, token)
                for job, token in zip(jobs, tokens)
            ],
        )
        pool.starmap(logout, [(token, user.id) for token, user in zip(tokens, users)])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
