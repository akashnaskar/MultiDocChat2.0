# --- Usage Example ---
# from logger.custom_logger import CustomLogger

# if __name__ == "__main__":
#     logger = CustomLogger().get_logger(__file__)
#     logger.info("User uploaded a file", user_id=123, filename="report.pdf")
#     logger.error("Failed to process PDF", error="File not found", user_id=123)
## working as expected
# logger/__init__.py
from logger.custom_logger import CustomLogger
# Create a single shared logger instance
GLOBAL_LOGGER = CustomLogger().get_logger("doc_portal")