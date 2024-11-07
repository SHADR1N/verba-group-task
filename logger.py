import logging

logger = logging.getLogger("Quote")
logger.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)

write = logging.FileHandler("exception.log")
write.setLevel(logging.CRITICAL)

logger.addHandler(stream)
logger.addHandler(write)

