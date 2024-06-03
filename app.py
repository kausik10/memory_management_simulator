import streamlit as st
from memory_management import MemoryManager

# Initialize the memory manager
memory_manager = MemoryManager()

st.title("Memory Management Simulator")

# User input for total memory size
total_memory = st.number_input("Enter total memory size:", min_value=1)
if st.button("Set Total Memory"):
    memory_manager.set_total_memory(total_memory)

# Memory management technique selection
technique = st.selectbox("Select memory management technique:", [
    "Fixed-sized Partitioning",
    "Unequal-sized Fixed Partitioning",
    "Dynamic Memory Allocation",
    "Buddy System",
    "Paging"
])

# Process management
process_id = st.text_input("Enter process ID:")
process_size = st.number_input("Enter process size:", min_value=1)

if st.button("Add Process"):
    memory_manager.add_process(technique, process_id, process_size)

if st.button("Remove Process"):
    memory_manager.remove_process(process_id)

# Display memory allocation status
st.write("Memory Allocation Status:")
st.write(memory_manager.get_allocation_status())

# Display allocation table
st.write("Allocation Table:")
st.write(memory_manager.get_allocation_table())
