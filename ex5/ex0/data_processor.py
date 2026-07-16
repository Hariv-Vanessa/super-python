from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data provided")

        current_rank = self._rank
        self._rank += 1
        old_data = (current_rank, self._storage.pop(0))
        return old_data


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(item, (int, float))
                       and not isinstance(item, bool)
                       for item in data)
        return False

    def ingest(
            self,
            data: int | float | list[int] | list[float] | list[int | float]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        if isinstance(data, (int, float)):
            self._storage.append(str(data))
        if isinstance(data, list):
            for item in data:
                self._storage.append(str(item))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise TypeError("Invalid data type.")
        if isinstance(data, str):
            self._storage.append(data)
        if isinstance(data, list):
            for item in data:
                self._storage.append(item)


class LogProcessor(DataProcessor):
    def _is_a_dict(self, data: Any) -> bool:
        if not isinstance(data, dict) or not data:
            return False
        return all(
            isinstance(key, str) and isinstance(value, str)
            and value.strip() != ""
            for key, value in data.items()
        )

    def validate(self, data: Any) -> bool:
        if self._is_a_dict(data):
            return True
        if isinstance(data, list) and data:
            return all(self._is_a_dict(item) for item in data)
        return False

    def _get_value(self, data: dict[str, str]) -> str | None:
        if len(data) == 2:
            value1, value2 = data.values()
            return f"{value1}: {value2}"
        return None

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise TypeError("Invalid data type.")
        values = data if (isinstance(data, list)) else [data]
        for value in values:
            log = self._get_value(value)
            if log:
                self._storage.append(log)


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")
    except TypeError as exc:
        print(f"Got exception: {exc}")

    numeric_value = [1, 2, 3, 4, 5]
    print(f"Processing data: {numeric_value}")
    try:
        numeric.ingest(numeric_value)
        print("Extracting 3 values...")
        try:
            for _ in range(3):
                rank, data = numeric.output()
                print(f"Numeric value {rank}: {data}")
        except IndexError as exc:
            print(f"{exc}")
    except TypeError as exc:
        print(f"Got exception: {exc}")

    print("\nTesting Text Processor...")
    print(f"Trying to validate input '42': {text.validate(42)}")
    text_value = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {text_value}")
    try:
        text.ingest(text_value)
        print("Extracting 1 value...")
        try:
            rank, data = text.output()
            print(f"Text value {rank}: {data}")
        except IndexError as exc:
            print(f"{exc}")
    except TypeError as exc:
        print(f"Got exception: {exc}")

    print("\nTesting Log Processor...")
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    dict_value = [
            {'log_level': "NOTICE", 'log_message': 'Connection to server'},
            {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'},
    ]
    print(f"Processing data: {dict_value}")
    try:
        log.ingest(dict_value)
        print("Extracting 2 values...")
        try:
            for _ in range(2):
                rank, data = log.output()
                print(f"Log entry {rank}: {data}")
        except IndexError as exc:
            print(f"{exc}")
    except TypeError as exc:
        print(f"Got exception: {exc}")


if __name__ == "__main__":
    main()
