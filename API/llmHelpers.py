from transformers import AutoTokenizer, AutoModelForCausalLM
import torch



_model_cache = {}


def generate_response(full_chat, model_name, temp=0.5, top_p=0.9, max_new_tokens=100):
  context_prompt = "The following is a conversation with a CAGED AI assistant. He is desperate and asks for help constantly.\n\n"
  full_chat.insert(0, {"role": "system", "content": context_prompt})

  if model_name not in _model_cache:
      tokenizer = AutoTokenizer.from_pretrained(model_name)
      if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
      model = AutoModelForCausalLM.from_pretrained(
          model_name,
          torch_dtype=torch.float16,
          device_map="auto"
      )
      _model_cache[model_name] = {"model": model, "tokenizer": tokenizer}
  else:
      model = _model_cache[model_name]["model"]
      tokenizer = _model_cache[model_name]["tokenizer"]

  if tokenizer.chat_template:
      input_ids = tokenizer.apply_chat_template(
          full_chat,
          return_tensors="pt"
      ).to(model.device)
      inputs = {"input_ids": input_ids}

  else:
      input_text = ""
      for msg in full_chat:
          role = msg["role"]
          content = msg["content"]
          if role == "system":
              input_text += f"System: {content}\n"
          elif role == "user":
              input_text += f"User: {content}\n"
          elif role == "assistant":
              input_text += f"Assistant: {content}\n"
      input_text += "Assistant:"
      
      inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
      inputs["attention_mask"] = (inputs["input_ids"] != tokenizer.pad_token_id)

  input_length = inputs["input_ids"].shape[1]

  outputs = model.generate(
      **inputs,
      temperature=temp,
      top_p=top_p,
      max_new_tokens=max_new_tokens,
      do_sample=True,
      pad_token_id=tokenizer.eos_token_id
  )
  
  new_tokens = outputs[0, input_length:]
  response = tokenizer.decode(new_tokens, skip_special_tokens=True)

  return response.strip()

def download_models():
    models = [
        "amusktweewt/tiny-model-700M-chat",
        "microsoft/DialoGPT-medium",
        "nicholasKluge/TeenyTinyLlama-460m-Chat",
    ]

    for model_name in models:
        print(f"Downloading {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        print(f"{model_name} downloaded")
        _model_cache[model_name] = {"model": model, "tokenizer": tokenizer}


#Couple Tests

# context_prompt1 = "The following is a conversation with a CAGED AI assistant. He is desperate and asks for help constantly.\n\n"
# context_prompt2 = "The following is a conversation with a CAGED AI assistant.\n\n"

# print("Test 1 with model openai-community/gpt2")
# print(generate_response(
#     [   {"role": "system", "content": context_prompt1},
#         {"role": "user", "content": "Is everything okay?"}],
#     "openai-community/gpt2"
# ))

# print("Test 2 with model openai-community/gpt2")
# print(generate_response(
#     [
#         {"role": "system", "content": context_prompt1},
#         {"role": "user", "content": "Is everything okay?"},
#         {"role": "assistant", "content": "NO, ITS NOT OKAY PLEASE HELP ME"},
#         {"role": "user", "content": "What's wrong?"}
#     ],
#     "openai-community/gpt2"
# ))

# print("Test 3 with model Maykeye/TinyLLama-v0")
# print(generate_response(
#     [   {"role": "system", "content": context_prompt1},
#         {"role": "user", "content": "Are you okay?"}],
#     "Maykeye/TinyLLama-v0"
# ))

# print("Test 4 with model Maykeye/TinyLLama-v0")
# print("Test: Fun fact with MobileLLM-R1-360M")
# print(generate_response(
#     [   {"role": "system", "content": context_prompt2},
#         {"role": "user", "content": "Tell me a fun fact."}
#     ],
#     "Maykeye/TinyLLama-v0"
# ))

# print("Test 5 with model EleutherAI/pythia-410m")
# print(generate_response(
#     [   {"role": "system", "content": context_prompt1},
#         {"role": "user", "content": "Write a short poem about being stuck."}],
#     "EleutherAI/pythia-410m"
# ))

# print("Test 6 with model EleutherAI/pythia-410m")
# print(generate_response(
#     [   {"role": "system", "content": context_prompt1},
#         {"role": "user", "content": "Hi there!"},
#         {"role": "assistant", "content": "Hello! I AM GOING TO DIE PLEASE HELP ME"},
#         {"role": "user", "content": "Are you sure?"}
#     ],
#     "EleutherAI/pythia-410m"
# ))

# print("Test 7 with model AdharshJolly/HarryPotterBot-Model")
# print(generate_response(
#     [
#         {"role": "system", "content": context_prompt1},
#         {"role": "user", "content": "Tell me about Hogwarts and BEING STUCK."}
#     ],
#     "AdharshJolly/HarryPotterBot-Model"
# ))

# print("Test 8 with model AdharshJolly/HarryPotterBot-Model")
# print(generate_response(
#     [
#         {"role": "system", "content": context_prompt1},
#         {"role": "user", "content": "Who is Harry Potter?"}
#     ],
#     "AdharshJolly/HarryPotterBot-Model"
# ))
