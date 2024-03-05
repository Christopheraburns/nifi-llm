
from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult
from nifiapi.properties import PropertyDescriptor, StandardValidators, ExpressionLanguageScope

class CallLocalLLM(FlowFileTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.FlowFileTransform']

    class ProcessorDetails:
        version = '2.0.0-SNAPSHOT'
        description = """Return a completion from a local LLM"""
        tags = ["LLM","GenAI", "Local Inference"]

    PROMPT_TEXT = PropertyDescriptor(
        name="Prompt Text",
        description="Specifies the prompt to send",
        required=True,
        validators=[StandardValidators.NON_EMPTY_VALIDATOR],
        expression_language_scope=ExpressionLanguageScope.FLOWFILE_ATTRIBUTES
    )

    property_descriptors = [
        PROMPT_TEXT
    ]

    def __init__(self, **kwargs):
        super().__init__()
        self.property_descriptors.append(self.PROMPT_TEXT)

    def getPropertyDescriptors(self):
        return self.property_descriptors
    
    def transform(self, context, flowfile):
        from llama_cpp import Llama

        prompt_text = context.getProperty(self.PROMPT_TEXT).evaluateAttributeExpressions(flowfile).getValue()

        #llm = Llama.from_pretrained(
        #    repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        #    filename="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        #    verbose=False
        #)

        llm = Llama(model_path="./mistral-7b-Q4.gguf",
        )


        output = llm("Q:" + prompt_text +" A: ", 
                     max_tokens=100,
                     stop=["Q:", "\n"], 
                     echo=False
        )

        attributes = {"mime.type": "application/json"}
        return FlowFileTransformResult(relationship="success", contents=output, attributes=attributes)