from abc import ABC, abstractmethod
from typing import Protocol, Any, cast


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
        if self._storage:
            old_data = (self._rank, self._storage.pop(0))
            self._rank += 1
            return old_data
        raise ValueError("No data provided ")
    

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

    def ingest(self, data: Any) -> None:
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

    def _is_content_valid(self, data: Any) -> bool:
        if not isinstance(data, dict) or not data:
            return False
        return all(
            isinstance(key, str) and isinstance(value, str)
            and value.strip() != ""
            for key, value in data.items()
        )

    def validate(self, data: Any) -> bool:
        if self._is_content_valid(data):
            return True
        if isinstance(data, list) and data:
            return all(self._is_content_valid(item) for item in data)
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


class CSV_plugin:
    def __init__(self) -> None:
        self.label = "CSV"

    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        new_data: list[str] = []
        for _, value in data:
            if '"' in data or ',' in data:                    
                value = value.replace('"', "")
                new_data.append(f'"{value}"')
            else:
                new_data.append(value)
        print("CSV Output:")
        print(",".join(new_data))


class JSON_plugin:
    def __init__(self) -> None:
        self.label = "JSON"

    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return

        new_data: list[str] = []
        for rank , value in data:
            if '"' in data or ',' in data:
                value = value.replace('"', '\\"')
            new_data.append(f'"item_{rank}": "{value}"')
        new_value = "{" + ",".join(new_data) + "}"
        print("JSON Output")
        print(new_value)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class DataStream():
    def __init__(self) -> None:
        self._processors: dict[str, DataProcessor] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            proc_label = proc.label.strip() if isinstance(proc.label, str) else None
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
            print(f"DataStream error - Can't process element in stream: {item}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        for key, values in self._processors.items():
            print(f"{key.capitalize()} Processor: total {values._count} items"
                  f" processed, remaining {len(values._storage)} on processor")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors.values():
            data: list[tuple[int, str]] = []
            for _ in range(nb):
                try:
                    data.append(proc.output())
                except ValueError:
                    break
            if data:
                plugin.process_output(data)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")

    first_batch = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]

    second_batch = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash"
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days"
            }
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]

    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    fake_proc = cast(DataProcessor, "")
    proc = DataStream()

    print("Initialize Data Stream...")
    proc.print_processors_stats()
    proc.register_processor(fake_proc)

    print("\nRegister Processors\n")

    print(f"Send first batch of data on stream: {first_batch}")
    print()
    proc.register_processor(numeric)
    proc.register_processor(text)
    proc.register_processor(log)
    proc.process_stream(first_batch)
    proc.print_processors_stats()
    
    print("\nSend 3 processed data from each processor to a CSV plugin:")
    proc.output_pipeline(3, CSV_plugin())

    print()
    proc.print_processors_stats()

    print(f"\nSend another batch of data: {second_batch}")
    proc.process_stream(second_batch)
    print()
    proc.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    # proc.process_stream(second_batch)
    proc.output_pipeline(5, JSON_plugin())
    print()
    proc.print_processors_stats()
