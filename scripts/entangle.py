from qiskit import QuantumCircuit

# Create a 2-qubit circuit
qc = QuantumCircuit(2)

# Apply Hadamard gate to qubit 0 (superposition)
qc.h(0)

# Apply CNOT gate (entanglement)
qc.cx(0, 1)

# Measure
qc.measure_all()

print(qc)
