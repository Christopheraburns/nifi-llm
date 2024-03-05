from llama_cpp import Llama
from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult
from nifiapi.properties import PropertyDescriptor, StandardValidators, ExpressionLanguageScope

class CallLocalLLM(FlowFileTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.FlowFileTransform']

    class ProcessorDetails:
        version = '2.0.0-SNAPSHOT'
        description = """Return a completion from a local LLM"""
        tags = ["LLM","GenAI", "Local Inference"]

    
    MODEL_PATH = PropertyDescriptor(
        name="Model Path",
        description="Specifies the path to an LLM model",
        required=True,
        validators=[StandardValidators.NON_EMPTY_VALIDATOR],
        expression_language_scope=ExpressionLanguageScope.FLOWFILE_ATTRIBUTES
    )

    property_descriptors = [
        MODEL_PATH
    ]

    def __init__(self, **kwargs):
        pass
        #super().__init__()
        #self.descriptors.append(self.MODEL_PATH)

    def getPropertyDescriptors(self):
        return self.property_descriptors
    
    def transform(self, context, flowfile):
        #prompt_text = context.getProperty(self.PROMPT_TEXT).evaluateAttributeExpressions(flowfile).getValue()
        b_prompt_text = flowfile.getContentsAsBytes()
        prompt_text = str(b_prompt_text)
        model_path = context.getProperty(self.MODEL_PATH).evaluateAttributeExpressions(flowfile).getValue()

        llm = Llama(model_path=model_path)
        
        output = llm("Q:" + prompt_text +" A: ", 
                     max_tokens=100,
                     stop=["Q:", "\n"], 
                     echo=False
        )

        attributes = {"mime.type": "application/json"}
        return FlowFileTransformResult(relationship="success", contents=output, attributes=attributes)