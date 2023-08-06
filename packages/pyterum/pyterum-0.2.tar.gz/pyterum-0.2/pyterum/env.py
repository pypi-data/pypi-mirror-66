import os


# Socket file paths for both what comes in and goes out
FRAGMENTER_INPUT = os.getenv("FRAGMENTER_INPUT")
FRAGMENTER_OUTPUT = os.getenv("FRAGMENTER_OUTPUT")

# Socket file paths for both what comes in and goes out 
TRANSFORMATION_STEP_INPUT = os.getenv("TRANSFORMATION_STEP_INPUT")
TRANSFORMATION_STEP_OUTPUT = os.getenv("TRANSFORMATION_STEP_OUTPUT")

# Size encoding of message with a default value of 4
ENC_MSG_SIZE_LENGTH = 4 if os.getenv("ENC_MSG_SIZE_LENGTH") == None else os.getenv("ENC_MSG_SIZE_LENGTH")

EXAMPLE_SOCKET_INPUT = "./pyterum_example_sockets/example_in.sock"
EXAMPLE_SOCKET_OUTPUT = "./pyterum_example_sockets/example_out.sock"