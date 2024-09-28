from transformers import GPT2Tokenizer, GPT2LMHeadModel

class AI:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')

    def generate_advice(self, prompt):
        # Use the GPT model to generate advice based on a prompt
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
        output = self.model.generate(input_ids, max_length=50)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    # Additional AI-related methods
