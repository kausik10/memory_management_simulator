import math
import streamlit as st
class MemoryManager:
    def __init__(self):
        self.total_memory = 0
        self.memory = []
        self.process_table = {}
        self.partitions = []

    def set_total_memory(self, total_memory):
        self.total_memory = total_memory
        self.memory = [None] * total_memory

    def add_process(self, technique, process_id, process_size):
        self.technique = technique
        try:
            if technique == "Fixed-sized Partitioning":
                self.fixed_size_partitioning(process_id, process_size)
            elif technique == "Unequal-sized Fixed Partitioning":
                self.unequal_size_partitioning(process_id, process_size)
            elif technique == "Dynamic Memory Allocation":
                self.dynamic_allocation(process_id, process_size)
            elif technique == "Buddy System":
                self.buddy_system(process_id, process_size)
            elif technique == "Paging":
                self.paging(process_id, process_size)
        except Exception as e:
            st.error(f"Error adding process {process_id}: {str(e)}")

    def remove_process(self, process_id):
        for i in range(self.total_memory):
            if self.memory[i] == process_id:
                self.memory[i] = None
        if process_id in self.process_table:
            del self.process_table[process_id]

    def get_allocation_status(self):
        return self.memory

    def get_allocation_table(self):
        return self.process_table

    def fixed_size_partitioning(self, process_id, process_size):
        partition_size = 32  # Example fixed partition size, ensure it divides total memory size correctly
        num_partitions = self.total_memory // partition_size

        print(f"Total Memory: {self.total_memory}")
        print(f"Partition Size: {partition_size}")
        print(f"Number of Partitions: {num_partitions}")
        print(f"Process Size: {process_size}")

        if process_size > partition_size:
            raise Exception("Process size is larger than partition size.")

        for i in range(0, self.total_memory, partition_size):
            if all(slot is None for slot in self.memory[i:i + partition_size]):
                for j in range(i, i + partition_size):
                    if j < self.total_memory:
                        self.memory[j] = process_id
                self.process_table[process_id] = (i, min(i + partition_size, self.total_memory))
                return
        raise Exception("No suitable partition found for the process.")

    def unequal_size_partitioning(self, process_id, process_size):
        partitions = [64, 128, 256, 512]  # Example unequal-sized partitions
        for partition_size in partitions:
            for i in range(0, self.total_memory, partition_size):
                if all(slot is None for slot in self.memory[i:i + partition_size]):
                    if partition_size >= process_size:
                        for j in range(i, i + partition_size):
                            if j < self.total_memory:
                                self.memory[j] = process_id
                        self.process_table[process_id] = (i, min(i + partition_size, self.total_memory))
                        return
        raise Exception("No suitable partition found for the process.")

    def dynamic_allocation(self, process_id, process_size):
        best_fit_index = -1
        best_fit_size = float('inf')
        for i in range(self.total_memory):
            if self.memory[i] is None:
                size = 0
                for j in range(i, self.total_memory):
                    if self.memory[j] is None:
                        size += 1
                    else:
                        break
                if size >= process_size and size < best_fit_size:
                    best_fit_size = size
                    best_fit_index = i
        if best_fit_index != -1:
            for i in range(best_fit_index, best_fit_index + process_size):
                self.memory[i] = process_id
            self.process_table[process_id] = (best_fit_index, best_fit_index + process_size)
        else:
            raise Exception("No suitable block found for the process.")

    def buddy_system(self, process_id, process_size):
        def next_power_of_two(x):
            return 1 if x == 0 else 2 ** (x - 1).bit_length()

        size = next_power_of_two(process_size)
        buddy_found = False
        for i in range(0, self.total_memory, size):
            if all(slot is None for slot in self.memory[i:i + size]):
                for j in range(i, i + size):
                    if j < self.total_memory:
                        self.memory[j] = process_id
                self.process_table[process_id] = (i, min(i + size, self.total_memory))
                buddy_found = True
                break
        if not buddy_found:
            raise Exception("No suitable block found for the process.")

    def paging(self, process_id, process_size):
        page_size = 4  # Example page size
        num_pages = math.ceil(process_size / page_size)
        frames = []
        for i in range(0, self.total_memory, page_size):
            if len(frames) == num_pages:
                break
            if all(slot is None for slot in self.memory[i:i + page_size]):
                frames.append(i)
        if len(frames) != num_pages:
            raise Exception("Not enough free frames available for paging.")
        for frame in frames:
            for i in range(frame, frame + page_size):
                if i < self.total_memory:
                    self.memory[i] = process_id
        self.process_table[process_id] = frames
