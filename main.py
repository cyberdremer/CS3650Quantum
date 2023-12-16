import qiskit
from qiskit import *
from qiskit import IBMQ

global provider
global _backend


def set_provider_as_IBM(token: str = None):
    """
    Sets the provider based on the input param. If none is provided, then we use the Aer simulator.
    Otherwise, we load in the account based on the

    :param token:
    """
    global provider
    if token is None or '':
        provider = qiskit.Aer
    else:
        IBMQ.save_account(token)
        IBMQ.load_account()
        provider = IBMQ.get_provider('ibm-q')


def set_backend(backend: str = 'qasm_simulator'):
    """
    Set the specified backend that we will be using, if there is no backend passed in,
    then we will use the 'qasm_simulator' backend in order to simulate the quantum circuit.

    :param backend:
    """
    global _backend
    global provider

    available_backends = provider.backends(backend, filters=lambda x: x.status().operational == True)
    if (backend != '') and (backend in str(available_backends)):
        _backend = provider.get_backend(backend)
    else:
        _backend = provider.get_backend('qasm_simulator')


def flip_coin():
    """
    Function for doing a quantum coinflip, returns the outcome of the coin flip

    :return: 0 or 1
    """
    global _backend
    # Initialize two registers, a Quantum and a Classical register of 1 bit
    quantReg = QuantumRegister(1)
    classicReg = ClassicalRegister(1)

    # Create a quantum circuit using the quantum register and the classical register
    quantCirc = QuantumCircuit(quantReg, classicReg)

    # Apply a Hadamard gate to the quantum circuit
    quantCirc.h(quantReg[0])

    # Measure the quantum circuit to grab the result of the superposition.
    quantCirc.measure(quantReg[0], classicReg[0])

    simulator = _backend

    # Simulate the quantum circuit
    job = execute(quantCirc, backend=simulator, shots=1).result()

    # Get the result of the quantum circuit when it is executed
    quantunBitCounts = job.get_counts(quantCirc)
    print(f"Here is what the quantum computer flipped: {quantunBitCounts}")

    try:
        out = 0
        # Used to see if counts returned 0, throws an exception if counts['0'] cannot be found
        # and breaks out to the except case, which returns 1.
        quantunBitCounts['0']
    except:
        out = 1
    return out


def main():
    set_provider_as_IBM()
    set_backend()
    numOfRounds = int(input("Enter the amount of rounds you would like to play against the quantum computer. "))
    classicalWins = 0
    quantumWins = 0
    roundCount = 0
    while roundCount < numOfRounds:
        userChoiceString = input("Try to guess if the quantum computer chose heads or tails: (A quantum output of 0 "
                                 "is heads, and a quantum output of 1 is tails) ")
        if userChoiceString.upper() == 'HEAD' or 'HEADS':
            valueInBit = 0
        else:
            valueInBit = 1

        quantumComputerChoice = flip_coin()
        if quantumComputerChoice == valueInBit:
            classicalWins += 1
            print("The classical computer won this round.")
        else:
            quantumWins += 1
            print("The quantum computer won this round.")
        roundCount += 1

    if classicalWins > quantumWins:
        print("The player has won the game of heads and tails, congratulations")
    elif classicalWins == quantumWins:
        print("The quantum computer and the classical computer have tied.")

    else:
        print("The quantum computer has won the game of heads and tails, better luck next time")


if __name__ == '__main__':
    main()
