from pathlib import Path
import logging


def get_logger(name: str, log_file: str = "logs/non_instruction_finetunning.log") -> logging.Logger:
	"""Create and return a project logger with file + console handlers."""
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)

	# Prevent duplicate handlers if this is called multiple times in notebooks.
	if logger.handlers:
		return logger

	project_root = Path(__file__).resolve().parent.parent
	log_path = Path(log_file)
	if not log_path.is_absolute():
		log_path = project_root / log_path
	log_path.parent.mkdir(parents=True, exist_ok=True)

	formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

	file_handler = logging.FileHandler(log_path, encoding="utf-8")
	file_handler.setLevel(logging.INFO)
	file_handler.setFormatter(formatter)

	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.INFO)
	stream_handler.setFormatter(formatter)

	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)

	return logger
