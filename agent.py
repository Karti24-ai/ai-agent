import os
import subprocess
import re
from huggingface_hub import InferenceClient

class MultiLanguageCoder:
    def __init__(self, token: str):
        # Using the lightning-fast 7B coding model
        self.model_id = "Qwen/Qwen2.5-Coder-7B-Instruct"
        self.client = InferenceClient(model=self.model_id, token=token)
        
    def generate_code_block(self, prompt: str, is_javascript: bool, error_message: str = None) -> str:
        lang = "JavaScript" if is_javascript else "Python"
        system_prompt = (
            f"You are an expert {lang} autonomous coding agent. Output ONLY raw executable {lang} code. "
            f"Do NOT wrap it in markdown code blocks like ```{lang.lower()}. Do not include any explanations. "
            f"Just output the exact lines of code to be saved directly to a script file."
        )
        
        user_content = prompt
        if error_message:
            user_content += f"\n\nCRITICAL ERROR: Your previous attempt failed with this error:\n{error_message}\nFix the bugs completely and rewrite the entire script perfectly."

        print(f"🤖 [Agent] Querying {self.model_id} via Inference API...")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        completion = self.client.chat.completions.create(
            model=self.model_id, 
            messages=messages, 
            max_tokens=1500
        )
        
        # Pull content via index fix
        raw_output = completion.choices[0].message.content.strip()
        
        # Clean up any leftover markdown code blocks if the AI outputs them
        clean_code = re.sub(r'^```[a-zA-Z]*\n', '', raw_output)
        clean_code = re.sub(r'\n```$', '', clean_code)
        return clean_code.strip()

    def run_autonomous_loop(self, task_description: str, max_attempts: int = 5):
        # Smart Language Detection
        is_javascript = "javascript" in task_description.lower() or "js" in task_description.lower() or "node" in task_description.lower()
        
        filename = "generated_output.js" if is_javascript else "generated_output.py"
        run_command = ["node", filename] if is_javascript else ["py", filename]
        
        current_prompt = task_description
        error_context = None
        
        for attempt in range(1, max_attempts + 1):
            print(f"\n--- 🚀 Attempt {attempt} of {max_attempts} ---")
            
            # Step 1: AI generates code
            raw_code = self.generate_code_block(current_prompt, error_message=error_context)
            
            # Step 2: Write code directly to file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(raw_code)
            print(f"💾 Saved code to '{filename}'")
            
            # Step 3: Run the code dynamically using your launcher command
            print(f"⚙️ Executing script with {' '.join(run_command)}...")
            result = subprocess.run(run_command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Success! The agent's code ran perfectly without errors.")
                print(f"\n--- Final Execution Output ---\n{result.stdout}")
                return True
            else:
                print("❌ Error Detected! Feeding bugs back to the agent's brain...")
                error_context = result.stderr
                print(f"[Error Details]: {error_context.strip()}")
                
        print("\n💥 Agent hit the maximum attempts and couldn't resolve the bug completely.")
        return False

# --- Run the Multi-Language Agent ---
if __name__ == "__main__":
    HF_TOKEN = "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"
    agent = MultiLanguageCoder(token=HF_TOKEN)
    
    print("==================================================")
    print("   🤖 Multi-Language Coding Agent Terminal Booted   ")
    print("   Supports: Python & JavaScript/Node.js          ")
    print("==================================================")
    
    while True:
        user_task = input("\n🤖 Enter a programming task > ")
        
        if user_task.strip().lower() in ["exit", "quit"]:
            print("Shutting down agent. Goodbye!")
            break
            
        if not user_task.strip():
            continue
            
        agent.run_autonomous_loop(user_task)
