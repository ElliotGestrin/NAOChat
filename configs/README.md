# Configs

## Introduction
Configs are available to customise the conversational behaviour for `main.py`. 

They do this via setting various parameters for `main.py` and the various classes used. For a list of all parameters, see [Base Parameters](#base-parameters) below. 

To select a config, specify `config=my_config` when calling `main.py`. 
```
> python3 main.py config=my_config
```

You're then able to override any parameters by setting these in the same way. Note that even parameters not included in the config can be overwritten. For example, you can change the `IP`  the `stream` 
```
> python3 main.py config=my_config IP=123.456.789 stream=True
```
Note that to set a parameter to `False` you currently have to set it to something that in python evaluates to false, such as an empty string. 

To create a new config called `my_config` simply create the file `my_config.yaml` in the `configs` directory. Begining a name with `local_`, such as `local_my_config`, will make it not tracked by git. 

## Base Parameters

The following is a list of all base parameters. Obligatory parameters are marked in **bold** and parameters which are sometimes obligatory, such as IP-adress if using NAO, are marked in *cursive*.

Some parameters allow for formatting, most notably the prompts. To format these parameters include `{format_parameter}` in the text. For example, `"base_prompt": "You're a {speach_style} ChatBot"` would give change the chatters to match whatever is specified by the `speach_style` parameter, for example "funny", "sad" or "french".

- **talker** ["terminal"/"speaker"/"nao"]: How a response is communicated. "terminal" will give text responses in the terminal, "speaker" will use text to speech over device speaker and "nao" will use the NAO specified by the IP parameter. Not case sensitive.

- **listener** ["terminal"/"mic"/"timer"]: How GPT hears you. "terminal" will take text input from the terminal, "mic" will use device microphone and "timer" will pause for a duration set by 

- stream [bool]: If the response from ChatGPT should be streamed line-by-line or in a single chunk.

- language [str]: The [ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for the primary language used. This configures the listener, if using a microphone, and any verbal talker used. Examples are: "en", "sv" and "fr". 

- name [str]: A parameter which doesn't do anything by itself. Used for formatting of other parameters.

- print_listening [str]: If truly, this will be printed when ready to receive input. 

- print_heard [str]: If truly, this will be printed followed by what the perceived input after an input is received. Note that no whitespace is added before the input is printed.

- *listener_timer_delay* [float]: How long, in seconds, the "timer" listener should wait before responding with the listener_timer_message

- listener_timer_message [str]: The message sent by the "timer" listener

- temp [float]: A value between 0 and 2 controlling how varied the responses will be. 2 is very varied, 0 is deterministic.

- **chat_prompt** [str]: The prompt given to ChatGPT regarding the conversation. Formattable. 

- chat_horizon [int]: The number of messages ChatGPT sees when responding. 1 means only the last message. ChatGPT:s own responses are counted.

- chat_token [int]: The maximum n192.168.43.234umber of tokens ChatGPT can respond with. A hard cuttoff will be seen if reached.

- *filt_prompt* [str]: The prompt given to the filter. Obligatory if filt_horizon > 0. Formattable. 

- filt_horizon [int]: How many messages the filter should look at when deciding if to respond. Includes both user and ChatGPT responses. Setting to a value <= 0 disables the filter. 

- *filt_keys* [list[str]]: If any of the strings in filt_keys are returned by the filter ChatGPT will get to respond. Obligatory if filt_horizon > 0. Formattable. 

- filt_name [str]: What ChatGPT is called for filter inputs. The user is always called "User". Formattable.

- filt_token [int]: The number of tokens the filter can respond with. Hard cuttoff if reached. 

- default_mic [bool]: If the default device microphone is used when the listener is "mic". If false, a choice of mic is done via terminal.

- use_whisper [bool]: If the listener should use OpenAI:s Whisper when doing speech to text. If false, google text-to-speech is used. 

- terminal_listener_prefix [str]: What the prefix is for user terminal input.

- nao_stand [bool]: If the NAO should stand up at the start of the program. It'll automatically sit down when the program closes. 

- nao_sleep_len [float]: How long NAO-talker waits per token in response

- nao_volume [int]: The volume the NAO-talker speaks at. 0 to 100.

- ip [str]: The IP adress of a NAO used

- nao_sleep_time [float]: How long NAO should wait per letter when speaking before continuing

## Custom Parameters

When creating a new config file you can include any parameter you'd like. However, their only use will be to format the base parameters. The suggested `speech_style` above would be such a parameter. See the second paragraph in [Base Parameters](#base-parameters) for a further details on formatting. 