import tkinter as tk
from tkinter import messagebox
from scapy.all import sniff, IP, TCP, UDP

class PacketAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Net Traffic")

        self.ip_label = tk.Label(root, text="IP:")
        self.ip_label.grid(row=0, column=0)
        self.ip_entry = tk.Entry(root)
        self.ip_entry.grid(row=0, column=1)
        self.start_button = tk.Button(root, text="Старт", command=self.start_sniffing)
        self.start_button.grid(row=0, column=2)
        self.stop_button = tk.Button(root, text="Стоп", command=self.stop_sniffing)
        self.stop_button.grid(row=0, column=3)

        self.incoming_label = tk.Label(root, text="Входящий:")
        self.incoming_label.grid(row=1, column=0)
        self.incoming_traffic = tk.Label(root, text="0")
        self.incoming_traffic.grid(row=1, column=1)

        self.outgoing_label = tk.Label(root, text="Исходящий:")
        self.outgoing_label.grid(row=1, column=2)
        self.outgoing_traffic = tk.Label(root, text="0")
        self.outgoing_traffic.grid(row=1, column=3)

        self.reset_button = tk.Button(root, text="Сброс", command=self.reset_counters)
        self.reset_button.grid(row=1, column=4)

        self.packet_listbox = tk.Listbox(root, width=80, height=20)
        self.packet_listbox.grid(row=2, column=0, columnspan=5)
        self.packet_listbox.bind('<<ListboxSelect>>', self.show_packet_details)

        self.mode_label = tk.Label(root, text="Режим отображения")
        self.mode_label.grid(row=3, column=0, columnspan=2)
        self.mode_var = tk.StringVar(value="full")
        self.full_mode = tk.Radiobutton(root, text="полный", variable=self.mode_var, value="full")
        self.full_mode.grid(row=3, column=2)
        self.dest_port_mode = tk.Radiobutton(root, text="по портам назначения", variable=self.mode_var, value="dest_port")
        self.dest_port_mode.grid(row=3, column=3)
        self.src_port_mode = tk.Radiobutton(root, text="по портам отправки", variable=self.mode_var, value="src_port")
        self.src_port_mode.grid(row=3, column=4)

        self.sniffing = False
        self.incoming = 0
        self.outgoing = 0

        self.packet_details = []

        self.port_data = {}

    def start_sniffing(self):
        self.sniffing = True
        self.sniff_thread()

    def stop_sniffing(self):
        self.sniffing = False

    def sniff_thread(self):
        if self.sniffing:
            sniff(prn=self.process_packet, store=0, timeout=1)
            self.root.after(1000, self.sniff_thread)

    def process_packet(self, packet):
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            size = len(packet)
            ip_version = "IPv4" if packet[IP].version == 4 else "IPv6"
            protocol = "TCP" if TCP in packet else "UDP" if UDP in packet else "Other"
            src_port = packet[TCP].sport if TCP in packet else (packet[UDP].sport if UDP in packet else "N/A")
            dst_port = packet[TCP].dport if TCP in packet else (packet[UDP].dport if UDP in packet else "N/A")

            detailed_info = f"IP Version: {ip_version}\nProtocol: {protocol}\nSource: {ip_src}:{src_port}\nDestination: {ip_dst}:{dst_port}\nSize: {size} bytes"
            self.packet_details.append(detailed_info)

            if self.mode_var.get() == "full":
                packet_info = f"{ip_src} -> {ip_dst} | {size} bytes"
                self.packet_listbox.insert(tk.END, packet_info)

            if ip_src == self.ip_entry.get():
                self.outgoing += size
                self.outgoing_traffic.config(text=str(self.outgoing))
            elif ip_dst == self.ip_entry.get():
                self.incoming += size
                self.incoming_traffic.config(text=str(self.incoming))

            if self.mode_var.get() == "dest_port":
                port = dst_port
            elif self.mode_var.get() == "src_port":
                port = src_port
            else:
                port = None

            if port:
                if port not in self.port_data:
                    self.port_data[port] = 0
                self.port_data[port] += size
                self.update_port_listbox()

    def update_port_listbox(self):
        self.packet_listbox.delete(0, tk.END)
        for port, size in self.port_data.items():
            self.packet_listbox.insert(tk.END, f"Port {port} size: {size}")

    def show_packet_details(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            detailed_info = self.packet_details[index]
            messagebox.showinfo("Packet Details", detailed_info)

    def reset_counters(self):
        self.incoming = 0
        self.outgoing = 0
        self.incoming_traffic.config(text="0")
        self.outgoing_traffic.config(text="0")
        self.packet_details.clear()
        self.port_data.clear()
        self.packet_listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketAnalyzer(root)
    root.mainloop()
