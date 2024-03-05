from llama_cpp import Llama

prompt_text = "What the are the names of all the planets in our solar system?"


#llm = Llama.from_pretrained(
#    repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
#    filename="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
#    verbose=False
#)

llm = Llama(
    model_path="./mistral-7b-Q4.gguf",
)


output = llm("Q:" + prompt_text +" A: ", 
                     max_tokens=2048,
                     #stop=["Q:", "\n"], 
                     echo=False
        )

print(output)