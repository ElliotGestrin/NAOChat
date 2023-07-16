from Talker import LocalTalker, TerminalTalker
from Chatter import Chatter
from Listener import Listener
from NAOTalker import NAOTalker
import warnings, yaml, sys, os, time
conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"configs")
kwargs = {key.lower() : value for key, value in [a.split("=") for a in sys.argv[1:]]}
base_params = yaml.safe_load(open(f"{conf_path}/base_params.yaml")) # Used to identify correct type of parameters

config = kwargs.get("config", "default")
if os.path.isfile(f"{conf_path}/{config}.yaml"):
    params = yaml.safe_load(open(f"{conf_path}/{config}.yaml"))
elif os.path.isfile(f"{conf_path}/local/{config}.yaml"):
    params = yaml.safe_load(open(f"{conf_path}/local/{config}.yaml"))
else:
    raise Exception(f"Can't find {config}.yaml in configs or configs/local")
# Overwrite any parameters set during call. Take types from: current config or base_params if not included
for k,v in kwargs.items():
    if k in params: params[k] = type(params[k])(v)
    elif k in base_params: 
        params[k] = type(base_params[k])(v)
    elif not k == "config": warnings.warn(f"Parameter {k} was not found in {config} or identifed as a base parameter. Ignoring")

# Set up chatter
if "filt_keys" in params: # Format any parameterised filter keys (such as {name})
    for i, key in enumerate(params["filt_keys"]):
        params["filt_keys"][i] = key.format(**params)
chatter = Chatter(
    chat_prompt=params["chat_prompt"].format(**params),
    chat_horison=params.get("chat_horison",10),
    chat_tokens=params.get("chat_tokens",100),
    temp=params.get("temp",0.5),
    stream=params.get("stream",False),
    filt_prompt=params["filt_prompt"].format(**params) if params.get("filt_horison",0) > 0 else "",
    filt_horison=params.get("filt_horison",0),
    filt_name=params.get("filt_name", "assistant").format(**params),
    filt_keys=params["filt_keys"] if params.get("filt_horison",0) > 0 else "",
    filt_tokens=params.get("filt_tokens",5),
)

# Set up talker
match params["talker"].lower():
    case "terminal": talker = TerminalTalker(
        language=params.get("language","en"),
        prefix=params.get("terminal_talker_prefix", "\nAssistant: ").format(**params)
    )
    case "speaker": talker = LocalTalker(
        language=params.get("language","en"),
    )
    case "nao": talker = NAOTalker(
        ip=params["ip"],
        language=params.get("language","en"),
        stand=params.get("nao_stand",True),
        sleep_len=params.get("nao_sleep_len",0.03)
    )
    case _: raise Exception("Incorrect 'talker' specified! Use 'terminal', 'speaker' or 'NAO'")

# Set up listener
match params["listener"].lower():
    case "mic": listener = Listener(
        language=params.get("language","en"),
        default_mic=params.get("default_mic",True),
        use_whisper=params.get("use_whisper",False)
    )
    case "terminal": listener = lambda : input(params.get("terminal_listener_prefix","User: "))
    case "timer": listener = lambda : [time.sleep(params["listener_timer_delay"]), params.get("listener_timer_message", " ")][1]
    case _: raise Exception("Incorrect 'listener' specified! Use 'terminal', 'timer' or 'mic'.")

# Start conversation
while True:
    if params.get("print_listening", True): print(params.get("print_listening", "Listening..."))
    heard = listener()
    if params.get("print_heard", True): print(f"Heard: {heard}")
    if heard != "":
        response = chatter(heard)
        talker(response)
