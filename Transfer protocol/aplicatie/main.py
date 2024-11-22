from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from client import send_file
from crypto_utils import generate_key
from user_manager import  save_active_key, get_active_key,  add_key_to_history,get_all_users ,ACTIVE_FILE
import matplotlib.pyplot as plt


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Signing Application")
        self.key = None
        self.username = None

        # Username entry
        Label(root, text="Username:").grid(row=0, column=0)
        self.username_entry = Entry(root)
        self.username_entry.grid(row=0, column=1)

        # Log In button
        Button(root, text="Log In", command=self.log_in).grid(row=1, column=0, columnspan=2)
        self.key_label = Label(root, text="No user logged in")
        self.key_label.grid(row=2, column=0, columnspan=2)

        # Regenerate Key button
        Button(root, text="Regenerate Key", command=self.regenerate_key).grid(row=3, column=0, columnspan=2)

        # Plot Key Distribution button
        Button(root, text="Plot Key Distribution", command=self.plot_key_distribution).grid(row=4, column=0, columnspan=2)

        # Test QRNG Distribution button
        Button(root, text="Test QRNG Distribution", command=self.test_qrng_distribution).grid(row=5, column=0, columnspan=2)

        # Send File button
        Button(root, text="Send File", command=self.send_file).grid(row=6, column=0, columnspan=2)
        # Show users button
        Button(root, text="Show Users", command=self.show_users).grid(row=7, column=0, columnspan=2)

    def log_in(self):
        self.username = self.username_entry.get()
        if not self.username:
            self.key_label.config(text="Enter a username first!")
            return

        # Încarcă cheia activă
        self.key = get_active_key(self.username)
        if not self.key:
            # Generează și salvează o cheie nouă dacă nu există
            self.key = generate_key(self.username)
            add_key_to_history(self.username, self.key)  
            #save_to_file(ACTIVE_FILE, {self.username: self.key}) 
            save_active_key(self.username, self.key)  # Salvează cheia activă
            self.key_label.config(text=f"New key generated for {self.username}")
        else:
            self.key_label.config(text=f"Welcome back, {self.username}! Key loaded.")


        
    def regenerate_key(self):
        if not self.username:
            messagebox.showwarning("Error", "Log in first to regenerate the key!")
            return

        # Confirmă regenerarea cheii
        if not messagebox.askyesno("Confirm", f"Are you sure you want to regenerate the key for {self.username}?"):
            return

        # Generează o nouă cheie
        self.key = generate_key(self.username)
        add_key_to_history(self.username, self.key)  # Salvează în istoricul cheilor
        #save_to_file(ACTIVE_FILE, {self.username: self.key})  # Salvează ca activă
        save_active_key(self.username, self.key)  # Salvează cheia activă
        self.key_label.config(text=f"New key generated for {self.username}")
        messagebox.showinfo("Success", f"New key generated and saved for {self.username}.")
    def show_users(self):
        users = get_all_users()
        if users:
            messagebox.showinfo("Users", f"Active users: {', '.join(users)}")
        else:
            messagebox.showinfo("Users", "No users found.")



    def send_file(self):
        if not self.key:
            self.key_label.config(text="Log in first!")
            return
        file_path = filedialog.askopenfilename(title="Select a file to send")
        if file_path:
            send_file(self.username, self.key, file_path)
            messagebox.showinfo("Success", "File sent successfully!")


    def plot_key_distribution(self):
        if not self.username:
            messagebox.showwarning("Error", "Log in first to plot key distribution!")
            return

        # Load keys for the user from history
        from user_manager import HISTORY_FILE, load_keys
        keys = load_keys(HISTORY_FILE).get(self.username, [])
        if not keys:
            messagebox.showinfo("Info", f"No keys found for user {self.username}.")
            return

        # Define a set of colors for the bars
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta']
        plt.figure(figsize=(10, 6))

        for idx, entry in enumerate(keys, start=1):
            key = entry["key"]  # Extract the actual key
            char_frequency = {"0": key.count("0"), "1": key.count("1")}
            plt.bar(
                char_frequency.keys(),
                char_frequency.values(),
                label=f"Key {idx} ({entry['timestamp']})",
                color=colors[idx % len(colors)],  # Cycle through the colors
                alpha=0.7,
            )

        plt.xlabel("Character")
        plt.ylabel("Frequency")
        plt.title(f"Key Distribution for {self.username}")
        plt.legend()
        plt.show()


    def test_qrng_distribution(self):
        """Test the variability of bits generated by QRNG."""
        from qiskit_qnrg import generate_random_bits

        char_frequency = {"0": 0, "1": 0}
        num_keys = 1000  # Number of keys to test
        for _ in range(num_keys):
            random_bits = generate_random_bits(256)
            char_frequency["0"] += random_bits.count("0")
            char_frequency["1"] += random_bits.count("1")

        # Plot the distribution of bits
        plt.bar(char_frequency.keys(), char_frequency.values(), color="green")
        plt.xlabel("Character")
        plt.ylabel("Frequency")
        plt.title(f"QRNG Bit Distribution for {num_keys} Keys")
        plt.show()


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
