# DiscoView.py (versão com navegação corrigida)

import customtkinter as ctk
from customtkinter import CTkLabel, CTkTextbox, CTkFrame
import datetime

class DiscoView(ctk.CTkToplevel):
    def __init__(self, master=None, nav_callback=None):
        super().__init__(master=master)
        self.title("Gerenciador de Disco e Arquivos")
        self.geometry("1000x700")
        
        self.nav_callback = nav_callback

        self.partitions_frame = CTkFrame(self)
        self.partitions_frame.pack(fill="x", padx=10, pady=10)
        CTkLabel(self.partitions_frame, text="Partições Montadas", font=("Arial", 16, "bold")).pack(anchor="w")
        self.partitions_text = CTkTextbox(self.partitions_frame, height=150, font=("Courier New", 12))
        self.partitions_text.pack(fill="x", expand=True, padx=5, pady=5)
        self.partitions_text.configure(state="disabled")

        self.browser_frame = CTkFrame(self)
        self.browser_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.current_path_label = CTkLabel(self.browser_frame, text="Path:", anchor="w")
        self.current_path_label.pack(fill="x", padx=5, pady=(5,0))

        self.browser_text = CTkTextbox(self.browser_frame, font=("Courier New", 12))
        self.browser_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.browser_text.bind("<Double-1>", self.on_double_click)
        
        # --- MUDANÇA: Lista para mapear linhas clicáveis aos dados ---
        self.display_items = []

    def mostrar_particoes(self, partitions):
        self.partitions_text.configure(state="normal")
        self.partitions_text.delete("1.0", "end")
        
        header = f"{'Dispositivo':<25} {'Ponto de Montagem':<25} {'Total(GB)':>12} {'Usado(GB)':>12} {'Uso(%)':>10}\n"
        self.partitions_text.insert("end", header)
        self.partitions_text.insert("end", "="*84 + "\n")

        for p in partitions:
            line = f"{p['device']:<25} {p['mount_point']:<25} {p['total']:>12.2f} {p['used']:>12.2f} {p['use_perc']:>9.2f}%\n"
            self.partitions_text.insert("end", line)
        
        self.partitions_text.configure(state="disabled")

    # Trecho de DiscoView.py para modificar

    def mostrar_arquivos(self, path, contents):
        self.current_path_label.configure(text=f"Path: {path}")
        self.browser_text.configure(state="normal") # Habilitar para edição
        self.browser_text.delete("1.0", "end")
        
        self.display_items = []

        header = f"{'Nome':<50} {'Tamanho (Bytes)':>20} {'Permissões':>12} {'Modificado em':>20}\n"
        self.browser_text.insert("end", header)
        self.browser_text.insert("end", "="*102 + "\n")
        
        if path != "/":
            self.display_items.append({'name': '..', 'path': '..', 'is_dir': True})
            self.browser_text.insert("end", f"{'[..]':<50}\n")

        for item in contents:
            self.display_items.append(item)
            size_str = str(item['size']) if not item['is_dir'] else "<DIR>"
            mtime_str = datetime.datetime.fromtimestamp(item['mtime']).strftime('%Y-%m-%d %H:%M')
            name_str = f"[{item['name']}]" if item['is_dir'] else item['name']
            
            line = f"{name_str:<50} {size_str:>20} {item['permissions']:>12} {mtime_str:>20}\n"
            self.browser_text.insert("end", line)
        
        self.browser_text.configure(state="disabled") # <-- REMOVA OU COMENTE ESTA LINHA   self.browser_text.configure(state="disabled") # Desabilitar novamente

    def on_double_click(self, event):
        # --- MUDANÇA: Lógica de clique simplificada e robusta ---
        index = self.browser_text.index(f"@{event.x},{event.y}")
        line_num = int(index.split('.')[0])
        
        # O conteúdo clicável começa na linha 3 (após 2 linhas de cabeçalho)
        content_line_index = line_num - 3

        # Verifica se o clique foi em uma linha de conteúdo válida
        if 0 <= content_line_index < len(self.display_items):
            item_clicado = self.display_items[content_line_index]
            
            # Se for um diretório (ou o item ".."), navega
            if item_clicado['is_dir']:
                self.nav_callback(item_clicado['path'])