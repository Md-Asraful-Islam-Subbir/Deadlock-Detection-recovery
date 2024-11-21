import tkinter as tk
from tkinter import messagebox
from process import Process, Resource
from deadlock_detection import DeadlockDetector
from recovery import DeadlockRecovery

class DeadlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection and Recovery")

        self.detector = DeadlockDetector()
        self.resources = {}
        self.processes = {}

        # Set up the interface
        self.create_widgets()

    def create_widgets(self):
        # Number of resources and processes
        tk.Label(self.root, text="Number of Resources:").grid(row=0, column=0)
        self.num_resources_entry = tk.Entry(self.root)
        self.num_resources_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Number of Processes:").grid(row=1, column=0)
        self.num_processes_entry = tk.Entry(self.root)
        self.num_processes_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Set", command=self.set_resources_processes).grid(row=2, column=0, columnspan=2)

    def set_resources_processes(self):
        try:
            num_resources = int(self.num_resources_entry.get())
            num_processes = int(self.num_processes_entry.get())
            self.resources = {f"R{i+1}": Resource(f"R{i+1}", total=0, available=0) for i in range(num_resources)}
            self.processes = {f"P{i+1}": Process(f"P{i+1}", {}, {}) for i in range(num_processes)}
            messagebox.showinfo("Success", "Resources and Processes set successfully!")

            # Show resource and process input forms
            self.show_resource_input()
            self.show_process_input()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def show_resource_input(self):
        row = 3
        for rid, resource in self.resources.items():
            tk.Label(self.root, text=f"{rid} Total Units:").grid(row=row, column=0)
            resource.total_entry = tk.Entry(self.root)
            resource.total_entry.grid(row=row, column=1)
            tk.Label(self.root, text=f"{rid} Available Units:").grid(row=row, column=2)
            resource.available_entry = tk.Entry(self.root)
            resource.available_entry.grid(row=row, column=3)
            row += 1

        tk.Button(self.root, text="Set Resources", command=self.set_resource_values).grid(row=row, column=0, columnspan=4)

    def set_resource_values(self):
        try:
            for rid, resource in self.resources.items():
                resource.total = int(resource.total_entry.get())
                resource.available = int(resource.available_entry.get())
                self.detector.add_resource(resource)
            messagebox.showinfo("Success", "Resource values set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for resource values.")

    def show_process_input(self):
        row = 10
        for pid, process in self.processes.items():
            tk.Label(self.root, text=f"{pid} Allocations & Max Needs").grid(row=row, column=0, columnspan=4)
            process.allocated_entries = {}
            process.max_entries = {}

            row += 1
            for rid in self.resources:
                tk.Label(self.root, text=f"{pid} Allocated {rid}:").grid(row=row, column=0)
                allocated_entry = tk.Entry(self.root)
                allocated_entry.grid(row=row, column=1)
                process.allocated_entries[rid] = allocated_entry

                tk.Label(self.root, text=f"{pid} Max {rid}:").grid(row=row, column=2)
                max_entry = tk.Entry(self.root)
                max_entry.grid(row=row, column=3)
                process.max_entries[rid] = max_entry

                row += 1

        tk.Button(self.root, text="Set Processes", command=self.set_process_values).grid(row=row, column=0, columnspan=4)
        tk.Button(self.root, text="Check Deadlock", command=self.check_deadlock).grid(row=row+1, column=0, columnspan=4)

    def set_process_values(self):
        try:
            for pid, process in self.processes.items():
                allocated_resources = {}
                max_resources = {}

                for rid in self.resources:
                    allocated_resources[rid] = int(process.allocated_entries[rid].get())
                    max_resources[rid] = int(process.max_entries[rid].get())

                    # Allocate resources and make requests based on max needs
                    # Allocation: Process to Resource (from resource to process)
                    if allocated_resources[rid] > 0:
                        self.detector.add_allocation(pid, rid)  # Allocation edge
                    
                    # Request: Process to Resource (from process to resource)
                    if allocated_resources[rid] < max_resources[rid]:
                        self.detector.add_request(pid, rid)  # Request edge

                process.allocated_resources = allocated_resources
                process.max_resources = max_resources
                self.detector.add_process(process)

            messagebox.showinfo("Success", "Process values set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for process values.")

    def check_deadlock(self):
        recovery = DeadlockRecovery(self.detector)
        result = recovery.recover_from_deadlock()
        
        if result:
            messagebox.showinfo("Deadlock", f"Deadlock detected and resolved by terminating {result}.")
        else:
            messagebox.showinfo("No Deadlock", "No deadlock detected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockApp(root)
    root.mainloop()
