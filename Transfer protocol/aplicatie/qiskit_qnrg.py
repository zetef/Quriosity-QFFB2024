from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_random_bits(num_bits, qubits=4):
    qc = QuantumCircuit(qubits, qubits)
    for i in range(qubits):
        qc.h(i)  # Apply Hadamard to all qubits
    qc.measure(range(qubits), range(qubits))  # Measure all qubits
    simulator = AerSimulator()
    result = simulator.run(qc, shots=num_bits // qubits).result()

    # Extract outcomes and construct bitstring
    counts = result.get_counts()
    bitstring = ''.join(format(int(outcome, 2), f'0{qubits}b') for outcome in counts.keys())
    #print(f"biti qnrg{bitstring[:num_bits]}")
    return bitstring[:num_bits]

#print("biti qnrg", generate_random_bits(256))