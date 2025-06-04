import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Tema renkleri
BG_COLOR = "#0d1b2d"
INPUT_BG = "#1b463b"
BTN_COLOR = "#1f6f9b"
TEXT_COLOR = "#e5e1dd"
FONT = ("Segoe UI", 10)

class Memory:
    def __init__(self):
        self.memory = {}

    def write(self, address, data):
        self.memory[address] = data

    def read(self, address):
        return self.memory.get(address, None)

    def inject_error(self, address, bit_position):
        if address in self.memory:
            data = self.memory[address]
            if 0 <= bit_position < len(data):
                data[bit_position] ^= 1
                self.memory[address] = data

memory = Memory()

def parity_bitlerini_hesapla(data_bits):
    n = len(data_bits)
    r = 0
    while (2**r) < (n + r + 1):
        r += 1
    return r

def hamming_code_olustur(data_bits):
    n = len(data_bits)
    r = parity_bitlerini_hesapla(data_bits)
    hamming_code = [0] * (n + r)

    j = 0
    k = 0
    for i in range(1, n + r + 1):
        if i == 2**j:
            j += 1
        else:
            hamming_code[i - 1] = data_bits[k]
            k += 1

    for i in range(r):
        parity_pos = 2**i
        parity = 0
        for j in range(1, n + r + 1):
            if j & parity_pos:
                parity ^= hamming_code[j - 1]
        hamming_code[parity_pos - 1] = parity

    return hamming_code

def detect_and_correct_error(hamming_code):
    n = len(hamming_code)
    r = parity_bitlerini_hesapla([0] * (n - len(bin(n)[2:]) + 1))

    error_pos = 0
    syndrome_bits = []

    for i in range(r):
        parity_pos = 2**i
        parity = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity ^= hamming_code[j - 1]
        syndrome_bits.insert(0, parity)
        if parity != 0:
            error_pos += parity_pos

    if error_pos != 0:
        if error_pos > len(hamming_code):
            return "Çift hata olabilir", hamming_code, syndrome_bits
        hamming_code[error_pos - 1] ^= 1
        return error_pos, hamming_code, syndrome_bits

    return None, hamming_code, syndrome_bits

def databitlerini_cikar(hamming_code):
    n = len(hamming_code)
    r = parity_bitlerini_hesapla([0] * (n - len(bin(n)[2:]) + 1))
    data_bits = []

    j = 0
    for i in range(1, n + 1):
        if i != 2**j:
            data_bits.append(hamming_code[i - 1])
        else:
            j += 1
    return data_bits

class HammingSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hamming Kodu Simülatörü ")
        self.geometry("700x800")
        self.configure(bg=BG_COLOR)

        self.addresses = []

        self.data_label = tk.Label(self, text="Veri (4, 8, 16, 32 bit):", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.data_label.pack(pady=5)

        self.data_entry = tk.Entry(self, bg=INPUT_BG, fg=TEXT_COLOR, font=FONT,
                                   validate="key",
                                   validatecommand=(self.register(self.validate_binary_input), '%P'))
        self.data_entry.pack()

        self.address_label = tk.Label(self, text="Bellek Adresi (örneğin: 0x01):", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.address_label.pack(pady=5)
        self.address_entry = tk.Entry(self, bg=INPUT_BG, fg=TEXT_COLOR, font=FONT)
        self.address_entry.pack()

        self.generate_button = tk.Button(self, text="Hamming Kodu Oluştur", command=self.generate_hamming_code, bg=BTN_COLOR, fg="white", font=FONT)
        self.generate_button.pack(pady=10)

        self.hamming_code_label = tk.Label(self, text="Oluşturulan Hamming Kodu burada gösterilecek.", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.hamming_code_label.pack(pady=5)

        self.write_button = tk.Button(self, text="Belleğe Yaz", command=self.write_to_memory, bg=BTN_COLOR, fg="white", font=FONT)
        self.write_button.pack(pady=10)

        self.address_combo_label = tk.Label(self, text="Bellekten işlem için adres seçiniz:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.address_combo_label.pack()
        self.address_combo = ttk.Combobox(self, values=self.addresses, state="readonly", font=FONT)
        self.address_combo.pack(pady=5)

        self.read_button = tk.Button(self, text="Bellekten Oku", command=self.read_from_memory, bg=BTN_COLOR, fg="white", font=FONT)
        self.read_button.pack(pady=10)

        self.inject_error_label = tk.Label(self, text="Hata Enjekte Et Bit Pozisyonu (0 bazlı):", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.inject_error_label.pack(pady=5)
        self.inject_error_entry = tk.Entry(self, bg=INPUT_BG, fg=TEXT_COLOR, font=FONT)
        self.inject_error_entry.pack()
        self.inject_error_button = tk.Button(self, text="Hata Enjekte Et", command=self.inject_error, bg=BTN_COLOR, fg="white", font=FONT)
        self.inject_error_button.pack(pady=10)

        self.visual_frame = tk.Frame(self, bg=INPUT_BG)
        self.visual_frame.pack(pady=10)

        self.output_label = tk.Label(self, text="", bg=BG_COLOR, fg=TEXT_COLOR, wraplength=550, justify="left", font=FONT)
        self.output_label.pack(pady=10)

        self.log_label = tk.Label(self, text="Log Paneli:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.log_label.pack()
        self.log_text = tk.Text(self, height=8, width=70, bg=INPUT_BG, fg=TEXT_COLOR, font=("Courier New", 9))
        self.log_text.pack(pady=5)

    def validate_binary_input(self, P):
        return all(c in '01' for c in P)

    def generate_hamming_code(self):
        data_str = self.data_entry.get()
        try:
            data = list(map(int, data_str))
        except ValueError:
            messagebox.showerror("Hata", "Lütfen sadece 0 ve 1 giriniz.")
            return

        if len(data) not in [4, 8, 16, 32]:
            messagebox.showerror("Hata", "Veri uzunluğu 4, 8, 16 veya 32 bit olmalıdır.")
            return

        hamming_code = hamming_code_olustur(data)
        hamming_code_str = ''.join(map(str, hamming_code))
        self.hamming_code_label.config(text=f"Oluşturulan Hamming Kodu: {hamming_code_str}")

    def write_to_memory(self):
        data_str = self.data_entry.get()
        address = self.address_entry.get().strip()
        try:
            data = list(map(int, data_str))
        except ValueError:
            messagebox.showerror("Hata", "Lütfen sadece 0 ve 1 giriniz.")
            return

        if len(data) not in [4, 8, 16, 32]:
            messagebox.showerror("Hata", "Veri uzunluğu 4, 8, 16 veya 32 bit olmalıdır.")
            return

        if not address:
            messagebox.showerror("Hata", "Lütfen geçerli bir adres giriniz.")
            return

        hamming_code = hamming_code_olustur(data)
        memory.write(address, hamming_code)
        hamming_code_str = ''.join(map(str, hamming_code))
        self.output_label.config(text=f"Adres {address}'e yazılan veri: {hamming_code_str}")

        if address not in self.addresses:
            self.addresses.append(address)
            self.address_combo['values'] = self.addresses

        self.log_text.insert(tk.END, f"{address} -> Belleğe yazıldı: {hamming_code_str}\n")
        self.log_text.see(tk.END)

    def read_from_memory(self):
        address = self.address_combo.get().strip()
        if not address:
            messagebox.showerror("Hata", "Lütfen adres seçiniz.")
            return

        hamming_code = memory.read(address)
        if hamming_code:
            error_pos, corrected_code, syndrome = detect_and_correct_error(hamming_code.copy())
            corrected_code_str = ''.join(map(str, corrected_code))
            original_data = databitlerini_cikar(corrected_code)
            original_data_str = ''.join(map(str, original_data))
            syndrome_str = ''.join(map(str, syndrome))

            if error_pos == "Çift hata olabilir":
                mesaj = f"{address} adresinde ÇİFT HATA olabilir!\nSendrom: {syndrome_str}\nHamming Kodu: {corrected_code_str}"
            elif error_pos is not None:
                mesaj = f"{address} adresinde {error_pos - 1}. bitte hata vardı.\nSendrom: {syndrome_str}\nDüzeltildi: {corrected_code_str}\nOrijinal Veri: {original_data_str}"
            else:
                mesaj = f"{address} adresinde hata yok.\nSendrom: {syndrome_str}\nHamming Kodu: {corrected_code_str}\nOrijinal Veri: {original_data_str}"

            self.output_label.config(text=mesaj)
            self.log_text.insert(tk.END, f"{address} -> Bellekten okundu\n{mesaj}\n\n")
            self.log_text.see(tk.END)
        else:
            messagebox.showwarning("Uyarı", "Adres bellekte yok!")

    def inject_error(self):
        address = self.address_combo.get().strip()
        try:
            bit_position = int(self.inject_error_entry.get())
            memory.inject_error(address, bit_position)
            hamming_code = memory.read(address)
            if hamming_code:
                error_pos, corrected_code, syndrome = detect_and_correct_error(hamming_code.copy())
                corrected_code_str = ''.join(map(str, corrected_code))
                original_data = databitlerini_cikar(corrected_code)
                original_data_str = ''.join(map(str, original_data))
                enjekted_code_str = ''.join(map(str, hamming_code))
                syndrome_str = ''.join(map(str, syndrome))

                if error_pos == "Çift hata olabilir":
                    mesaj = f"{bit_position}. bit pozisyonuna hata enjekte edildi.\nÇift hata olabilir!\nEnjekte Kod: {enjekted_code_str}\nSendrom: {syndrome_str}"
                elif error_pos is not None:
                    mesaj = f"{bit_position}. bit pozisyonuna hata enjekte edildi.\nEnjekte Kod: {enjekted_code_str}\nSendrom: {syndrome_str}\nDüzeltildi: {corrected_code_str}\nOrijinal Veri: {original_data_str}"
                else:
                    mesaj = f"Hata tespit edilemedi.\nEnjekte Kod: {enjekted_code_str}\nSendrom: {syndrome_str}"

                self.output_label.config(text=mesaj)
                self.log_text.insert(tk.END, f"{address} -> Hata enjekte edildi\n{mesaj}\n\n")
                self.log_text.see(tk.END)
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz bit pozisyonu")

if __name__ == "__main__":
    app = HammingSimulator()
    app.mainloop()
