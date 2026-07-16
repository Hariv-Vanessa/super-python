from abc import ABC, abstractmethod
from typing import Any, cast


class DataProcessor(ABC):
    label: str = ""

    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0
        self._count: int = 0

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
    label = "Numeric"

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

    def ingest(self, data:  int | float | list[int] | list[float] | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        if isinstance(data, (int, float)):
            self._storage.append(str(data))
            self._count += 1
        if isinstance(data, list):
            for item in data:
                self._storage.append(str(item))
                self._count += 1


class TextProcessor(DataProcessor):
    label = "text"

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
            self._count += 1
        if isinstance(data, list):
            for item in data:
                self._storage.append(item)
                self._count += 1


class LogProcessor(DataProcessor):
    label = "log"

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
                self._count += 1


class DataStream():
    def __init__(self) -> None:
        self._processors: dict[str, DataProcessor] = {}

    def register_processor(
            self,
            proc: DataProcessor
    ) -> None:
        if isinstance(proc, DataProcessor):
            if isinstance(proc.label, str):
                proc_label = proc.label.strip()
            else:
                None

            if proc_label:
                self._processors[proc_label] = proc
            else:
                print("No label found")
        else:
            print("No processor found, no data")

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            processed: bool = False
            for proc in self._processors.values():
                if proc.validate(item):
                    try:
                        proc.ingest(item)
                        processed = True
                        continue
                    except TypeError:
                        processed = False
                        break
            if not processed:
                print(f"DataStream error - "
                      f"Can't process element in stream: {item}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        for key, values in self._processors.items():
            print(f"{key.capitalize()} Processor: total {values._count} items"
                  f"processed, remaining {len(values._storage)} on processor")


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")

    stream_data = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]

    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    fake_proc = cast(DataProcessor, "")
    proc = DataStream()

    print("Initialize Data Stream...")
    proc.print_processors_stats()
    proc.register_processor(fake_proc)

    print("\nRegister Numeric Processor")
    proc.register_processor(numeric)

    print(f"\nSend first batch of data on stream: {stream_data}")
    proc.process_stream(stream_data)
    proc.print_processors_stats()

    print("\nRegistering other data processors")
    print("Send the same batch again")
    proc.register_processor(numeric)
    proc.register_processor(text)
    proc.register_processor(log)
    proc.process_stream(stream_data)
    proc.print_processors_stats()

    num_rank, text_rank, log_rank = 0, 0, 0
    try:
        if numeric:
            for _ in range(3):
                num_rank, _ = numeric.output()
        if text:
            for _ in range(2):
                text_rank, _ = text.output()
        if log:
            for _ in range(1):
                log_rank, _ = log.output()

        print(f"\nConsume some elements from the data processors:"
              f" {numeric.label.capitalize()} {num_rank},"
              f"{text.label.capitalize()} {text_rank},"
              f"{log.label.capitalize()} {log_rank}")

        proc.print_processors_stats()
    except ValueError as exc:
        print(f"{exc}")


if __name__ == "__main__":
    main()
