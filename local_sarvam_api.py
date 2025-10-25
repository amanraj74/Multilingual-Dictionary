"""
Sarvam-Translate API - CPU MODE (100% Reliable)
"""

from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

print("="*80)
print("Loading Sarvam-Translate (CPU mode)...")
print("="*80)

model_name = "sarvamai/sarvam-translate"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# FORCE CPU - No CUDA issues
device = "cpu"
print(f"Device: CPU (avoiding CUDA issues)")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.float32,  # CPU needs float32
    low_cpu_mem_usage=True
)

model.to("cpu")
model.eval()

print("✅ Model loaded on CPU!")
print("="*80)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '').strip()
        target_lang = data.get('target_language', 'Hindi')
        
        print(f"\n{'='*60}")
        print(f"Translating: '{text}' → {target_lang}")
        
        messages = [
            {"role": "system", "content": f"Translate the text below to {target_lang}."},
            {"role": "user", "content": text}
        ]
        
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = tokenizer([prompt], return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.01,
                num_return_sequences=1
            )
        
        generated = outputs[0][inputs['input_ids'].shape[1]:]
        translation = tokenizer.decode(generated, skip_special_tokens=True).strip()
        
        print(f"✅ Result: {translation}")
        print('='*60)
        
        return jsonify({
            "success": True,
            "translation": translation,
            "target_language": target_lang,
            "source_text": text
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model": "sarvam-translate", "device": "cpu"})

if __name__ == '__main__':
    print("\n🚀 Server running: http://localhost:5000")
    print("⚠️  CPU mode - slower but reliable\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
