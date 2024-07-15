import tkinter as tk
from tkinter import messagebox

# Hamming kodu fonksiyonları
def parity_bitlerini_hesapla(data_bits):
    """
    Verilen veri bitleri için gerekli parite bitlerinin sayısını hesaplar.
    """
    n = len(data_bits)
    r = 0
    while (2**r) < (n + r + 1):
        r += 1
    return r

def hamming_code_olustur(data_bits):
    """
    Verilen veri bitleri için Hamming kodunu oluşturur.
    """
    n = len(data_bits)
    r = parity_bitlerini_hesapla(data_bits)
    hamming_code = [0] * (n + r)
    
    j = 0
    k = 0
    # Veri bitlerini doğru pozisyonlara yerleştir, parite bitlerinin pozisyonlarını atla
    for i in range(1, n + r + 1):
        if i == 2**j:
            j += 1
        else:
            hamming_code[i - 1] = data_bits[k]
            k += 1

    # Parite bitlerini hesapla
    for i in range(r):
        parity_pos = 2**i
        parity = 0
        for j in range(1, n + r + 1):
            if j & parity_pos and j != parity_pos:
                parity ^= hamming_code[j - 1]
        hamming_code[parity_pos - 1] = parity

    return hamming_code

def detect_and_correct_error(hamming_code):
    """
    Hamming kodundaki tek bit hatasını tespit eder ve düzeltir.
    """
    n = len(hamming_code)
    r = parity_bitlerini_hesapla([0] * (n - len(bin(n)[2:]) + 1))
    
    error_pos = 0
    # Parite bitlerini kontrol et
    for i in range(r):
        parity_pos = 2**i
        parity = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity ^= hamming_code[j - 1]
        if parity != 0:
            error_pos += parity_pos
    
    if error_pos != 0:
        # Hata varsa düzelt
        hamming_code[error_pos - 1] ^= 1
        return error_pos, hamming_code
    return None, hamming_code

def databitlerini_cikar(hamming_code):
    """
    Hamming kodundan orijinal veri bitlerini çıkarır.
    """
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

# Bellek sınıfı
class Memory:
    def __init__(self):
        self.memory = {}

    def write(self, address, data):
        """
        Belirli bir adrese veri yazar.
        """
        self.memory[address] = data

    def read(self, address):
        """
        Belirli bir adresten veri okur.
        """
        return self.memory.get(address, None)

    def inject_error(self, address, bit_position):
        """
        Belirtilen adresteki verinin belirtilen bit pozisyonuna tek bit hatası enjekte eder.
        """
        if address in self.memory:
            data = self.memory[address]
            if 0 <= bit_position < len(data):
                data[bit_position] ^= 1
                self.memory[address] = data
            else:
                print("Bit pozisyonu aralık dışında!")
        else:
            print("Adres bulunamadı!")

# Küresel bellek örneği oluştur
memory = Memory()

# Tkinter UI sınıfı
class HammingSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hamming Kodu Simülatörü")
        self.geometry("400x400")
        self.configure(bg="#ffe4e1")  # Daha uyumlu bir arka plan rengi

        # Veri Girişi
        self.data_label = tk.Label(self, text="Veri (4, 8, 16 bit) boşluksuz (örneğin, 1101):", bg="#ffe4e1", fg="black")
        self.data_label.pack(pady=10)
        self.data_entry = tk.Entry(self)
        self.data_entry.pack()

        # Hamming Kodu Oluştur
        self.generate_button = tk.Button(self, text="Hamming Kodu Oluştur", command=self.generate_hamming_code, bg="#ff69b4", fg="white")
        self.generate_button.pack(pady=10)

        self.hamming_code_label = tk.Label(self, text="Oluşturulan Hamming Kodu burada gösterilecek.", bg="#ffe4e1", fg="black")
        self.hamming_code_label.pack(pady=5)

        # Belleğe Yaz
        self.write_button = tk.Button(self, text="Belleğe Yaz", command=self.write_to_memory, bg="#ff69b4", fg="white")
        self.write_button.pack(pady=10)

        # Bellekten Oku
        self.read_button = tk.Button(self, text="Bellekten Oku", command=self.read_from_memory, bg="#ff69b4", fg="white")
        self.read_button.pack(pady=10)

        # Hata Enjekte Et
        self.inject_error_label = tk.Label(self, text="Hata Enjekte Et Bit Pozisyonu (0 bazlı):", bg="#ffe4e1", fg="black")
        self.inject_error_label.pack(pady=10)
        self.inject_error_entry = tk.Entry(self)
        self.inject_error_entry.pack()
        self.inject_error_button = tk.Button(self, text="Hata Enjekte Et", command=self.inject_error, bg="#ff69b4", fg="white")
        self.inject_error_button.pack(pady=10)

        self.output_label = tk.Label(self, text="", bg="#ffe4e1", fg="black")
        self.output_label.pack(pady=10)

    def generate_hamming_code(self):
        """
        Giriş verisi için Hamming kodunu oluştur ve göster.
        """
        data_str = self.data_entry.get()
        data = list(map(int, data_str))
        hamming_code = hamming_code_olustur(data)
        hamming_code_str = ''.join(map(str, hamming_code))
        self.hamming_code_label.config(text=f"Oluşturulan Hamming Kodu: {hamming_code_str}")

    def write_to_memory(self):
        """
        Giriş verisi için Hamming kodunu oluştur ve belleğe yaz.
        """
        data_str = self.data_entry.get()
        data = list(map(int, data_str))
        address = "0x01"
        hamming_code = hamming_code_olustur(data)
        memory.write(address, hamming_code)
        hamming_code_str = ''.join(map(str, hamming_code))
        self.output_label.config(text=f"Adres {address}'e yazılan veri: {hamming_code_str}")

    def read_from_memory(self):
        """
        Bellekten Hamming kodunu oku, varsa hataları tespit ve düzelt, ve sonuçları göster.
        """
        address = "0x01"
        hamming_code = memory.read(address)
        if hamming_code:
            error_pos, corrected_code = detect_and_correct_error(hamming_code)
            corrected_code_str = ''.join(map(str, corrected_code))
            if error_pos is not None:
                self.output_label.config(text=f"Adres {address}'ten okunan veride {error_pos-1}. pozisyonda hata var. Düzeltildi: {corrected_code_str}")
            else:
                self.output_label.config(text=f"Adres {address}'ten okunan veride hata yok: {corrected_code_str}")
        else:
            messagebox.showwarning("Uyarı", "Veri bulunamadı!")

    def inject_error(self):
        """
        Belirtilen adresteki verinin belirtilen bit pozisyonuna tek bit hatası enjekte et.
        """
        address = "0x01"
        try:
            bit_position = int(self.inject_error_entry.get())
            memory.inject_error(address, bit_position)
            hamming_code = memory.read(address)
            if hamming_code:
                error_pos, corrected_code = detect_and_correct_error(hamming_code)
                corrected_code_str = ''.join(map(str, corrected_code))
                enjekted_code_str = ''.join(map(str, hamming_code))
                if error_pos is not None:
                    self.output_label.config(
                        text=f"{bit_position}. pozisyonda hata enjekte edildi.\n"
                             f"Enjekte Edilen Kod: {enjekted_code_str}\n"
                             f"Düzeltildi: {corrected_code_str}")
                else:
                    self.output_label.config(text=f"{bit_position}. pozisyonda hata enjekte edildikten sonra hata tespit edilmedi.")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz bit pozisyonu")

# Uygulamayı çalıştır
if __name__ == "__main__":
    app = HammingSimulator()
    app.mainloop()
