import json
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# --- Encryption Setup ---
# In a real app, save this key securely!
SECRET_KEY = Fernet.generate_key() 
cipher = Fernet(SECRET_KEY)

class SeaitChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Seait Encrypted Chatbot")
        self.training_data = {"hi": "Hello!", "bye": "Goodbye!"}

        # UI Elements
        self.chat_display = tk.Text(root, height=10, width=50)
        self.chat_display.pack(pady=10)
        
        self.btn_export = tk.Button(root, text="Export .seait", command=self.export_data)
        self.btn_export.pack(side=tk.LEFT, padx=10)

        self.btn_import = tk.Button(root, text="Import .seait", command=self.import_data)
        self.btn_import.pack(side=tk.RIGHT, padx=10)

    def export_data(self):
        """Encrypts JSON data and saves it as a .seait file."""
        # Convert dictionary to JSON string then to bytes
        json_data = json.dumps(self.training_data).encode()
        encrypted_data = cipher.encrypt(json_data)

        file_path = filedialog.asksaveasfilename(defaultextension=".seait", 
                                                filetypes=[("Seait Files", "*.seait")])
        if file_path:
            with open(file_path, "wb") as f:
                f.write(encrypted_data)
            messagebox.showinfo("Success", "Data exported successfully!")

    def import_data(self):
        """Reads a .seait file, decrypts it, and loads the JSON."""
        file_path = filedialog.askopenfilename(filetypes=[("Seait Files", "*.seait")])
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    encrypted_content = f.read()
                
                # Decrypt and load back to JSON
                decrypted_json = cipher.decrypt(encrypted_content).decode()
                self.training_data = json.loads(decrypted_json)
                
                messagebox.showinfo("Success", f"Imported {len(self.training_data)} triggers!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt/import: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeaitChatbot(root)
    root.mainloop()
